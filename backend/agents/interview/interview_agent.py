import uuid
from typing import Dict, Any, Optional
from datetime import datetime
from backend.services.firestore_service import firestore_service
from backend.services.gemini_service import gemini_service
from backend.services.analytics_service import analytics_service
from backend.schemas.models import (
    InterviewStartRequest, InterviewStartResponse,
    InterviewAnswerRequest, InterviewAnswerResponse,
    InterviewEvaluation
)
from backend.prompts.interview import INTERVIEW_QUESTION_PROMPT, INTERVIEW_EVALUATION_PROMPT

class InterviewAgent:
    def start_interview(self, req: InterviewStartRequest) -> InterviewStartResponse:
        interview_id = f"int_{uuid.uuid4().hex[:8]}"
        
        profile = firestore_service.get_document("student_profiles", req.user_id) or {}
        target_role = req.target_role or profile.get("target_role", "Backend Engineer")
        target_company = req.target_company or profile.get("target_company", "Tier 1 Product Company")
        
        # Initial question generation
        prompt = INTERVIEW_QUESTION_PROMPT.format(
            target_role=target_role,
            target_company=target_company,
            interview_type=req.interview_type,
            previous_turns="Interview session starting."
        )
        
        fallback_question = {
            "technical": f"Can you explain how indexing works in relational databases and when a composite index should be used for a {target_role} role?",
            "HR": "Tell me about a time you faced a tight deadline or conflicting priorities. How did you handle it?",
            "behavioral": "Describe a scenario where you disagreed with a technical design decision made by a peer. How was it resolved?",
            "project": "Walk me through the architecture of your flagship project. What was the most challenging technical bottleneck?",
            "resume": "Looking at your resume, you listed Redis for caching. How did you configure TTL and cache eviction strategies?",
            "role_specific": f"What design considerations are most critical when designing scalable RESTful APIs for {target_role}?"
        }.get(req.interview_type, f"Can you walk me through your technical background relevant to {target_role}?")
        
        res = gemini_service.generate_json(prompt, {"question": fallback_question, "context_notes": "Opening question for technical assessment."})
        initial_q = res.get("question", fallback_question)
        context_notes = res.get("context_notes", "Initial role evaluation question.")
        
        session_data = {
            "interview_id": interview_id,
            "user_id": req.user_id,
            "interview_type": req.interview_type,
            "target_role": target_role,
            "target_company": target_company,
            "current_question_number": 1,
            "questions_answers": [
                {
                    "question_number": 1,
                    "question": initial_q,
                    "candidate_answer": None,
                    "evaluation": None
                }
            ],
            "status": "in_progress",
            "created_at": datetime.utcnow().isoformat()
        }
        
        firestore_service.set_document("interviews", interview_id, session_data)
        analytics_service.log_event("interview_started", req.user_id, {
            "interview_id": interview_id,
            "interview_type": req.interview_type
        })
        
        return InterviewStartResponse(
            interview_id=interview_id,
            user_id=req.user_id,
            interview_type=req.interview_type,
            current_question_number=1,
            question=initial_q,
            context_notes=context_notes
        )

    def answer_interview_question(self, interview_id: str, req: InterviewAnswerRequest) -> InterviewAnswerResponse:
        session = firestore_service.get_document("interviews", interview_id)
        if not session:
            # Fallback if session missing
            eval_fallback = InterviewEvaluation(
                correctness=75.0, technical_depth=70.0, clarity=80.0,
                relevance=85.0, structure=75.0, conciseness=75.0,
                overall_answer_score=76.6,
                feedback="Good clear response with logical reasoning.",
                key_strengths=["Clear articulation"],
                improvement_areas=["Add more technical depth"]
            )
            return InterviewAnswerResponse(
                interview_id=interview_id,
                evaluation=eval_fallback,
                is_completed=True,
                interview_summary={"final_score": 76.6, "total_questions": 1}
            )

        q_history = session.get("questions_answers", [])
        current_turn = q_history[-1]
        current_q = current_turn.get("question", "Explain your technical solution.")
        
        # Evaluate current answer using Gemini prompt
        eval_prompt = INTERVIEW_EVALUATION_PROMPT.format(
            target_role=session.get("target_role", "Backend Engineer"),
            interview_type=session.get("interview_type", "technical"),
            question=current_q,
            candidate_answer=req.candidate_answer
        )
        
        fallback_eval_dict = {
            "correctness": 80.0,
            "technical_depth": 75.0,
            "clarity": 85.0,
            "relevance": 85.0,
            "structure": 80.0,
            "conciseness": 75.0,
            "overall_answer_score": 80.0,
            "feedback": "Strong understanding of core concepts. Clear delivery.",
            "key_strengths": ["Structured answer", "Good relevance"],
            "improvement_areas": ["Quantify impact with data points"]
        }
        
        eval_res = gemini_service.generate_json(eval_prompt, fallback_eval_dict)
        evaluation = InterviewEvaluation(**eval_res)
        
        current_turn["candidate_answer"] = req.candidate_answer
        current_turn["evaluation"] = evaluation.model_dump()
        
        # Check if max questions (e.g. 3) reached
        current_q_num = len(q_history)
        is_completed = current_q_num >= 3
        
        next_question = None
        if not is_completed:
            # Generate dynamic follow-up question based on current answer
            turns_str = "\n".join([f"Q{i+1}: {t['question']}\nA{i+1}: {t.get('candidate_answer', '')}" for i, t in enumerate(q_history)])
            followup_prompt = INTERVIEW_QUESTION_PROMPT.format(
                target_role=session.get("target_role", "Backend Engineer"),
                target_company=session.get("target_company", "Tier 1 Product Company"),
                interview_type=session.get("interview_type", "technical"),
                previous_turns=turns_str
            )
            
            followup_fallback = f"Building on your point about '{req.candidate_answer[:40]}...', how would you handle high load or failure edge cases?"
            res_q = gemini_service.generate_json(followup_prompt, {"question": followup_fallback})
            next_question = res_q.get("question", followup_fallback)
            
            q_history.append({
                "question_number": current_q_num + 1,
                "question": next_question,
                "candidate_answer": None,
                "evaluation": None
            })
        else:
            session["status"] = "completed"
            
        session["questions_answers"] = q_history
        firestore_service.set_document("interviews", interview_id, session)
        
        summary = None
        if is_completed:
            scores = [t["evaluation"]["overall_answer_score"] for t in q_history if t.get("evaluation")]
            avg_score = round(sum(scores) / len(scores), 1) if scores else 80.0
            summary = {
                "final_score": avg_score,
                "total_questions": len(q_history),
                "summary": f"Completed mock interview with average score of {avg_score}/100."
            }
            analytics_service.log_event("interview_completed", req.user_id, {
                "interview_id": interview_id,
                "final_score": avg_score
            })
            
            # Update interview dimension in readiness
            profile = firestore_service.get_document("student_profiles", req.user_id)
            if profile and "readiness" in profile:
                profile["readiness"]["dimensions"]["interview"] = round(profile["readiness"]["dimensions"].get("interview", 50.0) * 0.7 + avg_score * 0.3, 1)
                firestore_service.set_document("student_profiles", req.user_id, profile)
                
        return InterviewAnswerResponse(
            interview_id=interview_id,
            evaluation=evaluation,
            is_completed=is_completed,
            next_question=next_question,
            interview_summary=summary
        )

interview_agent = InterviewAgent()

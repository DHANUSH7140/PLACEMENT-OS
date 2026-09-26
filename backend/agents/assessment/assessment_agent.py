import uuid
from typing import List, Dict, Any, Optional
from datetime import datetime
from backend.services.firestore_service import firestore_service
from backend.services.analytics_service import analytics_service
from backend.services.gemini_service import gemini_service
from backend.schemas.models import (
    QuestionItem, QuestionAttemptRequest, QuestionAttemptResponse,
    AssessmentStartRequest, AssessmentStartResponse,
    AssessmentSubmitRequest, AssessmentSubmitResponse, MistakeRecord
)
from backend.prompts.skill_gap import SKILL_GAP_PROMPT_TEMPLATE

# Sample default question pool across categories
DEFAULT_QUESTIONS: List[Dict[str, Any]] = [
    {
        "question_id": "q_dsa_1",
        "title": "Binary Tree Level Order Traversal",
        "topic": "Trees",
        "category": "DSA",
        "difficulty": "Medium",
        "content": "Given the root of a binary tree, return the level order traversal of its nodes' values. What data structure is optimal?",
        "options": ["Queue (BFS)", "Stack (DFS)", "Priority Queue", "Array List"],
        "correct_option_index": 0,
        "explanation": "BFS using a Queue processes tree nodes layer by layer efficiently in O(N) time."
    },
    {
        "question_id": "q_dsa_2",
        "title": "Detect Cycle in Directed Graph",
        "topic": "Graphs",
        "category": "DSA",
        "difficulty": "Medium",
        "content": "Which algorithm is commonly used to detect cycles in a directed graph?",
        "options": ["Kahn's Algorithm (Topological Sort / Indegree)", "Binary Search", "Dijkstra Algorithm", "Kruskal Algorithm"],
        "correct_option_index": 0,
        "explanation": "Topological sorting using Kahn's algorithm or DFS recursion stack tracking detects cycles in directed graphs."
    },
    {
        "question_id": "q_sql_1",
        "title": "SQL Join Types",
        "topic": "Joins",
        "category": "SQL",
        "difficulty": "Easy",
        "content": "Which SQL JOIN returns all rows from the left table, and matching rows from the right table?",
        "options": ["LEFT JOIN", "RIGHT JOIN", "INNER JOIN", "FULL OUTER JOIN"],
        "correct_option_index": 0,
        "explanation": "LEFT JOIN preserves all rows from the left table regardless of matching records in the right table."
    },
    {
        "question_id": "q_apt_1",
        "title": "Time and Distance",
        "topic": "Quantitative",
        "category": "Aptitude",
        "difficulty": "Easy",
        "content": "A train moving at 60 km/h passes a pole in 9 seconds. What is the length of the train?",
        "options": ["150 meters", "120 meters", "180 meters", "200 meters"],
        "correct_option_index": 0,
        "explanation": "Speed = 60 * 5/18 = 50/3 m/s. Length = Speed * Time = (50/3) * 9 = 150 meters."
    },
    {
        "question_id": "q_cs_1",
        "title": "Process vs Thread",
        "topic": "Operating Systems",
        "category": "CS Fundamentals",
        "difficulty": "Easy",
        "content": "What is the primary memory sharing difference between threads of the same process?",
        "options": ["Threads share address space and heap", "Threads have isolated memory spaces", "Threads cannot access global variables", "Threads create separate process tables"],
        "correct_option_index": 0,
        "explanation": "Threads belonging to the same process share code, data, heap, and OS resources, but maintain separate stacks."
    }
]

class AssessmentAgent:
    def get_questions(self, category: Optional[str] = None, difficulty: Optional[str] = None) -> List[QuestionItem]:
        # Query Firestore or fallback pool
        stored = firestore_service.query_collection("questions")
        questions_pool = stored if stored else DEFAULT_QUESTIONS
        
        filtered = []
        for q in questions_pool:
            if category and q.get("category", "").lower() != category.lower():
                continue
            if difficulty and q.get("difficulty", "").lower() != difficulty.lower():
                continue
            filtered.append(QuestionItem(**q))
            
        return filtered if filtered else [QuestionItem(**q) for q in DEFAULT_QUESTIONS]

    def record_question_attempt(self, req: QuestionAttemptRequest) -> QuestionAttemptResponse:
        attempt_id = f"att_{uuid.uuid4().hex[:8]}"
        
        # Find question
        questions = self.get_questions()
        target_q = next((q for q in questions if q.question_id == req.question_id), None)
        
        if not target_q:
            # Fallback mock target question if unknown ID passed
            target_q = questions[0]
            
        correct_answer = target_q.options[target_q.correct_option_index] if (target_q.options and target_q.correct_option_index is not None) else "Queue (BFS)"
        
        is_correct = False
        submitted_clean = req.submitted_answer.strip().lower()
        if submitted_clean == correct_answer.lower() or (target_q.correct_option_index is not None and submitted_clean == str(target_q.correct_option_index)):
            is_correct = True
            
        score = 100.0 if is_correct else 0.0
        feedback = "Correct! Excellent grasp of concept." if is_correct else f"Incorrect. Correct answer: {correct_answer}."
        
        attempt_data = {
            "attempt_id": attempt_id,
            "user_id": req.user_id,
            "question_id": target_q.question_id,
            "submitted_answer": req.submitted_answer,
            "is_correct": is_correct,
            "score": score,
            "time_taken_seconds": req.time_taken_seconds,
            "created_at": datetime.utcnow().isoformat()
        }
        firestore_service.set_document("question_attempts", attempt_id, attempt_data)
        
        mistake_logged = False
        if not is_correct:
            mistake_logged = self._log_mistake(req.user_id, target_q, req.submitted_answer)
            
        analytics_service.log_event("question_attempted", req.user_id, {
            "question_id": target_q.question_id,
            "is_correct": is_correct,
            "score": score
        })
        
        return QuestionAttemptResponse(
            attempt_id=attempt_id,
            user_id=req.user_id,
            question_id=target_q.question_id,
            is_correct=is_correct,
            score=score,
            feedback=feedback,
            correct_answer=correct_answer,
            explanation=target_q.explanation or "Standard concept explanation.",
            mistake_logged=mistake_logged
        )

    def start_assessment(self, req: AssessmentStartRequest) -> AssessmentStartResponse:
        assessment_id = f"asm_{uuid.uuid4().hex[:8]}"
        questions = self.get_questions(category=req.category)[:req.question_count]
        
        assessment_data = {
            "assessment_id": assessment_id,
            "user_id": req.user_id,
            "category": req.category,
            "question_ids": [q.question_id for q in questions],
            "status": "in_progress",
            "created_at": datetime.utcnow().isoformat()
        }
        firestore_service.set_document("assessments", assessment_id, assessment_data)
        
        analytics_service.log_event("assessment_started", req.user_id, {
            "assessment_id": assessment_id,
            "category": req.category
        })
        
        return AssessmentStartResponse(
            assessment_id=assessment_id,
            user_id=req.user_id,
            category=req.category,
            questions=questions,
            created_at=assessment_data["created_at"]
        )

    def submit_assessment(self, assessment_id: str, req: AssessmentSubmitRequest) -> AssessmentSubmitResponse:
        asm_doc = firestore_service.get_document("assessments", assessment_id)
        category = asm_doc.get("category", "DSA") if asm_doc else "DSA"
        
        correct_count = 0
        total_questions = len(req.answers)
        new_gaps = []
        
        for ans in req.answers:
            attempt_res = self.record_question_attempt(QuestionAttemptRequest(
                user_id=req.user_id,
                question_id=ans.question_id,
                submitted_answer=ans.submitted_answer,
                time_taken_seconds=ans.time_taken_seconds
            ))
            if attempt_res.is_correct:
                correct_count += 1
            else:
                new_gaps.append(f"Mistake on {ans.question_id}")
                
        overall_score = round((correct_count / max(total_questions, 1)) * 100.0, 1)
        
        # Update user readiness score in Firestore
        profile_doc = firestore_service.get_document("student_profiles", req.user_id)
        route_recalculated = False
        
        if profile_doc and "readiness" in profile_doc:
            readiness = profile_doc["readiness"]
            dims = readiness.get("dimensions", {})
            cat_key = category.lower().replace(" ", "_")
            if cat_key in dims:
                # Weighted adjustment
                dims[cat_key] = round(dims[cat_key] * 0.7 + overall_score * 0.3, 1)
            
            # Recalculate overall readiness
            readiness["overall_score"] = round(sum(dims.values()) / len(dims), 1)
            
            # If poor score (< 60%), flag route recalculation
            if overall_score < 60.0:
                route_recalculated = True
                readiness["critical_gaps"].append(f"Low assessment score ({overall_score}%) in {category}")
                
            profile_doc["readiness"] = readiness
            firestore_service.set_document("student_profiles", req.user_id, profile_doc)
            
        feedback_summary = f"Completed {category} assessment with {overall_score}% accuracy ({correct_count}/{total_questions} correct)."
        
        analytics_service.log_event("assessment_completed", req.user_id, {
            "assessment_id": assessment_id,
            "category": category,
            "overall_score": overall_score,
            "correct_count": correct_count
        })
        
        return AssessmentSubmitResponse(
            assessment_id=assessment_id,
            overall_score=overall_score,
            total_questions=total_questions,
            correct_count=correct_count,
            dimension_impacts={category.lower(): overall_score},
            feedback_summary=feedback_summary,
            new_skill_gaps=new_gaps,
            route_recalculated=route_recalculated
        )

    def _log_mistake(self, user_id: str, question: QuestionItem, submitted_answer: str) -> bool:
        mistake_id = f"mst_{uuid.uuid4().hex[:8]}"
        
        # Check existing mistakes to increment recurrence_count if same question/topic
        existing = firestore_service.query_collection("mistakes", "user_id", user_id)
        recurrence = 1
        for m in existing:
            if m.get("question_id") == question.question_id:
                recurrence = m.get("recurrence_count", 1) + 1
                mistake_id = m.get("mistake_id", mistake_id)
                break

        record = MistakeRecord(
            mistake_id=mistake_id,
            user_id=user_id,
            topic=question.topic,
            question_id=question.question_id,
            question_text=question.content,
            mistake_type="conceptual" if "tree" in question.topic.lower() or "graph" in question.topic.lower() else "misinterpretation",
            likely_cause=f"Incorrect selection: '{submitted_answer}'. Misunderstood algorithm properties.",
            correction=question.explanation or "Review topic core principles.",
            remediation=f"Practice 3 additional practice questions on {question.topic}.",
            recurrence_count=recurrence,
            created_at=datetime.utcnow().isoformat()
        )
        firestore_service.set_document("mistakes", mistake_id, record.model_dump())
        return True

assessment_agent = AssessmentAgent()

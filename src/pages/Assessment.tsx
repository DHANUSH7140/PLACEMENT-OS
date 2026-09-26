import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startAssessment, getAssessmentQuestions, submitAssessmentQuestionAttempt, submitAssessment } from '../services/api/assessment';
import type { PracticeQuestion } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const Assessment = () => {
  const navigate = useNavigate();
  const [assessmentId, setAssessmentId] = useState<string | null>(null);
  const [questions, setQuestions] = useState<PracticeQuestion[]>([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState<Record<string, string>>({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Initialize assessment sequence
    const init = async () => {
      try {
        const { assessmentId } = await startAssessment();
        setAssessmentId(assessmentId);
        const qs = await getAssessmentQuestions(assessmentId);
        setQuestions(qs);
      } catch(e) {
        console.error(e);
      } finally {
        setLoading(false);
      }
    };
    init();
  }, []);

  const handleNext = async () => {
    if (!assessmentId) return;
    const q = questions[currentIndex];
    const answer = answers[q.id] || '';
    
    await submitAssessmentQuestionAttempt(assessmentId, q.id, answer);

    if (currentIndex < questions.length - 1) {
      setCurrentIndex(currentIndex + 1);
    } else {
      await submitAssessment(assessmentId);
      navigate(`/assessment/results?id=${assessmentId}`);
    }
  };

  const currentQ = questions[currentIndex];

  if (loading) {
    return <div className="min-h-screen flex items-center justify-center bg-sage-slate text-matte-charcoal font-medium">Initializing Diagnostic Protocols...</div>;
  }

  if (!questions.length) return <div>Failed to load questions.</div>;

  return (
    <div className="min-h-screen bg-sage-slate p-4 md:p-8 flex flex-col items-center justify-center">
      <div className="w-full max-w-4xl text-center mb-6">
        <h1 className="text-headline-md text-matte-charcoal">Diagnostic Assessment</h1>
        <p className="text-on-surface-variant text-label-md">Question {currentIndex + 1} of {questions.length}</p>
        <div className="w-full h-2 bg-white/40 rounded-full mt-4 overflow-hidden">
          <div className="h-full bg-chartreuse transition-all" style={{ width: `${((currentIndex + 1)/questions.length)*100}%`}}></div>
        </div>
      </div>
      
      <Card className="w-full max-w-4xl min-h-[400px] flex flex-col">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-6">
            <span className="px-3 py-1 bg-[#121316] text-white text-label-sm rounded-full">{currentQ.topic}</span>
            <span className="px-3 py-1 bg-[#f3f4f6] text-[#46464b] text-label-sm rounded-full capitalize">{currentQ.difficulty}</span>
          </div>
          <h2 className="text-headline-sm mb-8">{currentQ.question}</h2>

          {currentQ.questionType === 'mcq' && currentQ.options && (
            <div className="flex flex-col gap-3">
              {currentQ.options.map(opt => (
                <button 
                  key={opt}
                  onClick={() => setAnswers(prev => ({ ...prev, [currentQ.id]: opt }))}
                  className={`w-full text-left p-4 rounded-[16px] border transition-all ${
                    answers[currentQ.id] === opt 
                    ? 'border-chartreuse bg-chartreuse/10 shadow-sm' 
                    : 'border-[#eceeed] bg-[#fbfbfb] hover:bg-white hover:border-[#c7c6cb]'
                  }`}
                >
                  <span className="text-body-md font-medium">{opt}</span>
                </button>
              ))}
            </div>
          )}

          {currentQ.questionType === 'theory' && (
            <textarea 
              className="w-full h-40 p-4 rounded-[16px] bg-[#f3f4f6] text-body-md resize-none outline-none focus:ring-2 focus:ring-chartreuse transition-all"
              placeholder="Explain your thought process..."
              value={answers[currentQ.id] || ''}
              onChange={(e) => setAnswers(prev => ({ ...prev, [currentQ.id]: e.target.value }))}
            />
          )}

          {currentQ.questionType === 'coding' && (
            <div className="bg-[#121316] text-[#e8e8e8] w-full min-h-[300px] rounded-[16px] p-4 font-mono text-body-sm whitespace-pre-wrap">
              {/* Mock code editor */}
              {currentQ.codeTemplate}
            </div>
          )}
        </div>

        <div className="mt-8 flex justify-between border-t border-[#eceeed] pt-6">
          <Button variant="ghost" onClick={() => setCurrentIndex(Math.max(0, currentIndex - 1))} disabled={currentIndex === 0}>
            Previous
          </Button>
          <Button onClick={handleNext} disabled={!answers[currentQ.id] && currentQ.questionType !== 'coding'}>
            {currentIndex === questions.length - 1 ? 'Submit Assessment' : 'Next Question'}
          </Button>
        </div>
      </Card>
    </div>
  );
};

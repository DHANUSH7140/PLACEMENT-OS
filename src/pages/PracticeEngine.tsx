import { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { getPracticeQuestion, submitQuestionAttempt } from '../services/api/practice';
import type { PracticeQuestion, PracticeEvaluation } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { BrainCircuit, AlertCircle, TrendingUp, RefreshCw, XCircle } from 'lucide-react';

export const PracticeEngine = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [question, setQuestion] = useState<PracticeQuestion | null>(null);
  const [answer, setAnswer] = useState('');
  const [evaluation, setEvaluation] = useState<PracticeEvaluation | null>(null);
  const [loading, setLoading] = useState(true);
  const [evaluating, setEvaluating] = useState(false);

  useEffect(() => {
    if (id) {
      getPracticeQuestion(id).then(setQuestion).finally(() => setLoading(false));
    }
  }, [id]);

  const handleSubmit = async () => {
    if (!id || !answer) return;
    setEvaluating(true);
    try {
      const evalResult = await submitQuestionAttempt(id, answer);
      setEvaluation(evalResult);
    } catch (e) {
      console.error(e);
    } finally {
      setEvaluating(false);
    }
  };

  if (loading) return <div className="p-8 text-center text-outline">Loading execution environment...</div>;
  if (!question) return <div className="p-8 text-center text-danger">Question not found.</div>;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto space-y-6">
      
      {!evaluation ? (
        <Card className="flex flex-col min-h-[500px]">
          <div className="flex justify-between items-center mb-6">
            <span className="text-label-md px-3 py-1 bg-[#f3f4f6] text-outline rounded-full">{question.topic}</span>
            <Button variant="ghost" size="sm" onClick={() => navigate('/practice')}><XCircle size={20}/></Button>
          </div>
          
          <h2 className="text-headline-md mb-8">{question.question}</h2>

          <div className="flex-1 flex flex-col gap-4">
            {question.questionType === 'coding' && (
              <div className="w-full bg-[#121316] p-4 rounded-[16px] text-[#e8e8e8] font-mono text-body-sm min-h-[150px]">
                {question.codeTemplate}
              </div>
            )}
            
            <textarea 
              className="w-full flex-1 min-h-[200px] p-4 rounded-[16px] bg-[#fbfbfb] border border-[#eceeed] text-body-md resize-none outline-none focus:ring-2 focus:ring-chartreuse transition-all font-mono"
              placeholder={question.questionType === 'coding' ? "Paste your exact implementation here..." : "Provide your solution..."}
              value={answer}
              onChange={(e) => setAnswer(e.target.value)}
              disabled={evaluating}
            />
          </div>

          <div className="mt-6 flex justify-end">
            <Button onClick={handleSubmit} disabled={!answer || evaluating} className="w-full md:w-auto relative overflow-hidden group">
              {evaluating ? (
                <span className="flex items-center gap-2"><RefreshCw size={18} className="animate-spin" /> RUNNING AI EVALUATION...</span>
              ) : (
                <span className="flex items-center gap-2"><BrainCircuit size={18} /> Submit for Evaluation</span>
              )}
            </Button>
          </div>
        </Card>
      ) : (
        <div className="space-y-6">
          <Card variant="charcoal" className="bg-matte-charcoal text-center p-12">
            <h2 className="text-headline-md mb-8">Evaluation Complete</h2>
            <div className="w-40 h-40 mx-auto rounded-full border-[6px] border-white/10 flex items-center justify-center mb-6 relative">
              <div className="absolute inset-0 rounded-full border-[6px] border-chartreuse" style={{ clipPath: `polygon(0 0, 100% 0, 100% ${evaluation.score}%, 0 ${evaluation.score}%)` }}></div>
              <span className="text-[56px] font-bold font-sans text-white z-10">{evaluation.score}</span>
            </div>
            
            <div className="grid grid-cols-3 gap-4 max-w-lg mx-auto mb-8 border-t border-white/10 pt-8">
              <div className="flex flex-col gap-1">
                <span className="text-body-sm text-[#8a8f98]">Correctness</span>
                <span className="text-headline-sm">{evaluation.correctness}%</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-body-sm text-[#8a8f98]">Approach</span>
                <span className="text-headline-sm">{evaluation.approach}%</span>
              </div>
              <div className="flex flex-col gap-1">
                <span className="text-body-sm text-[#8a8f98]">Understanding</span>
                <span className="text-headline-sm">{evaluation.understanding}%</span>
              </div>
            </div>
          </Card>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <Card className="bg-[#fdf5f5] border-none shadow-none">
              <h3 className="text-headline-sm flex items-center gap-2 text-danger mb-4"><AlertCircle size={18}/> Identified Mistake</h3>
              <p className="text-label-md font-mono text-danger/80 mb-2">{evaluation.mistakeType}</p>
              <p className="text-body-md whitespace-pre-wrap">{evaluation.whyItHappened}</p>
              <p className="text-body-sm mt-4 text-on-surface-variant"><strong>Correct Concept: </strong>{evaluation.correctConcept}</p>
            </Card>

            <Card className="bg-[#f6faeb] border-none shadow-none flex flex-col justify-between">
              <div>
                <h3 className="text-headline-sm flex items-center gap-2 text-secondary mb-4"><TrendingUp size={18}/> Remediation Plan</h3>
                <p className="text-body-md text-on-surface-variant mb-4">{evaluation.explanation}</p>
                <div className="p-4 bg-white rounded-xl border border-[#eceeed]">
                  <p className="text-label-sm text-outline mb-1">Recommended Action</p>
                  <p className="font-medium text-body-sm">{evaluation.recommendedAction}</p>
                </div>
              </div>
              <Button onClick={() => navigate('/dashboard')} className="mt-6 w-full">
                Accept Feedback & Proceed
              </Button>
            </Card>
          </div>
        </div>
      )}
    </div>
  );
};

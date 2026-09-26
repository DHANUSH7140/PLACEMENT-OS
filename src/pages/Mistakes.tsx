import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMistakes } from '../services/api/practice';
import type { Mistake } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { AlertTriangle, RefreshCw, CheckCircle2 } from 'lucide-react';

export const Mistakes = () => {
  const navigate = useNavigate();
  const [mistakes, setMistakes] = useState<Mistake[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMistakes().then(setMistakes).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center text-outline">Loading Error Logs...</div>;

  const unresolved = mistakes.filter(m => m.status === 'unresolved');
  const fixed = mistakes.filter(m => m.status === 'fixed');

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 border-b border-[#eceeed] pb-6">
        <div>
          <h1 className="text-headline-xl text-matte-charcoal mb-2">Mistake Bank</h1>
          <p className="text-body-lg text-on-surface-variant flex items-center gap-2">
            Unresolved Conceptual Gaps <span className="text-danger bg-danger/10 px-2 py-0.5 rounded-full text-label-md font-bold">{unresolved.length}</span>
          </p>
        </div>
      </div>

      <div className="grid grid-cols-1 gap-6">
        {mistakes.length === 0 && <Card className="p-12 text-center text-on-surface-variant">No mistakes recorded yet. Keep practicing!</Card>}
        
        {unresolved.map(mistake => (
          <Card key={mistake.id} className="border-danger/30 relative overflow-hidden">
            <div className="absolute left-0 top-0 bottom-0 w-1 bg-danger"></div>
            <div className="flex justify-between items-start mb-6">
              <div>
                <span className="text-label-sm px-3 py-1 bg-[#121316] text-[#e8fa8c] rounded-full">{mistake.topic}</span>
                <h3 className="text-headline-sm text-matte-charcoal mt-4 mb-2">{mistake.mistakeType}</h3>
                <p className="text-body-md text-on-surface-variant">{mistake.question}</p>
              </div>
              <div className="text-label-sm font-mono text-outline">Attempted {mistake.attemptCount}x</div>
            </div>

            <div className="bg-[#fdf5f5] rounded-xl p-4 mb-6">
              <h4 className="text-label-sm text-danger mb-1 flex items-center gap-2"><AlertTriangle size={14}/> WHY IT HAPPENED</h4>
              <p className="text-body-md text-on-surface-variant mb-4">{mistake.whyItHappened}</p>
              
              <h4 className="text-label-sm text-chartreuse-light bg-matte-charcoal px-2 py-0.5 inline-flex items-center gap-2 rounded-full mb-2"><CheckCircle2 size={12}/> CORRECT CONCEPT</h4>
              <p className="text-body-md text-matte-charcoal font-medium">{mistake.correctConcept}</p>
            </div>

            <div className="flex justify-between items-center bg-[#f3f4f6] -m-5 mt-0 p-4 border-t border-[#eceeed]">
              <div className="text-body-sm text-on-surface-variant">
                <strong>Remediation:</strong> {mistake.recommendedRemediation}
              </div>
              <Button onClick={() => navigate(`/practice?topic=${encodeURIComponent(mistake.topic)}`)} variant="ghost" className="gap-2">
                <RefreshCw size={16}/> Practice Similar
              </Button>
            </div>
          </Card>
        ))}

        {fixed.length > 0 && (
          <div className="mt-8">
            <h2 className="text-headline-sm mb-4">Resolved Mistakes</h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {fixed.map(mistake => (
                <Card key={mistake.id} className="opacity-70 grayscale">
                  <h3 className="font-semibold">{mistake.mistakeType}</h3>
                  <p className="text-body-sm">{mistake.topic}</p>
                </Card>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

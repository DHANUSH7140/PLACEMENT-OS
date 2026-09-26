import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getAssessmentResults } from '../services/api/assessment';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const AssessmentResults = () => {
  const [searchParams] = useSearchParams();
  const id = searchParams.get('id');
  const navigate = useNavigate();
  const [results, setResults] = useState<any>(null);

  useEffect(() => {
    if (id) {
      getAssessmentResults(id).then(setResults).catch(console.error);
    }
  }, [id]);

  if (!results) {
    return <div className="min-h-screen bg-sage-slate flex items-center justify-center font-medium">Processing Telemetry...</div>;
  }

  return (
    <div className="min-h-screen bg-sage-slate flex flex-col items-center justify-center p-4">
      <Card variant="charcoal" className="w-full max-w-2xl text-center p-12">
        <h1 className="text-headline-md mb-2">Diagnostic Complete</h1>
        <p className="text-on-surface-variant text-[#8a8f98] mb-8">Base route recalculation successful.</p>

        <div className="w-48 h-48 mx-auto rounded-full border-[8px] border-chartreuse flex items-center justify-center mb-8 bg-[#1c1e22] shadow-[0_0_40px_rgba(214,242,84,0.15)]">
          <span className="text-[64px] font-bold font-sans text-white">{results.readinessScore}</span>
        </div>
        <p className="text-label-md text-chartreuse mb-8 font-mono">baseline readiness</p>

        <div className="bg-[#1c1e22] rounded-xl p-4 mb-8 text-left border border-white/5">
          <h3 className="text-body-md font-bold mb-3 text-white">Critical Gaps Discovered</h3>
          <ul className="flex flex-col gap-2">
            {results.skillGaps.map((gap: string) => (
              <li key={gap} className="text-body-sm text-[#c7c6ca] flex items-center gap-2">
                <div className="w-1.5 h-1.5 rounded-full bg-danger"></div> {gap}
              </li>
            ))}
          </ul>
        </div>

        <div className="flex justify-center gap-4">
          <Button onClick={() => navigate('/dashboard')} size="lg">
            View Dashboard
          </Button>
          <Button variant="ghost" onClick={() => navigate('/placement-gps')} className="text-white hover:text-black">
            View Placement GPS
          </Button>
        </div>
      </Card>
    </div>
  );
};

import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getInterviewResults } from '../services/api/interview';
import type { InterviewResult } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';

export const InterviewResults = () => {
  const [searchParams] = useSearchParams();
  const id = searchParams.get('id');
  const navigate = useNavigate();
  const [results, setResults] = useState<InterviewResult | null>(null);

  useEffect(() => {
    if (id) {
      getInterviewResults(id).then(setResults).catch(console.error);
    }
  }, [id]);

  if (!results) {
    return <div className="min-h-screen flex items-center justify-center font-medium">Processing Telemetry...</div>;
  }

  const dimensions = [
    { label: 'Correctness', value: results.scores.correctness },
    { label: 'Tech Depth', value: results.scores.technicalDepth },
    { label: 'Clarity', value: results.scores.clarity },
    { label: 'Relevance', value: results.scores.relevance },
    { label: 'Structure', value: results.scores.structure },
    { label: 'Conciseness', value: results.scores.conciseness },
  ];

  return (
    <div className="min-h-screen max-w-5xl mx-auto animate-in fade-in slide-in-from-bottom-4 space-y-8 pb-12">
      <div className="text-center py-8">
        <h1 className="text-headline-xl text-matte-charcoal mb-4">Interview Analysis Complete</h1>
        <p className="text-body-lg text-on-surface-variant max-w-xl mx-auto">Your responses have been processed against our target framework.</p>
      </div>

      <Card variant="charcoal" className="p-8 pb-10 relative overflow-hidden">
        <div className="grid grid-cols-2 md:grid-cols-6 gap-6 relative z-10 text-center">
          {dimensions.map(d => (
            <div key={d.label} className="flex flex-col items-center">
              <div className="w-16 h-16 rounded-full border-4 border-[#2f3131] bg-[#121316] text-white flex items-center justify-center mb-3">
                <span className="font-mono text-headline-sm">{d.value}</span>
              </div>
              <span className="text-label-sm text-[#8a8f98]">{d.label}</span>
            </div>
          ))}
        </div>
      </Card>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="bg-[#f6faeb] border-none shadow-none">
          <h3 className="text-headline-sm text-success-tone mb-4">Strengths</h3>
          <ul className="space-y-3">
            {results.strengths.map(s => (
              <li key={s} className="flex items-start gap-2 text-body-md">
                <div className="w-1.5 h-1.5 rounded-full bg-success-tone mt-2 shrink-0"></div> {s}
              </li>
            ))}
          </ul>
        </Card>
        
        <Card className="bg-[#fdf5f5] border-none shadow-none">
          <h3 className="text-headline-sm text-danger mb-4">Weaknesses</h3>
          <ul className="space-y-3">
            {results.weaknesses.map(w => (
              <li key={w} className="flex items-start gap-2 text-body-md">
                <div className="w-1.5 h-1.5 rounded-full bg-danger mt-2 shrink-0"></div> {w}
              </li>
            ))}
          </ul>
        </Card>
      </div>

      <Card className="p-8 bg-white border border-[#eceeed]">
        <h3 className="text-headline-sm mb-4">Recommendations</h3>
        <ul className="space-y-3 mb-8">
          {results.recommendations.map(r => (
            <li key={r} className="text-body-md text-on-surface-variant pl-4 border-l-2 border-[#dadada]">{r}</li>
          ))}
        </ul>
        
        <div className="p-4 rounded-xl bg-[#121316] text-white flex items-center justify-between flex-wrap gap-4">
          <div>
            <p className="text-label-sm text-[#8a8f98] mb-1">NEXT BEST ACTION</p>
            <p className="text-body-md font-bold text-chartreuse">{results.nextBestAction}</p>
          </div>
          <Button onClick={() => navigate('/dashboard')} className="hover:shadow-chartreuse-glow">
            End Session
          </Button>
        </div>
      </Card>
    </div>
  );
};

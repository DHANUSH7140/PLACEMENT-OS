import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getSkillGaps } from '../services/api/dashboard';
import type { SkillGap as SkillGapType } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Target, TrendingUp, AlertTriangle } from 'lucide-react';

export const SkillGap = () => {
  const navigate = useNavigate();
  const [gaps, setGaps] = useState<SkillGapType[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getSkillGaps().then(setGaps).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="flex items-center justify-center p-8 text-outline">Analyzing Skill Gaps...</div>;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto space-y-8">
      <div className="flex items-center gap-4">
        <Target size={32} className="text-matte-charcoal" />
        <h1 className="text-headline-xl">Skill Gap Analysis</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {gaps.map((gap, i) => (
          <Card key={i} className={`flex flex-col relative overflow-hidden ${gap.status === 'critical' ? 'border-danger/30' : ''}`}>
            {gap.status === 'critical' && <div className="absolute top-0 left-0 right-0 h-1 bg-danger"></div>}
            
            <div className="flex justify-between items-start mb-4">
              <div>
                <h3 className="text-headline-sm flex items-center gap-2">
                  {gap.topic} 
                  {gap.status === 'critical' && <AlertTriangle size={16} className="text-danger"/>}
                </h3>
                <span className="text-label-sm text-on-surface-variant uppercase tracking-wider">{gap.priority} Priority</span>
              </div>
              <div className="flex flex-col items-end">
                <span className="text-headline-md">{gap.currentScore} <span className="text-body-sm text-outline">/ {gap.targetScore}</span></span>
                {gap.trend === 'up' && <span className="text-success-tone text-label-sm flex items-center"><TrendingUp size={12}/> trending</span>}
              </div>
            </div>

            <div className="w-full bg-[#f3f4f6] h-3 rounded-full overflow-hidden mb-6 relative">
              <div className="absolute h-full bg-outline-variant transition-all rounded-full" style={{ width: `${gap.targetScore}%`}}></div>
              <div className={`absolute h-full ${gap.status === 'critical' ? 'bg-danger' : 'bg-chartreuse'} transition-all rounded-full`} style={{ width: `${gap.currentScore}%`}}></div>
            </div>

            <div className="mt-auto">
              <p className="text-label-sm text-on-surface-variant mb-2">Recommended Focus Areas:</p>
              <div className="flex flex-wrap gap-2 mb-6">
                {gap.recommendedTopics.map(t => (
                  <span key={t} className="px-3 py-1 bg-white border border-[#eceeed] rounded-full text-body-sm shadow-sm">{t}</span>
                ))}
              </div>
              <Button onClick={() => navigate(`/practice?topic=${encodeURIComponent(gap.topic)}`)} className="w-full">
                Practice This Now
              </Button>
            </div>
          </Card>
        ))}
      </div>
    </div>
  );
};

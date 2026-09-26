import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getDashboard } from '../services/api/dashboard';
import type { DashboardData } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { CapsuleMeter } from '../components/ui/CapsuleMeter';
import { ChevronRight, Target, AlertTriangle, Zap, CheckCircle2 } from 'lucide-react';

export const Dashboard = () => {
  const navigate = useNavigate();
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getDashboard()
      .then(setData)
      .catch(console.error)
      .finally(() => setLoading(false));
  }, []);

  if (loading) {
    return <div className="h-full flex items-center justify-center text-outline">Loading your tactile OS...</div>;
  }

  if (!data) return <div className="text-error">Failed to load dashboard data.</div>;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 space-y-8">
      {/* Header section */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6">
        <div>
          <h1 className="text-headline-xl text-matte-charcoal mb-2">Systems Online</h1>
          <p className="text-body-lg text-on-surface-variant flex items-center gap-2">
            Placement Readiness <span className="text-chartreuse-light px-2 py-0.5 rounded-full bg-matte-charcoal text-label-md font-bold">{data.readinessScore} / 100</span>
          </p>
        </div>
        <Button onClick={() => navigate('/mission')} size="lg" className="w-full md:w-auto">
          Start Today's Mission
        </Button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Dimensions */}
        <Card className="lg:col-span-2 flex flex-col gap-6">
          <div className="flex items-center justify-between">
            <h2 className="text-headline-sm flex items-center gap-2"><Target size={20} /> Skill Dimensions</h2>
            <Button variant="ghost" size="sm" onClick={() => navigate('/skill-gap')}>View Gap Analysis <ChevronRight size={16}/></Button>
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {data.dimensions.map((dim, i) => (
              <div key={i} className="p-4 rounded-xl border border-[#eceeed] bg-white flex flex-col gap-3">
                <div className="flex justify-between items-center">
                  <span className="font-semibold text-body-md">{dim.title}</span>
                  <span className="text-label-md bg-[#f3f4f6] px-2 py-1 rounded-[8px] border border-[#e2e2e2]">{dim.score}%</span>
                </div>
                <CapsuleMeter score={dim.score} />
                <p className="text-body-sm text-outline mt-1">{dim.recommendedAction}</p>
              </div>
            ))}
          </div>
        </Card>

        {/* Status Panels */}
        <div className="flex flex-col gap-6">
          <Card variant="charcoal" className="relative group">
            <div className="absolute inset-0 bg-gradient-to-br from-chartreuse/10 to-transparent"></div>
            <div className="relative z-10 flex flex-col gap-4">
              <h2 className="text-headline-sm flex items-center gap-2"><CheckCircle2 size={18} className="text-chartreuse" /> Current Strengths</h2>
              <div className="flex flex-wrap gap-2">
                {data.strengths.map(s => <span key={s} className="px-3 py-1 rounded-full bg-white/10 text-body-sm">{s}</span>)}
              </div>
            </div>
          </Card>
          
          <Card className="flex flex-col gap-4 bg-[#fdf5f5] border-none shadow-none">
            <h2 className="text-headline-sm flex items-center gap-2 text-danger"><AlertTriangle size={18} /> Critical Skill Gaps</h2>
            <ul className="space-y-2">
              {data.criticalGaps.map(gap => (
                <li key={gap} className="flex items-center gap-2 text-body-sm font-medium"><div className="w-1.5 h-1.5 rounded-full bg-danger"></div>{gap}</li>
              ))}
            </ul>
          </Card>
        </div>
      </div>

      {/* Next Best Action & Route */}
      <Card variant="charcoal" className="mt-8 flex flex-col md:flex-row items-center justify-between gap-6 p-8 relative overflow-hidden">
        <div className="absolute top-0 right-0 w-64 h-64 bg-chartreuse opacity-10 rounded-full blur-[80px]"></div>
        <div className="relative z-10">
          <p className="text-label-md text-chartreuse-light mb-2 font-mono flex items-center gap-2"><Zap size={16}/> NEXT BEST ACTION</p>
          <h2 className="text-headline-lg mb-2">{data.nextBestAction}</h2>
          <p className="text-on-surface-variant text-[#8a8f98]">Based on your latest Tree Traversal performance.</p>
        </div>
        <Button onClick={() => navigate('/practice/recommended')} size="lg" className="relative z-10 hover:shadow-chartreuse-glow">
          Execute Protocol
        </Button>
      </Card>
    </div>
  );
};

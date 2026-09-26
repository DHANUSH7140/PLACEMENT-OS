import React, { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { getMission } from '../services/api/dashboard';
import type { MissionData } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { CheckCircle2, Play, Flag, ChevronRight } from 'lucide-react';

export const Mission = () => {
  const navigate = useNavigate();
  const [mission, setMission] = useState<MissionData | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getMission().then(setMission).finally(() => setLoading(false));
  }, []);

  if (loading) return <div className="p-8 text-center text-outline">Loading Mission Parameters...</div>;
  if (!mission) return <div className="text-danger p-8">Current mission not found.</div>;

  const completed = mission.tasks.filter(t => t.status === 'completed').length;
  const progress = (completed / mission.tasks.length) * 100;

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto space-y-8">
      <div className="flex flex-col md:flex-row md:items-end justify-between gap-6 pb-6 border-b border-[#eceeed]">
        <div>
          <span className="text-label-md text-chartreuse-light px-3 py-1 bg-matte-charcoal rounded-full font-mono mb-4 inline-block shadow-charcoal-dock">DAILY MISSION</span>
          <h1 className="text-headline-xl text-matte-charcoal mb-2">{mission.title}</h1>
          <p className="text-body-lg text-on-surface-variant max-w-lg">{mission.description}</p>
        </div>
        <div className="flex flex-col items-end">
          <span className="text-headline-md font-mono">{mission.estimatedTime}m</span>
          <span className="text-label-sm text-outline">Estimated Time</span>
        </div>
      </div>

      <div className="w-full bg-[#f3f4f6] h-2 rounded-full overflow-hidden mb-2">
        <div className="h-full bg-chartreuse transition-all duration-1000" style={{ width: `${progress}%` }}></div>
      </div>
      <div className="text-label-sm text-outline font-mono flex justify-between">
        <span>{completed} COMPLETED</span>
        <span>{mission.tasks.length} TOTAL</span>
      </div>

      <div className="grid grid-cols-1 gap-4 mt-8">
        {mission.tasks.map((task, i) => (
          <Card key={task.id} className={`flex flex-col md:flex-row justify-between items-start md:items-center p-6 gap-6 transition-all ${
            task.status === 'active' ? 'border-chartreuse shadow-nested-card' : 'shadow-none'
          }`}>
            <div className="flex items-start gap-4">
              <div className={`mt-1 shrink-0 ${
                task.status === 'completed' ? 'text-success-tone' :
                task.status === 'active' ? 'text-matte-charcoal' : 'text-outline-variant'
              }`}>
                {task.status === 'completed' ? <CheckCircle2 size={24} /> :
                 task.status === 'active' ? <Play size={24} className="fill-current" /> :
                 <CheckCircle2 size={24} />}
              </div>
              <div>
                <div className="flex items-center gap-3">
                  <h3 className={`text-headline-sm ${task.status === 'active' ? 'text-matte-charcoal' : task.status === 'completed' ? 'text-on-surface-variant line-through' : 'text-on-surface-variant'}`}>
                    {task.title}
                  </h3>
                  <span className="text-label-sm uppercase tracking-wider text-outline px-2 py-0.5 bg-[#f3f4f6] rounded-md border border-[#eceeed]">
                    {task.type}
                  </span>
                </div>
                <p className="text-body-sm text-outline mt-1">{task.description}</p>
              </div>
            </div>
            
            <div className="shrink-0 w-full md:w-auto mt-4 md:mt-0">
              {task.status === 'active' && (
                <Button onClick={() => navigate(task.type === 'practice' ? '/practice/recommended' : '/practice')} className="w-full">
                  Execute Task <ChevronRight size={16} />
                </Button>
              )}
              {task.status === 'pending' && <Button variant="ghost" disabled className="w-full">Locked</Button>}
              {task.status === 'completed' && <span className="text-success-tone font-semibold text-body-md flex items-center justify-center gap-1"><CheckCircle2 size={16}/> Done</span>}
            </div>
          </Card>
        ))}
      </div>

      {progress === 100 && (
         <div className="mt-12 p-8 bg-matte-charcoal text-center rounded-[32px] text-white shadow-charcoal-dock animate-in slide-in-from-bottom-8 fade-in">
           <h2 className="text-headline-lg text-chartreuse mb-2">Mission Accomplished</h2>
           <p className="text-[#8a8f98] mb-6">Your Placement Readiness and GPS route have been updated.</p>
           <Button onClick={() => navigate('/dashboard')} className="hover:shadow-chartreuse-glow">
             Return to Dashboard
           </Button>
         </div>
      )}
    </div>
  );
};

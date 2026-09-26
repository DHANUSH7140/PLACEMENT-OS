import { Card } from '../components/ui/Card';
import { BarChart, Bar, LineChart, Line, XAxis, YAxis, Tooltip, ResponsiveContainer, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar } from 'recharts';
import { BarChart as BarChartIcon } from 'lucide-react';

export const Analytics = () => {
  const lineData = [
    { name: 'Week 1', score: 45 },
    { name: 'Week 2', score: 52 },
    { name: 'Week 3', score: 58 },
    { name: 'Week 4', score: 65 },
    { name: 'Week 5', score: 72 },
  ];

  const radarData = [
    { subject: 'Aptitude', A: 78, fullMark: 100 },
    { subject: 'DSA', A: 64, fullMark: 100 },
    { subject: 'SQL', A: 81, fullMark: 100 },
    { subject: 'CS Theory', A: 72, fullMark: 100 },
    { subject: 'Communication', A: 75, fullMark: 100 },
    { subject: 'Projects', A: 60, fullMark: 100 },
  ];

  const barData = [
    { name: 'Mon', questions: 4 },
    { name: 'Tue', questions: 7 },
    { name: 'Wed', questions: 12 },
    { name: 'Thu', questions: 5 },
    { name: 'Fri', questions: 8 },
    { name: 'Sat', questions: 15 },
    { name: 'Sun', questions: 20 },
  ];

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto space-y-6">
      <div className="flex items-center gap-4 pb-6 border-b border-[#eceeed]">
        <BarChartIcon size={32} className="text-matte-charcoal" />
        <h1 className="text-headline-xl">Progress Analytics</h1>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="flex flex-col gap-4 min-h-[300px]">
          <h2 className="text-headline-sm">Readiness Trajectory</h2>
          <div className="flex-1 w-full h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={lineData}>
                <XAxis dataKey="name" fontSize={12} stroke="#a1aca4" tickLine={false} axisLine={false} />
                <YAxis fontSize={12} stroke="#a1aca4" tickLine={false} axisLine={false} domain={[0, 100]} />
                <Tooltip contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                <Line type="monotone" dataKey="score" stroke="#d6f254" strokeWidth={4} dot={{ stroke: '#121316', strokeWidth: 2, r: 6, fill: '#d6f254' }} />
              </LineChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="flex flex-col gap-4 min-h-[300px]">
          <h2 className="text-headline-sm">Skill Distribution</h2>
          <div className="flex-1 w-full h-[250px]">
            <ResponsiveContainer width="100%" height="100%">
              <RadarChart outerRadius="70%" data={radarData}>
                <PolarGrid stroke="#eceeed" />
                <PolarAngleAxis dataKey="subject" fontSize={11} stroke="#121316" />
                <PolarRadiusAxis angle={30} domain={[0, 100]} tick={false} stroke="transparent" />
                <Radar name="Student" dataKey="A" stroke="#121316" fill="#121316" fillOpacity={0.1} strokeWidth={2} />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        </Card>

        <Card className="col-span-1 md:col-span-2 flex flex-col gap-4 min-h-[300px]">
           <h2 className="text-headline-sm">Practice Volume (Questions solved)</h2>
           <div className="flex-1 w-full h-[250px]">
             <ResponsiveContainer width="100%" height="100%">
               <BarChart data={barData}>
                  <XAxis dataKey="name" fontSize={12} stroke="#a1aca4" tickLine={false} axisLine={false} />
                  <YAxis fontSize={12} stroke="#a1aca4" tickLine={false} axisLine={false} />
                  <Tooltip cursor={{ fill: 'rgba(18,19,22,0.04)' }} contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 4px 12px rgba(0,0,0,0.1)' }} />
                  <Bar dataKey="questions" fill="#121316" radius={[4, 4, 0, 0]} />
               </BarChart>
             </ResponsiveContainer>
           </div>
        </Card>
      </div>
    </div>
  );
};

import { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Briefcase, Building, ChevronRight, Zap } from 'lucide-react';
import { Input } from '../components/ui/Input';
import { delay } from '../services/api/client';

export const DreamCompany = () => {
  const [company, setCompany] = useState('');
  const [role, setRole] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<any>(null);

  const handleSearch = async () => {
    if (!company || !role) return;
    setLoading(true);
    await delay(1200);
    setResults({
      matchingSkills: ['Data Structures', 'REST APIs'],
      missingSkills: ['System Design', 'Behavioral STAR methodology'],
      weakAreas: ['Graph Traversal', 'Dynamic Programming speeds'],
      recommendations: [
        'Complete 15 Hard DP questions in the next week.',
        'Review System Design primer focusing on Load Balancers.'
      ]
    });
    setLoading(false);
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 max-w-5xl mx-auto space-y-6">
       <div className="flex flex-col items-center text-center p-8 border-b border-[#eceeed] mb-8">
         <Building size={48} className="text-matte-charcoal mb-4" />
         <h1 className="text-headline-xl">Dream Company DNA</h1>
         <p className="text-body-lg text-on-surface-variant max-w-xl mx-auto mt-2">Discover the exact competencies expected by your target company and compare them against your profile.</p>
       </div>

       {!results && (
         <Card className="max-w-2xl mx-auto flex flex-col gap-6">
           <Input label="Company Name" placeholder="e.g. Google, Amazon, Stripe" value={company} onChange={e => setCompany(e.target.value)} />
           <Input label="Target Role" placeholder="e.g. Frontend Engineer, Product Manager" value={role} onChange={e => setRole(e.target.value)} />
           <Button onClick={handleSearch} disabled={!company || !role || loading}>
              {loading ? 'Decoding Company DNA...' : 'Analyze Requirements'}
           </Button>
         </Card>
       )}

       {results && (
         <div className="space-y-6 animate-in slide-in-from-bottom-4">
           <div className="flex justify-between items-end mb-6">
             <div>
                <h2 className="text-headline-lg">{company}</h2>
                <p className="text-body-lg text-on-surface-variant">{role} Profile Analysis</p>
             </div>
             <Button variant="ghost" onClick={() => setResults(null)}>New Search</Button>
           </div>

           <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
             <Card variant="charcoal" className="bg-matte-charcoal">
               <h3 className="text-headline-sm text-chartreuse mb-4">Matches Profile</h3>
               <div className="flex flex-wrap gap-2">
                 {results.matchingSkills.map((s: string) => <span key={s} className="px-3 py-1 bg-white/10 text-white rounded-md text-body-sm">{s}</span>)}
               </div>
             </Card>

             <Card className="bg-[#fdf5f5] border-none">
               <h3 className="text-headline-sm text-danger mb-4">Missing Requirements</h3>
               <div className="flex flex-wrap gap-2">
                 {results.missingSkills.map((s: string) => <span key={s} className="px-3 py-1 bg-danger/10 text-danger rounded-md text-body-sm">{s}</span>)}
               </div>
             </Card>
           </div>
           
           <Card className="p-8 mt-4">
              <h3 className="text-headline-sm mb-4 flex items-center gap-2"><Zap className="text-warning"/> Tactical Recommendations</h3>
              <ul className="space-y-3">
                {results.recommendations.map((r: string, i: number) => (
                  <li key={i} className="text-body-md bg-[#f3f4f6] p-4 rounded-xl flex items-start gap-4">
                     <span className="text-label-md font-mono text-outline shrink-0 mt-0.5">0{i+1}</span>
                     {r}
                  </li>
                ))}
              </ul>
           </Card>
         </div>
       )}
    </div>
  );
};

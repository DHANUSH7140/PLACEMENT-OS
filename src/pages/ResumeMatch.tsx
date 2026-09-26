import { useState } from 'react';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';
import { delay } from '../services/api/client';
import { Upload, FileText, CheckCircle2, ChevronRight, Briefcase } from 'lucide-react';
import { useNavigate } from 'react-router-dom';

export const ResumeMatch = () => {
  const navigate = useNavigate();
  const [jobDesc, setJobDesc] = useState('');
  const [file, setFile] = useState<File | null>(null);
  
  const [state, setState] = useState<'idle' | 'uploading' | 'processing' | 'analyzing' | 'complete'>('idle');
  const [results, setResults] = useState<any>(null);

  const handleAnalyze = async () => {
    if (!file || !jobDesc) return;
    
    // Simulate complex pipeline steps
    setState('uploading'); await delay(800);
    setState('processing'); await delay(800);
    setState('analyzing'); await delay(1200);
    
    setResults({
      compatibilityScore: 78,
      matchedSkills: ['React', 'TypeScript', 'Responsive Design', 'Problem Solving'],
      missingSkills: ['System Design Basics', 'CI/CD Pipelines'],
      recommendations: ['Highlight the internal tool you built using React context.', 'Add a project demonstrating API integrations.'],
      roleAlignment: 'Strong fit for Frontend roles, moderate fit for Full Stack.'
    });
    setState('complete');
  };

  if (state === 'complete' && results) {
    return (
      <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto space-y-8">
        <h1 className="text-headline-xl">Resume Match Results</h1>
        
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          <Card variant="charcoal" className="flex flex-col items-center justify-center text-center p-8 bg-matte-charcoal">
            <div className="w-32 h-32 rounded-full border-[8px] border-chartreuse flex items-center justify-center mb-4">
              <span className="text-headline-lg text-white">{results.compatibilityScore}%</span>
            </div>
            <p className="text-chartreuse font-mono text-label-sm tracking-wider">COMPATIBILITY</p>
          </Card>
          
          <Card className="col-span-2 p-6 flex flex-col gap-6 bg-white border border-[#eceeed]">
            <div>
              <h3 className="text-headline-sm flex items-center gap-2 mb-3"><CheckCircle2 className="text-success-tone" size={18}/> Matched Skills</h3>
              <div className="flex flex-wrap gap-2">
                {results.matchedSkills.map((s: string) => <span key={s} className="px-3 py-1 bg-[#f3f4f6] text-on-surface-variant rounded-md text-body-sm">{s}</span>)}
              </div>
            </div>
            
            <div>
              <h3 className="text-headline-sm flex items-center gap-2 mb-3 text-warning"><AlertCircleIcon className="text-warning" size={18}/> Missing / Weak Skills</h3>
              <div className="flex flex-wrap gap-2">
                {results.missingSkills.map((s: string) => <span key={s} className="px-3 py-1 bg-warning/10 text-warning rounded-md text-body-sm">{s}</span>)}
              </div>
            </div>
          </Card>
        </div>

        <Card className="p-8">
          <h3 className="text-headline-sm mb-4">Recommendations</h3>
          <ul className="space-y-3 mb-8">
             {results.recommendations.map((r: string, i: number) => (
                <li key={i} className="text-body-md text-on-surface-variant flex items-start gap-3">
                  <div className="w-1.5 h-1.5 rounded-full bg-matte-charcoal mt-2 shrink-0"></div> {r}
                </li>
             ))}
          </ul>
          
          <Button onClick={() => navigate('/resume-assessment')} className="w-full relative overflow-hidden group">
            Generate Questions From My Resume <ChevronRight size={16} className="group-hover:translate-x-1 transition-transform" />
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-4xl mx-auto space-y-6">
      <div className="border-b border-[#eceeed] pb-6 mb-6">
        <h1 className="text-headline-xl text-matte-charcoal flex items-center gap-3">
          <FileText size={32} /> Resume Match
        </h1>
        <p className="text-body-lg text-on-surface-variant mt-2">Align your resume with a specific job description.</p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <Card className="flex flex-col gap-4">
          <h2 className="text-headline-sm">1. Upload Resume</h2>
          <div className="border-2 border-dashed border-[#c7c6cb] rounded-xl p-8 flex flex-col items-center justify-center text-center bg-[#fbfbfb]">
             <Upload size={32} className="text-outline mb-4" />
             <p className="text-body-md mb-4 text-on-surface-variant">Upload PDF or DOCX file.</p>
             <Input type="file" accept=".pdf,.doc,.docx" onChange={e => setFile(e.target.files?.[0] || null)} />
          </div>
          {file && <p className="text-label-sm text-chartreuse-light bg-matte-charcoal px-3 py-1 rounded-md self-start">File attached: {file.name}</p>}
        </Card>

        <Card className="flex flex-col gap-4">
          <h2 className="text-headline-sm">2. Target Job Description</h2>
          <textarea
            className="w-full flex-1 rounded-[16px] bg-[#f3f4f6] p-4 text-body-md border-none outline-none focus:ring-2 focus:ring-chartreuse resize-none"
            placeholder="Paste the job description here..."
            value={jobDesc}
            onChange={e => setJobDesc(e.target.value)}
          />
        </Card>
      </div>

      <div className="flex justify-end mt-4">
        {state !== 'idle' ? (
          <Button disabled className="w-full md:w-auto">
            <span className="flex items-center gap-2 font-mono"><RefreshCwIcon className="animate-spin" size={16}/> {state.toUpperCase()}...</span>
          </Button>
        ) : (
          <Button onClick={handleAnalyze} disabled={!file || !jobDesc} className="w-full md:w-auto">
             Analyze Resume Compatibility
          </Button>
        )}
      </div>
    </div>
  );
};

// Quick stub inline icons
const AlertCircleIcon = ({className, size}: any) => <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>;
const RefreshCwIcon = ({className, size}: any) => <svg className={className} width={size} height={size} viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2"><path d="M21 2v6h-6"/><path d="M3 12a9 9 0 0 1 15-6.7L21 8"/><path d="M3 22v-6h6"/><path d="M21 12a9 9 0 0 1-15 6.7L3 16"/></svg>;

import { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { getPracticeQuestions } from '../services/api/practice';
import type { PracticeQuestion } from '../types';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { PenTool, Filter, Code2, Database, BrainCircuit, Activity } from 'lucide-react';

export const PracticeList = () => {
  const navigate = useNavigate();
  const [params] = useSearchParams();
  const filterTopic = params.get('topic');
  const [questions, setQuestions] = useState<PracticeQuestion[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    getPracticeQuestions(filterTopic || undefined).then(setQuestions).finally(() => setLoading(false));
  }, [filterTopic]);

  if (loading) return <div className="p-8 text-center text-outline">Loading question bank...</div>;

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'coding': return <Code2 size={16} />;
      case 'sql': return <Database size={16} />;
      case 'theory': return <BrainCircuit size={16} />;
      default: return <Activity size={16} />;
    }
  };

  return (
    <div className="animate-in fade-in slide-in-from-bottom-4 duration-500 max-w-5xl mx-auto space-y-6">
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-[#eceeed] pb-6">
        <div>
          <h1 className="text-headline-lg flex items-center gap-3 text-matte-charcoal">
            <PenTool size={28} /> Practice Arena
          </h1>
          {filterTopic && <p className="text-body-md text-on-surface-variant mt-2">Filtered by: <span className="font-semibold text-on-surface">{filterTopic}</span></p>}
        </div>
        <Button variant="secondary" className="gap-2">
          <Filter size={16} /> Filters
        </Button>
      </div>

      <div className="grid grid-cols-1 gap-4">
        {questions.length === 0 ? (
          <Card className="text-center py-12 text-on-surface-variant">No questions found for this topic.</Card>
        ) : (
          questions.map(q => (
            <Card key={q.id} className="flex flex-col md:flex-row md:items-center justify-between gap-6 hover:shadow-low-elevation transition-shadow">
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-2 flex-wrap">
                  <span className="flex items-center gap-1 text-label-sm bg-[#121316] text-[#e8fa8c] px-2 py-1 rounded-md tracking-wider">
                    {getTypeIcon(q.questionType)} {q.questionType.toUpperCase()}
                  </span>
                  <span className={`text-label-sm px-2 py-1 rounded-md uppercase tracking-wider ${
                    q.difficulty === 'hard' ? 'bg-danger/10 text-danger' : 
                    q.difficulty === 'medium' ? 'bg-warning/10 text-warning' : 
                    'bg-chartreuse/20 text-chartreuse-light font-bold bg-matte-charcoal'
                  }`}>
                    {q.difficulty}
                  </span>
                  <span className="text-label-sm bg-[#f3f4f6] text-outline px-2 py-1 rounded-md">{q.topic}</span>
                </div>
                <h3 className="text-headline-sm text-matte-charcoal">{q.question}</h3>
                <div className="flex gap-2 mt-3 flex-wrap">
                  {q.companyTags.map(tag => (
                    <span key={tag} className="text-label-sm text-on-surface-variant bg-white border border-[#eceeed] px-2 py-0.5 rounded-full shadow-sm">{tag}</span>
                  ))}
                </div>
              </div>
              <Button onClick={() => navigate(`/practice/${q.id}`)} className="shrink-0 w-full md:w-auto">
                Attempt
              </Button>
            </Card>
          ))
        )}
      </div>
    </div>
  );
};

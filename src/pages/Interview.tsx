import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { startInterview, submitInterviewAnswer } from '../services/api/interview';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Mic, Send, MessageSquare } from 'lucide-react';
import { Input } from '../components/ui/Input';

interface ChatMessage {
  role: 'system' | 'user';
  text: string;
}

export const Interview = () => {
  const navigate = useNavigate();
  const [setup, setSetup] = useState(true);
  const [role, setRole] = useState('Software Engineer');
  const [type, setType] = useState('Behavioral');
  
  const [interviewId, setInterviewId] = useState<string | null>(null);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const handleStart = async () => {
    setLoading(true);
    try {
      const { id, initialMessage } = await startInterview(type, role, 'medium');
      setInterviewId(id);
      setMessages([{ role: 'system', text: initialMessage }]);
      setSetup(false);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleSend = async () => {
    if (!input || !interviewId) return;
    const userMsg = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', text: userMsg }]);
    setLoading(true);
    
    try {
      const { replyMessage, isRoundComplete } = await submitInterviewAnswer(interviewId, userMsg);
      setMessages(prev => [...prev, { role: 'system', text: replyMessage }]);
      if (isRoundComplete) {
        navigate(`/interview/results?id=${interviewId}`);
      }
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const handleEnd = () => {
    if (interviewId) {
      navigate(`/interview/results?id=${interviewId}`);
    }
  };

  if (setup) {
    return (
      <div className="max-w-2xl mx-auto p-4 md:p-8 animate-in fade-in slide-in-from-bottom-4">
        <h1 className="text-headline-xl text-matte-charcoal mb-8">AI Interview Setup</h1>
        <Card className="flex flex-col gap-6 p-8">
          <div>
            <label className="text-label-md text-on-surface-variant block mb-2">Target Role</label>
            <Input value={role} onChange={e => setRole(e.target.value)} />
          </div>
          <div>
            <label className="text-label-md text-on-surface-variant block mb-2">Interview Type</label>
            <div className="flex flex-wrap gap-2">
              {['Behavioral', 'Technical', 'HR', 'System Design'].map(t => (
                <button key={t} onClick={() => setType(t)} className={`px-4 py-2 rounded-full text-body-sm font-semibold transition-all ${
                  type === t ? 'bg-chartreuse text-[#121316]' : 'bg-[#f3f4f6] text-outline hover:bg-[#e8e8e8]'
                }`}>{t}</button>
              ))}
            </div>
          </div>
          <Button onClick={handleStart} className="mt-4 w-full" disabled={loading}>
            {loading ? 'Initializing Interface...' : 'Commence Interview'}
          </Button>
        </Card>
      </div>
    );
  }

  return (
    <div className="max-w-4xl mx-auto h-[calc(100vh-140px)] flex flex-col pt-4">
      <div className="flex justify-between items-center py-4 border-b border-[#eceeed] mb-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 rounded-full bg-[#121316] flex items-center justify-center text-chartreuse shadow-chartreuse-glow">
            <Mic size={20} />
          </div>
          <div>
            <h2 className="text-headline-sm font-bold text-matte-charcoal">{type} Interview</h2>
            <p className="text-label-sm text-outline">{role}</p>
          </div>
        </div>
        <Button variant="ghost" onClick={handleEnd} className="text-danger hover:bg-danger/10 hover:text-danger">End Interview</Button>
      </div>

      <div className="flex-1 overflow-y-auto flex flex-col gap-4 pb-4">
        {messages.map((msg, i) => (
          <div key={i} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-[80%] rounded-2xl p-4 ${
              msg.role === 'user' 
                ? 'bg-matte-charcoal text-white rounded-br-none' 
                : 'bg-white border border-[#eceeed] text-on-surface rounded-bl-none shadow-sm'
            }`}>
              <p className="text-body-md whitespace-pre-wrap">{msg.text}</p>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex justify-start">
             <div className="max-w-[80%] rounded-2xl p-4 bg-white border border-[#eceeed] rounded-bl-none text-outline flex items-center gap-2">
               <span className="w-2 h-2 rounded-full bg-chartreuse animate-bounce"></span>
               <span className="w-2 h-2 rounded-full bg-chartreuse animate-bounce delay-75"></span>
               <span className="w-2 h-2 rounded-full bg-chartreuse animate-bounce delay-150"></span>
             </div>
          </div>
        )}
      </div>

      <div className="flex gap-2 shrink-0 bg-white p-2 rounded-[24px] border border-[#eceeed] shadow-nested-card">
        <textarea
          className="flex-1 min-h-[50px] bg-transparent resize-none p-3 outline-none text-body-md"
          placeholder="Type your response or use voice..."
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => {
            if (e.key === 'Enter' && !e.shiftKey) {
              e.preventDefault();
              handleSend();
            }
          }}
          disabled={loading}
        />
        <div className="flex flex-col items-center justify-end h-full p-1 gap-2">
          <button className="w-10 h-10 rounded-full bg-[#f3f4f6] text-outline flex items-center justify-center hover:bg-[#e8e8e8] transition-all">
            <Mic size={18} />
          </button>
          <button onClick={handleSend} disabled={!input || loading} className="w-10 h-10 rounded-full bg-chartreuse text-[#121316] flex items-center justify-center disabled:opacity-50 transition-all hover:shadow-chartreuse-glow">
            <Send size={18} className="translate-x-[1px] translate-y-[1px]" />
          </button>
        </div>
      </div>
    </div>
  );
};

import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

const ONBOARDING_STEPS = ['Goals', 'Skills', 'Preparation'];

const ROLES = ['Data Analyst', 'Software Engineer', 'Backend Developer', 'Frontend Developer', 'Full Stack Developer', 'Data Scientist', 'AI/ML Engineer'];

export const Onboarding = () => {
  const navigate = useNavigate();
  const [stepIndex, setStepIndex] = useState(0);
  
  const [formData, setFormData] = useState({
    name: '',
    targetRoles: [] as string[],
    targetCompanies: '',
    programmingLanguages: '',
    preparationTime: '',
    placementTimeline: '',
    experienceLevel: 'Beginner'
  });

  const handleNext = () => {
    if (stepIndex < ONBOARDING_STEPS.length - 1) {
      setStepIndex(stepIndex + 1);
    } else {
      navigate('/assessment'); // redirect to Diagnostic
    }
  };

  const handleBack = () => {
    if (stepIndex > 0) {
      setStepIndex(stepIndex - 1);
    }
  };

  const toggleRole = (role: string) => {
    setFormData(prev => ({
      ...prev,
      targetRoles: prev.targetRoles.includes(role) 
        ? prev.targetRoles.filter(r => r !== role)
        : [...prev.targetRoles, role]
    }));
  };

  return (
    <div className="min-h-screen bg-sage-slate flex flex-col items-center justify-center p-6">
      <div className="w-full max-w-2xl mb-8 flex items-center justify-center gap-2">
        {ONBOARDING_STEPS.map((step, i) => (
          <div key={step} className={`flex items-center gap-2 ${i !== 0 ? 'ml-2' : ''}`}>
            <div className={`h-2 w-8 rounded-full ${i <= stepIndex ? 'bg-chartreuse' : 'bg-white/30'}`} />
            <span className={`text-label-sm ${i <= stepIndex ? 'text-matte-charcoal' : 'text-outline'}`}>{step}</span>
          </div>
        ))}
      </div>

      <Card className="w-full max-w-2xl">
        {stepIndex === 0 && (
          <div className="animate-in fade-in slide-in-from-right-4 duration-300">
            <h2 className="text-headline-md mb-2">Define your goals</h2>
            <p className="text-body-md text-on-surface-variant mb-6">Let's start by understanding what you're aiming for.</p>
            
            <Input label="Full Name" value={formData.name} onChange={e => setFormData({...formData, name: e.target.value})} className="mb-4" />
            
            <label className="text-label-md text-on-surface-variant mb-2 block">Target Roles (Select multiple)</label>
            <div className="flex flex-wrap gap-2 mb-4">
              {ROLES.map(role => (
                <button
                  key={role}
                  onClick={() => toggleRole(role)}
                  className={`px-4 py-2 rounded-full text-body-sm font-semibold transition-all ${
                    formData.targetRoles.includes(role) 
                      ? 'bg-chartreuse text-[#121316]' 
                      : 'bg-[#f3f4f6] text-outline-variant hover:bg-[#e8e8e8] text-on-surface'
                  }`}
                >
                  {role}
                </button>
              ))}
            </div>

            <Input label="Target Companies (comma separated)" placeholder="Google, StartupX" value={formData.targetCompanies} onChange={e => setFormData({...formData, targetCompanies: e.target.value})} />
          </div>
        )}

        {stepIndex === 1 && (
          <div className="animate-in fade-in slide-in-from-right-4 duration-300">
            <h2 className="text-headline-md mb-2">Technical Skills</h2>
            <p className="text-body-md text-on-surface-variant mb-6">What tools are you currently working with?</p>
            
            <Input label="Programming Languages" placeholder="C++, Java, Python..." value={formData.programmingLanguages} onChange={e => setFormData({...formData, programmingLanguages: e.target.value})} className="mb-4" />
            
            <label className="text-label-md text-on-surface-variant mb-2 block">Experience Level</label>
            <select 
              value={formData.experienceLevel} 
              onChange={e => setFormData({...formData, experienceLevel: e.target.value})}
              className="flex h-12 w-full rounded-[16px] bg-[#f3f4f6] px-4 py-2 text-body-md text-on-surface outline-none focus-visible:ring-2 focus-visible:ring-chartreuse mb-4 border-none"
            >
              <option>Beginner (0-1 years)</option>
              <option>Intermediate (1-3 years)</option>
              <option>Advanced (3+ years)</option>
            </select>
          </div>
        )}

        {stepIndex === 2 && (
          <div className="animate-in fade-in slide-in-from-right-4 duration-300">
            <h2 className="text-headline-md mb-2">Preparation Context</h2>
            <p className="text-body-md text-on-surface-variant mb-6">How much time can you commit?</p>
            
            <Input type="number" label="Daily Prep Time (minutes)" placeholder="120" value={formData.preparationTime} onChange={e => setFormData({...formData, preparationTime: e.target.value})} className="mb-4" />
            <Input type="number" label="Placement Timeline (months)" placeholder="6" value={formData.placementTimeline} onChange={e => setFormData({...formData, placementTimeline: e.target.value})} />
          </div>
        )}

        <div className="mt-8 flex justify-between">
          <Button variant="ghost" onClick={handleBack} disabled={stepIndex === 0} className={stepIndex === 0 ? 'opacity-0 pointer-events-none' : ''}>
            Back
          </Button>
          <Button onClick={handleNext}>
            {stepIndex === ONBOARDING_STEPS.length - 1 ? 'Start Diagnostic Assessment' : 'Continue'}
          </Button>
        </div>
      </Card>
    </div>
  );
};

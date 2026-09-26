import React from 'react';
import { useNavigate } from 'react-router-dom';
import { Button } from '../components/ui/Button';

export const Landing = () => {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen bg-sage-slate flex flex-col items-center justify-center p-6 text-center">
      <div className="max-w-2xl bg-porcelain p-12 rounded-3xl shadow-low-elevation border border-[#eceeed]">
        <h1 className="text-headline-xl mb-2 text-matte-charcoal">PLACEMENT OS</h1>
        <p className="text-headline-sm text-outline mb-10">Reimagine Placement Preparation</p>

        <div className="flex flex-col gap-4 text-headline-md text-on-surface-variant font-medium mb-12">
          <span>Know where you stand.</span>
          <span>Know what to improve.</span>
          <span>Know what to do next.</span>
        </div>

        <div className="flex justify-center gap-4">
          <Button size="lg" onClick={() => navigate('/login')}>
            Get Started
          </Button>
          <Button variant="secondary" size="lg" onClick={() => navigate('/login')}>
            Log In
          </Button>
        </div>
      </div>
    </div>
  );
};

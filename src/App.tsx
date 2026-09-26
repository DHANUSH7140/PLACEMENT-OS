import React, { useEffect, useState } from 'react';
import { Routes, Route, useNavigate, Navigate } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import { AppLayout } from './components/layout/AppLayout';
import { Landing } from './pages/Landing';
import { Login } from './pages/Login';
import { Onboarding } from './pages/Onboarding';
import { Dashboard } from './pages/Dashboard';
import { Assessment } from './pages/Assessment';
import { AssessmentResults } from './pages/AssessmentResults';
import { SkillGap } from './pages/SkillGap';
import { PlacementGPS } from './pages/PlacementGPS';
import { Mission } from './pages/Mission';
import { PracticeList } from './pages/PracticeList';
import { PracticeEngine } from './pages/PracticeEngine';
import { Mistakes } from './pages/Mistakes';
import { Interview } from './pages/Interview';
import { InterviewResults } from './pages/InterviewResults';
import { ResumeMatch } from './pages/ResumeMatch';
import { DreamCompany } from './pages/DreamCompany';
import { Analytics } from './pages/Analytics';
import { Profile } from './pages/Profile';



// Protected Route Wrapper
const ProtectedRoute = ({ children }: { children: JSX.Element }) => {
  const { authState } = useAuth();
  if (authState === 'loading') return <div className="p-8">Loading...</div>;
  if (authState === 'unauthenticated') return <Navigate to="/login" replace />;
  return children;
};

function App() {
  const { authState } = useAuth();

  if (authState === 'loading') {
    return <div className="min-h-screen bg-sage-slate flex items-center justify-center"><span className="text-white">Authorizing...</span></div>;
  }

  return (
    <Routes>
      <Route path="/" element={<Landing />} />
      <Route path="/login" element={<Login />} />
      <Route path="/onboarding" element={<ProtectedRoute><Onboarding /></ProtectedRoute>} />
      
      {/* Protected Main App Layout */}
      <Route element={<ProtectedRoute><AppLayout /></ProtectedRoute>}>
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/skill-gap" element={<SkillGap />} />
        <Route path="/placement-gps" element={<PlacementGPS />} />
        <Route path="/mission" element={<Mission />} />
        <Route path="/practice" element={<PracticeList />} />
        <Route path="/practice/:id" element={<PracticeEngine />} />
        <Route path="/mistakes" element={<Mistakes />} />
        <Route path="/resume-match" element={<ResumeMatch />} />
        <Route path="/dream-company" element={<DreamCompany />} />
        <Route path="/analytics" element={<Analytics />} />
        <Route path="/profile" element={<Profile />} />
      </Route>
      
      {/* Protected Standalone (No AppLayout wrapper) */}
      <Route path="/assessment" element={<ProtectedRoute><Assessment /></ProtectedRoute>} />
      <Route path="/resume-assessment" element={<ProtectedRoute><Assessment /></ProtectedRoute>} />
      <Route path="/assessment/results" element={<ProtectedRoute><AssessmentResults /></ProtectedRoute>} />
      <Route path="/interview" element={<ProtectedRoute><Interview /></ProtectedRoute>} />
      <Route path="/interview/results" element={<ProtectedRoute><InterviewResults /></ProtectedRoute>} />
    </Routes>
  );
}

export default App;

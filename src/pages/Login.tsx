import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { signInWithEmailAndPassword, createUserWithEmailAndPassword, signInWithPopup, GoogleAuthProvider } from 'firebase/auth';
import { auth } from '../services/firebase/config';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/ui/Card';
import { Button } from '../components/ui/Button';
import { Input } from '../components/ui/Input';

const MOCK_EMAIL = 'test@test.com';
const MOCK_PASSWORD = 'password123';

export const Login = () => {
  const navigate = useNavigate();
  const { mockLogin } = useAuth();
  const [isSignUp, setIsSignUp] = useState(false);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAuth = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    // Mock login bypass — works without Firebase
    if (email === MOCK_EMAIL && password === MOCK_PASSWORD) {
      mockLogin();
      navigate('/dashboard');
      return;
    }

    if (!auth) {
      setError('Firebase not configured. Use test@test.com / password123 to log in.');
      setLoading(false);
      return;
    }

    try {
      if (isSignUp) {
        await createUserWithEmailAndPassword(auth, email, password);
        navigate('/onboarding');
      } else {
        await signInWithEmailAndPassword(auth, email, password);
        navigate('/dashboard');
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };


  const handleGoogle = async () => {
    if (!auth) {
      setError('Firebase not configured.');
      return;
    }
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
      navigate('/dashboard');
    } catch (err: any) {
      setError(err.message);
    }
  };

  return (
    <div className="min-h-screen bg-sage-slate flex items-center justify-center p-6">
      <Card className="w-full max-w-md">
        <h1 className="text-headline-lg mb-6 text-center">{isSignUp ? 'Create Account' : 'Welcome Back'}</h1>
        
        {/* Dev hint — remove after Firebase is configured */}
        <div className="mb-4 p-3 bg-[#f3f4f6] border border-[#eceeed] rounded-xl text-body-sm text-on-surface-variant font-mono">
          <span className="font-semibold text-matte-charcoal block mb-1">🔑 Dev Mode Credentials</span>
          <span>Email: test@test.com</span><br/>
          <span>Password: password123</span>
        </div>

        {error && <div className="mb-4 p-3 bg-red-50 text-red-700 rounded-sm text-body-sm">{error}</div>}
        <form onSubmit={handleAuth} className="flex flex-col gap-4">
          <Input 
            label="Email Address" 
            type="email" 
            value={email} 
            onChange={(e) => setEmail(e.target.value)} 
            required 
            placeholder="student@university.edu"
          />
          <Input 
            label="Password" 
            type="password" 
            value={password} 
            onChange={(e) => setPassword(e.target.value)} 
            required 
          />
          <Button type="submit" disabled={loading} className="mt-2">
            {loading ? 'Processing...' : (isSignUp ? 'Sign Up' : 'Log In')}
          </Button>
        </form>
        
        <div className="mt-6 flex flex-col gap-4 relative">
          <div className="absolute inset-0 flex items-center">
            <div className="w-full border-t border-[#eceeed]"></div>
          </div>
          <div className="relative flex justify-center text-body-sm">
            <span className="bg-white px-2 text-outline">or</span>
          </div>
          <Button variant="secondary" onClick={handleGoogle}>
            Continue with Google
          </Button>
        </div>

        <p className="mt-6 text-center text-body-sm text-on-surface-variant">
          {isSignUp ? 'Already have an account?' : "Don't have an account?"}{' '}
          <button onClick={() => setIsSignUp(!isSignUp)} className="font-semibold text-matte-charcoal hover:underline">
            {isSignUp ? 'Log in' : 'Sign up'}
          </button>
        </p>
      </Card>
    </div>
  );
};

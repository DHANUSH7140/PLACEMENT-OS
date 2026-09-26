import React, { createContext, useContext, useEffect, useState } from 'react';
import { getAuth, onAuthStateChanged } from 'firebase/auth';
import type { User } from 'firebase/auth';

type AuthState = 'loading' | 'authenticated' | 'unauthenticated';

interface AuthContextType {
  user: User | null;
  authState: AuthState;
  mockLogin: () => void;
  mockLogout: () => void;
}

const AuthContext = createContext<AuthContextType>({
  user: null,
  authState: 'loading',
  mockLogin: () => {},
  mockLogout: () => {},
});

export const useAuth = () => useContext(AuthContext);

// Mock user object that looks like a Firebase User
const MOCK_USER = { uid: 'mock-user-001', email: 'test@test.com', displayName: 'Test Student' } as unknown as User;

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [authState, setAuthState] = useState<AuthState>('loading');

  const mockLogin = () => {
    setUser(MOCK_USER);
    setAuthState('authenticated');
    localStorage.setItem('mock_auth', 'true');
  };

  const mockLogout = () => {
    setUser(null);
    setAuthState('unauthenticated');
    localStorage.removeItem('mock_auth');
  };

  useEffect(() => {
    // Check persisted mock session first
    if (localStorage.getItem('mock_auth') === 'true') {
      setUser(MOCK_USER);
      setAuthState('authenticated');
      return;
    }

    try {
      const auth = getAuth();
      const unsubscribe = onAuthStateChanged(auth, (currentUser) => {
        if (currentUser) {
          setUser(currentUser);
          setAuthState('authenticated');
        } else {
          setUser(null);
          setAuthState('unauthenticated');
        }
      });
      return () => unsubscribe();
    } catch (e) {
      console.warn("Firebase not initialized yet, defaulting to unauthenticated mode.");
      setAuthState('unauthenticated');
    }
  }, []);

  return (
    <AuthContext.Provider value={{ user, authState, mockLogin, mockLogout }}>
      {children}
    </AuthContext.Provider>
  );
};

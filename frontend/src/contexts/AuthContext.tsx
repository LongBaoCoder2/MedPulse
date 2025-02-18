import { createContext, useContext, useState, useEffect, ReactNode } from 'react';
import Cookies from 'js-cookie';
import { getProfile } from '@/api/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  login: (token: string) => void;
  logout: () => void;

  // User info
  email: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [email, setEmail] = useState<string>('');

  useEffect(() => {
    const token = Cookies.get('access_token');
    setIsAuthenticated(!!token);

    getProfile().then(profile => {
      setEmail(profile.email);
    })
  }, []);

  const login = (token: string) => {
    Cookies.set('access_token', token, { expires: 7 });
    setIsAuthenticated(true);
  };

  const logout = () => {
    Cookies.remove('access_token');
    setIsAuthenticated(false);
    setEmail('');
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, login, logout, email }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
} 
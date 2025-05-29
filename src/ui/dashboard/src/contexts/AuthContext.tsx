/**
 * Authentication Context
 * Provides authentication state and functions throughout the application
 */

import React, { createContext, useContext, useState, useEffect } from 'react';
import { login as apiLogin, logout as apiLogout, getCurrentUser } from '../services/auth';

interface AuthContextType {
  isAuthenticated: boolean;
  user: any | null;
  login: (username: string, password: string) => Promise<void>;
  logout: () => Promise<void>;
  loading: boolean;
  error: string | null;
}

const AuthContext = createContext<AuthContextType>({
  isAuthenticated: false,
  user: null,
  login: async () => {},
  logout: async () => {},
  loading: false,
  error: null
});

export const useAuth = () => useContext(AuthContext);

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [isAuthenticated, setIsAuthenticated] = useState<boolean>(false);
  const [user, setUser] = useState<any | null>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Check if user is already authenticated on mount
  useEffect(() => {
    const checkAuth = async () => {
      const token = localStorage.getItem('auth_token');
      
      if (token) {
        try {
          const userData = await getCurrentUser();
          setUser(userData);
          setIsAuthenticated(true);
        } catch (err) {
          // Token is invalid or expired
          localStorage.removeItem('auth_token');
          setIsAuthenticated(false);
          setUser(null);
        }
      }
      
      setLoading(false);
    };
    
    checkAuth();
  }, []);

  const login = async (username: string, password: string) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiLogin(username, password);
      
      // Store token in localStorage
      localStorage.setItem('auth_token', response.token);
      
      setUser(response.user);
      setIsAuthenticated(true);
    } catch (err: any) {
      setError(err.message || 'Login failed');
      throw err;
    } finally {
      setLoading(false);
    }
  };

  const logout = async () => {
    setLoading(true);
    
    try {
      await apiLogout();
    } catch (err) {
      console.error('Logout error:', err);
    } finally {
      // Remove token from localStorage
      localStorage.removeItem('auth_token');
      
      setUser(null);
      setIsAuthenticated(false);
      setLoading(false);
    }
  };

  return (
    <AuthContext.Provider value={{ isAuthenticated, user, login, logout, loading, error }}>
      {children}
    </AuthContext.Provider>
  );
};

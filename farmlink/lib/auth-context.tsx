// app/contexts/AuthContext.tsx
"use client";

import React, { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { getCurrentUser, getCurrentToken, logout as apiLogout } from "@/lib/api";

interface User {
  id: string | null;
  role: string | null;
  email: string | null;
  username: string | null;
  isAuthenticated: boolean;
}

interface AuthContextType {
  user: User;
  token: string | null;
  loading: boolean;
  logout: () => Promise<void>;
  refreshUser: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User>({
    id: null,
    role: null,
    email: null,
    username: null,
    isAuthenticated: false,
  });
  const [token, setToken] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  const loadAuthData = async () => {
    setLoading(true);
    
    // Load user data from localStorage
    const userData = getCurrentUser();
    setUser(userData);
    
    // Get token from API
    try {
      const currentToken = await getCurrentToken();
      setToken(currentToken);
      
      // Update user authentication status based on token
      if (currentToken) {
        setUser(prev => ({ ...prev, isAuthenticated: true }));
      }
    } catch (error) {
      console.error("Error loading auth data:", error);
    } finally {
      setLoading(false);
    }
  };

  const handleLogout = async () => {
    await apiLogout();
    setUser({
      id: null,
      role: null,
      email: null,
      username: null,
      isAuthenticated: false,
    });
    setToken(null);
  };

  useEffect(() => {
    loadAuthData();
  }, []);

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        logout: handleLogout,
        refreshUser: loadAuthData,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
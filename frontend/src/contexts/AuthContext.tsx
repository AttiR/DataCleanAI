import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react';
import { apiService } from '../services/apiService';

interface User {
  id: number;
  username: string;
  email: string;
  full_name?: string;
  is_active: boolean;
  is_email_verified: boolean;
  created_at: string;
  last_login?: string;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  error: string | null;
}

type AuthAction =
  | { type: 'AUTH_START' }
  | { type: 'AUTH_SUCCESS'; payload: { user: User; token: string } }
  | { type: 'AUTH_FAILURE'; payload: string }
  | { type: 'AUTH_LOGOUT' }
  | { type: 'CLEAR_ERROR' }
  | { type: 'UPDATE_USER'; payload: User };

interface AuthContextType extends AuthState {
  login: (email: string, password: string) => Promise<void>;
  register: (userData: RegisterData) => Promise<void>;
  logout: () => void;
  verifyEmail: (token: string) => Promise<void>;
  resendVerification: (email: string) => Promise<void>;
  requestPasswordReset: (email: string) => Promise<void>;
  resetPassword: (token: string, newPassword: string) => Promise<void>;
  changePassword: (currentPassword: string, newPassword: string) => Promise<void>;
  clearError: () => void;
}

interface RegisterData {
  username: string;
  email: string;
  password: string;
  full_name?: string;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const authReducer = (state: AuthState, action: AuthAction): AuthState => {
  switch (action.type) {
    case 'AUTH_START':
      return {
        ...state,
        isLoading: true,
        error: null,
      };
    case 'AUTH_SUCCESS':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: true,
        user: action.payload.user,
        token: action.payload.token,
        error: null,
      };
    case 'AUTH_FAILURE':
      return {
        ...state,
        isLoading: false,
        isAuthenticated: false,
        user: null,
        token: null,
        error: action.payload,
      };
    case 'AUTH_LOGOUT':
      return {
        ...state,
        isAuthenticated: false,
        user: null,
        token: null,
        error: null,
      };
    case 'CLEAR_ERROR':
      return {
        ...state,
        error: null,
      };
    case 'UPDATE_USER':
      return {
        ...state,
        user: action.payload,
      };
    default:
      return state;
  }
};

const initialState: AuthState = {
  user: null,
  token: localStorage.getItem('token'),
  isAuthenticated: false,
  isLoading: false,
  error: null,
};

export const AuthProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [state, dispatch] = useReducer(authReducer, initialState);

  // Check if user is authenticated on app load
  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      // Verify token and get user info
      apiService.get('/auth/me')
        .then((response) => {
          dispatch({
            type: 'AUTH_SUCCESS',
            payload: { user: response.data, token },
          });
        })
        .catch(() => {
          localStorage.removeItem('token');
          dispatch({ type: 'AUTH_LOGOUT' });
        });
    }
  }, []);

  const login = async (email: string, password: string) => {
    dispatch({ type: 'AUTH_START' });
    try {
      const response = await apiService.post('/auth/login', { email, password });
      const { access_token } = response.data;

      localStorage.setItem('token', access_token);
      apiService.setAuthToken(access_token);

      // Get user info
      const userResponse = await apiService.get('/auth/me');

      dispatch({
        type: 'AUTH_SUCCESS',
        payload: { user: userResponse.data, token: access_token },
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Login failed';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  const register = async (userData: RegisterData) => {
    dispatch({ type: 'AUTH_START' });
    try {
      const response = await apiService.post('/auth/register', userData);
      console.log('Registration response:', response.data);
      dispatch({ type: 'AUTH_LOGOUT' }); // Don't auto-login after registration
    } catch (error: any) {
      console.error('Registration error:', error);
      console.error('Error response:', error.response?.data);
      const errorMessage = error.response?.data?.detail || 'Registration failed';
      dispatch({ type: 'AUTH_FAILURE', payload: errorMessage });
      throw error;
    }
  };

  const logout = () => {
    localStorage.removeItem('token');
    apiService.setAuthToken(null);
    dispatch({ type: 'AUTH_LOGOUT' });
  };

  const verifyEmail = async (token: string) => {
    try {
      await apiService.post('/auth/verify-email', { token });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Email verification failed';
      throw new Error(errorMessage);
    }
  };

  const resendVerification = async (email: string) => {
    try {
      await apiService.post('/auth/resend-verification', { email });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to resend verification email';
      throw new Error(errorMessage);
    }
  };

  const requestPasswordReset = async (email: string) => {
    try {
      await apiService.post('/auth/request-password-reset', { email });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Failed to request password reset';
      throw new Error(errorMessage);
    }
  };

  const resetPassword = async (token: string, newPassword: string) => {
    try {
      await apiService.post('/auth/reset-password', { token, new_password: newPassword });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Password reset failed';
      throw new Error(errorMessage);
    }
  };

  const changePassword = async (currentPassword: string, newPassword: string) => {
    try {
      await apiService.post('/auth/change-password', {
        current_password: currentPassword,
        new_password: newPassword,
      });
    } catch (error: any) {
      const errorMessage = error.response?.data?.detail || 'Password change failed';
      throw new Error(errorMessage);
    }
  };

  const clearError = () => {
    dispatch({ type: 'CLEAR_ERROR' });
  };

  const value: AuthContextType = {
    ...state,
    login,
    register,
    logout,
    verifyEmail,
    resendVerification,
    requestPasswordReset,
    resetPassword,
    changePassword,
    clearError,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

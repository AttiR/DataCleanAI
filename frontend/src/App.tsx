import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';

import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Layout from './components/Layout';
import Home from './pages/Home';
import Dashboard from './pages/Dashboard';
import DatasetUpload from './pages/DatasetUpload';
import DatasetList from './pages/DatasetList';
import DatasetDetail from './pages/DatasetDetail';
import Analysis from './pages/Analysis';
import Cleaning from './pages/Cleaning';
import Jobs from './pages/Jobs';
import Login from './pages/Login';
import Register from './pages/Register';
import VerifyEmail from './pages/VerifyEmail';

// Create a theme instance
const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h4: {
      fontWeight: 600,
    },
    h5: {
      fontWeight: 600,
    },
    h6: {
      fontWeight: 600,
    },
  },
  components: {
    MuiCard: {
      styleOverrides: {
        root: {
          boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
          borderRadius: 8,
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          textTransform: 'none',
          fontWeight: 500,
        },
      },
    },
  },
});

// Create a client
const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <Box sx={{ display: 'flex', minHeight: '100vh' }}>
              <Routes>
                {/* Public routes */}
                <Route path="/" element={<Home />} />
                <Route path="/login" element={<Login />} />
                <Route path="/register" element={<Register />} />
                <Route path="/verify-email" element={<VerifyEmail />} />

                {/* Protected routes */}
                <Route path="/dashboard" element={
                  <ProtectedRoute>
                    <Layout>
                      <Dashboard />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/upload" element={
                  <ProtectedRoute>
                    <Layout>
                      <DatasetUpload />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/datasets" element={
                  <ProtectedRoute>
                    <Layout>
                      <DatasetList />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/datasets/:id" element={
                  <ProtectedRoute>
                    <Layout>
                      <DatasetDetail />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/datasets/:id/analysis" element={
                  <ProtectedRoute>
                    <Layout>
                      <Analysis />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/datasets/:id/cleaning" element={
                  <ProtectedRoute>
                    <Layout>
                      <Cleaning />
                    </Layout>
                  </ProtectedRoute>
                } />
                <Route path="/jobs" element={
                  <ProtectedRoute>
                    <Layout>
                      <Jobs />
                    </Layout>
                  </ProtectedRoute>
                } />
              </Routes>
            </Box>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;

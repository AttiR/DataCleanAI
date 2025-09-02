import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { CssBaseline, Box } from '@mui/material';
import { QueryClient, QueryClientProvider } from 'react-query';

import Layout from './components/Layout';
import Dashboard from './pages/Dashboard';
import DatasetUpload from './pages/DatasetUpload';
import DatasetList from './pages/DatasetList';
import DatasetDetail from './pages/DatasetDetail';
import Analysis from './pages/Analysis';
import Cleaning from './pages/Cleaning';
import Jobs from './pages/Jobs';

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
        <Router>
          <Box sx={{ display: 'flex', minHeight: '100vh' }}>
            <Layout>
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/upload" element={<DatasetUpload />} />
                <Route path="/datasets" element={<DatasetList />} />
                <Route path="/datasets/:id" element={<DatasetDetail />} />
                <Route path="/datasets/:id/analysis" element={<Analysis />} />
                <Route path="/datasets/:id/cleaning" element={<Cleaning />} />
                <Route path="/jobs" element={<Jobs />} />
              </Routes>
            </Layout>
          </Box>
        </Router>
      </ThemeProvider>
    </QueryClientProvider>
  );
}

export default App;

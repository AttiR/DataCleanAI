import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Container,
  Paper,
  LinearProgress,
  Alert
} from '@mui/material';
import { Analytics as AnalyticsIcon } from '@mui/icons-material';
import { useMutation, useQuery } from 'react-query';
import { apiService } from '../services/apiService';

const Analysis: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const datasetId = parseInt(id || '0');
  const navigate = useNavigate();
  const [analysisStarted, setAnalysisStarted] = useState(false);

  const analyzeMutation = useMutation(() => apiService.analyzeDataset(datasetId), {
    onSuccess: () => {
      setAnalysisStarted(true);
    },
  });

  // Poll for analysis results when analysis is started
  const { data: analysisResponse, isLoading: isPolling } = useQuery(
    ['analysis', datasetId],
    () => apiService.getAnalysisResults(datasetId),
    {
      enabled: analysisStarted,
      refetchInterval: 2000, // Poll every 2 seconds
      refetchIntervalInBackground: false,
    }
  );

  const analysisData = analysisResponse?.data;

  // Redirect to dashboard when analysis is completed
  useEffect(() => {
    if (analysisData?.status === 'completed') {
      navigate('/dashboard');
    }
  }, [analysisData, navigate]);

  const handleAnalyze = () => {
    analyzeMutation.mutate();
  };

  return (
    <Container maxWidth="md">
      <Box sx={{
        minHeight: '80vh',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        py: 4
      }}>
        <Card sx={{
          width: '100%',
          maxWidth: 600,
          borderRadius: 3,
          overflow: 'hidden',
          position: 'relative',
          background: 'white',
          border: '1px solid rgba(0,0,0,0.05)',
          boxShadow: '0 8px 32px rgba(0,0,0,0.1)',
        }}>
          <Box sx={{
            background: 'linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #4ecdc4 100%)',
            color: 'white',
            p: 3,
            textAlign: 'center',
            position: 'relative',
            overflow: 'hidden',
            '&::before': {
              content: '""',
              position: 'absolute',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              background: 'linear-gradient(45deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%)',
              pointerEvents: 'none',
            }
          }}>
            <Box sx={{ position: 'relative', zIndex: 1 }}>
              <AnalyticsIcon sx={{ fontSize: 48, mb: 2 }} />
              <Typography variant="h4" component="h1" gutterBottom sx={{ fontWeight: 'bold' }}>
                Data Quality Analysis
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.95 }}>
                Ready to analyze your dataset with AI-powered quality insights
              </Typography>
            </Box>
          </Box>

          <CardContent sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="h6" gutterBottom sx={{ mb: 3, color: 'text.secondary' }}>
              Click the button below to start the comprehensive data quality analysis
            </Typography>

            <Box sx={{ mb: 3 }}>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                The analysis will include:
              </Typography>
              <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1, alignItems: 'center' }}>
                <Typography variant="body2" color="text.secondary">
                  • Missing data detection and patterns
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Duplicate identification and analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Outlier detection using statistical methods
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Data type consistency analysis
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Quality score calculation
                </Typography>
              </Box>
            </Box>

            {!analysisStarted ? (
              <Button
                variant="contained"
                size="large"
                startIcon={analyzeMutation.isLoading ? <CircularProgress size={20} color="inherit" /> : <AnalyticsIcon />}
                disabled={analyzeMutation.isLoading}
                onClick={handleAnalyze}
                sx={{
                  py: 2,
                  px: 6,
                  fontSize: '1.1rem',
                  fontWeight: 600,
                  borderRadius: 3,
                  background: 'linear-gradient(45deg, #ff6b35, #f7931e)',
                  color: 'white',
                  boxShadow: '0 8px 32px rgba(255, 107, 53, 0.3)',
                  '&:hover': {
                    background: 'linear-gradient(45deg, #e55a2b, #e8841a)',
                    boxShadow: '0 12px 40px rgba(255, 107, 53, 0.4)',
                    transform: 'translateY(-2px)',
                  },
                  transition: 'all 0.3s ease',
                  minWidth: 200,
                }}
              >
                {analyzeMutation.isLoading ? 'Starting Analysis...' : 'Start Analysis'}
              </Button>
            ) : (
              <Box sx={{ width: '100%', maxWidth: 400 }}>
                <Typography variant="h6" gutterBottom sx={{ mb: 2, color: '#ff6b35' }}>
                  Analysis in Progress...
                </Typography>
                <LinearProgress
                  sx={{
                    mb: 2,
                    height: 8,
                    borderRadius: 4,
                    backgroundColor: 'rgba(255, 107, 53, 0.2)',
                    '& .MuiLinearProgress-bar': {
                      backgroundColor: '#ff6b35',
                      borderRadius: 4,
                    }
                  }}
                />
                <Typography variant="body2" color="text.secondary">
                  Progress: {analysisData?.progress || 0}%
                </Typography>
                {analysisData?.message && (
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    {analysisData.message}
                  </Typography>
                )}
              </Box>
            )}
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};

export default Analysis;

import React from 'react';
import {
  Box,
  Container,
  Typography,
  Button,
  Grid,
  Card,
  CardContent,
  Fade,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Analytics as AnalyticsIcon,
  CleaningServices as CleaningIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const Home: React.FC = () => {
  const navigate = useNavigate();
  const { isAuthenticated } = useAuth();

  const features = [
    {
      icon: <UploadIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Easy Data Upload',
      description: 'Upload your datasets in CSV, Excel, or Parquet formats with drag-and-drop interface.',
    },
    {
      icon: <AnalyticsIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'AI-Powered Analysis',
      description: 'Get comprehensive data quality insights and statistical analysis automatically.',
    },
    {
      icon: <CleaningIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Smart Data Cleaning',
      description: 'Automatically detect and fix missing values, duplicates, and data inconsistencies.',
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Secure & Private',
      description: 'Your data is encrypted and secure. Only you can access your datasets.',
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Fast Processing',
      description: 'Process large datasets quickly with our optimized algorithms.',
    },
    {
      icon: <CheckIcon sx={{ fontSize: 40, color: 'primary.main' }} />,
      title: 'Quality Assurance',
      description: 'Ensure data quality with automated validation and quality scoring.',
    },
  ];

  const handleGetStarted = () => {
    if (isAuthenticated) {
      navigate('/');
    } else {
      navigate('/register');
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        padding: 0,
      }}
    >
      {/* Hero Section */}
      <Box
        sx={{
          background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
          color: 'white',
          py: 8,
        }}
      >
        <Container maxWidth="lg">
          <Fade in timeout={1000}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h2"
                component="h1"
                gutterBottom
                sx={{
                  fontWeight: 'bold',
                  mb: 3,
                  background: 'linear-gradient(45deg, #fff, #e3f2fd)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                }}
              >
                AutoDataFix
              </Typography>
              <Typography
                variant="h4"
                component="h2"
                gutterBottom
                sx={{ mb: 2, opacity: 0.9 }}
              >
                AI-Powered Data Quality System
              </Typography>
              <Typography
                variant="h6"
                sx={{ mb: 4, opacity: 0.8, maxWidth: '600px', mx: 'auto' }}
              >
                Transform your messy data into clean, analysis-ready datasets with our intelligent
                data cleaning and quality analysis tools.
              </Typography>
              <Box sx={{ display: 'flex', gap: 2, justifyContent: 'center', flexWrap: 'wrap' }}>
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGetStarted}
                  sx={{
                    py: 1.5,
                    px: 4,
                    fontSize: '1.1rem',
                    fontWeight: 600,
                    borderRadius: 2,
                    background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #1565c0, #1976d2)',
                    },
                  }}
                >
                  {isAuthenticated ? 'Go to Dashboard' : 'Get Started Free'}
                </Button>
                {!isAuthenticated && (
                  <Button
                    variant="outlined"
                    size="large"
                    onClick={() => navigate('/login')}
                    sx={{
                      py: 1.5,
                      px: 4,
                      fontSize: '1.1rem',
                      fontWeight: 600,
                      borderRadius: 2,
                      borderColor: 'white',
                      color: 'white',
                      '&:hover': {
                        borderColor: 'white',
                        backgroundColor: 'rgba(255, 255, 255, 0.1)',
                      },
                    }}
                  >
                    Sign In
                  </Button>
                )}
              </Box>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{ py: 8, backgroundColor: 'rgba(255, 255, 255, 0.95)' }}>
        <Container maxWidth="md">
          <Typography
            variant="h3"
            component="h2"
            textAlign="center"
            gutterBottom
            sx={{ mb: 6, fontWeight: 'bold', color: 'text.primary' }}
          >
            Why Choose AutoDataFix?
          </Typography>
          <Grid container spacing={3} justifyContent="center">
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index}>
                <Fade in timeout={1000 + index * 200}>
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      maxWidth: 320,
                      mx: 'auto',
                      transition: 'transform 0.3s ease-in-out, box-shadow 0.3s ease-in-out',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: '0 12px 24px rgba(0,0,0,0.15)',
                      },
                    }}
                  >
                    <CardContent sx={{ textAlign: 'center', p: 3, flexGrow: 1 }}>
                      <Box sx={{ mb: 2 }}>{feature.icon}</Box>
                      <Typography
                        variant="h6"
                        component="h3"
                        gutterBottom
                        sx={{ fontWeight: 'bold', color: 'text.primary', fontSize: '1.1rem' }}
                      >
                        {feature.title}
                      </Typography>
                      <Typography
                        variant="body2"
                        color="text.secondary"
                        sx={{ lineHeight: 1.6, fontSize: '0.9rem' }}
                      >
                        {feature.description}
                      </Typography>
                    </CardContent>
                  </Card>
                </Fade>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

      {/* CTA Section */}
      <Box
        sx={{
          py: 8,
          background: 'linear-gradient(135deg, #1976d2, #42a5f5)',
          color: 'white',
        }}
      >
        <Container maxWidth="md">
          <Fade in timeout={1500}>
            <Box sx={{ textAlign: 'center' }}>
              <Typography
                variant="h4"
                component="h2"
                gutterBottom
                sx={{ fontWeight: 'bold', mb: 2 }}
              >
                Ready to Clean Your Data?
              </Typography>
              <Typography
                variant="h6"
                sx={{ mb: 4, opacity: 0.9 }}
              >
                Experience the power of AI-driven data cleaning and analysis.
              </Typography>
              <Button
                variant="contained"
                size="large"
                onClick={handleGetStarted}
                sx={{
                  py: 2,
                  px: 6,
                  fontSize: '1.2rem',
                  fontWeight: 600,
                  borderRadius: 2,
                  background: 'white',
                  color: 'primary.main',
                  '&:hover': {
                    background: 'rgba(255, 255, 255, 0.9)',
                  },
                }}
              >
                {isAuthenticated ? 'Go to Dashboard' : 'Start Free Trial'}
              </Button>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Footer */}
      <Box
        sx={{
          py: 4,
          backgroundColor: 'rgba(0, 0, 0, 0.8)',
          color: 'white',
          textAlign: 'center',
        }}
      >
        <Container maxWidth="md">
          <Typography variant="body2" sx={{ opacity: 0.8 }}>
            © 2024 AutoDataFix. All rights reserved. Built with ❤️ for data professionals.
          </Typography>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;

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
  Chip,
  Stack,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Analytics as AnalyticsIcon,
  CleaningServices as CleaningIcon,
  Security as SecurityIcon,
  Speed as SpeedIcon,
  CheckCircle as CheckIcon,
  AutoFixHigh as AutoFixIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

const Home: React.FC = () => {
  const navigate = useNavigate();

  const features = [
    {
      icon: <UploadIcon sx={{ fontSize: 48, color: '#ff6b35' }} />,
      title: 'Easy Data Upload',
      description: 'Upload your datasets in CSV, Excel, or Parquet formats with our intuitive drag-and-drop interface.',
      color: '#ff6b35',
      bgColor: 'rgba(255, 107, 53, 0.1)',
    },
    {
      icon: <AnalyticsIcon sx={{ fontSize: 48, color: '#4ecdc4' }} />,
      title: 'AI-Powered Analysis',
      description: 'Get comprehensive data quality insights and statistical analysis powered by advanced machine learning.',
      color: '#4ecdc4',
      bgColor: 'rgba(78, 205, 196, 0.1)',
    },
    {
      icon: <CleaningIcon sx={{ fontSize: 48, color: '#ff6b35' }} />,
      title: 'Smart Data Cleaning',
      description: 'Automatically detect and fix missing values, duplicates, and data inconsistencies with AI precision.',
      color: '#ff6b35',
      bgColor: 'rgba(255, 107, 53, 0.1)',
    },
    {
      icon: <SecurityIcon sx={{ fontSize: 48, color: '#6c757d' }} />,
      title: 'Secure & Private',
      description: 'Your data is encrypted and secure. Advanced privacy protection ensures only you can access your datasets.',
      color: '#6c757d',
      bgColor: 'rgba(108, 117, 125, 0.1)',
    },
    {
      icon: <SpeedIcon sx={{ fontSize: 48, color: '#4ecdc4' }} />,
      title: 'Lightning Fast',
      description: 'Process large datasets in seconds with our optimized algorithms and cloud-powered infrastructure.',
      color: '#4ecdc4',
      bgColor: 'rgba(78, 205, 196, 0.1)',
    },
    {
      icon: <CheckIcon sx={{ fontSize: 48, color: '#ff6b35' }} />,
      title: 'Quality Assurance',
      description: 'Ensure data quality with automated validation, quality scoring, and comprehensive reporting.',
      color: '#ff6b35',
      bgColor: 'rgba(255, 107, 53, 0.1)',
    },
  ];


  const handleGetStarted = () => {
    navigate('/dashboard');
  };

  return (
    <Box
      sx={{
        background: 'linear-gradient(135deg, #ff6b35 0%, #f7931e 50%, #4ecdc4 100%)',
        padding: 0,
        position: 'relative',
      }}
    >
      {/* Animated Background Elements */}
      <Box
        sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          right: 0,
          bottom: 0,
          background: `
            radial-gradient(circle at 20% 80%, rgba(255, 107, 53, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 80% 20%, rgba(78, 205, 196, 0.3) 0%, transparent 50%),
            radial-gradient(circle at 40% 40%, rgba(108, 117, 125, 0.2) 0%, transparent 50%)
          `,
          animation: 'float 6s ease-in-out infinite',
          '@keyframes float': {
            '0%, 100%': { transform: 'translateY(0px)' },
            '50%': { transform: 'translateY(-20px)' },
          },
        }}
      />

      {/* Hero Section */}
      <Box
        sx={{
          position: 'relative',
          zIndex: 1,
          color: 'white',
          py: { xs: 6, md: 8 },
          px: 2,
          minHeight: '40vh',
        }}
      >
        <Container maxWidth="lg">
          <Fade in timeout={1000}>
            <Box sx={{ textAlign: 'center' }}>
              {/* Badge */}
              <Chip
                label="🚀 AI-Powered Data Platform"
                sx={{
                  mb: 3,
                  backgroundColor: 'rgba(255, 255, 255, 0.2)',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '0.9rem',
                  backdropFilter: 'blur(10px)',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                }}
              />

              <Typography
                variant="h1"
                component="h1"
                gutterBottom
                sx={{
                  fontWeight: 800,
                  mb: 2,
                  fontSize: { xs: '2rem', md: '3rem' },
                  background: 'linear-gradient(45deg, #fff, #f0f8ff)',
                  backgroundClip: 'text',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  textShadow: '0 4px 8px rgba(0,0,0,0.1)',
                }}
              >
                AutoDataFix
              </Typography>

              <Typography
                variant="h4"
                component="h2"
                gutterBottom
                sx={{
                  mb: 2,
                  opacity: 0.95,
                  fontSize: { xs: '1.2rem', md: '1.8rem' },
                  fontWeight: 600,
                }}
              >
                Transform Data Chaos into
                <Box component="span" sx={{ color: '#4ecdc4', ml: 1 }}>
                  Clean Insights
                </Box>
              </Typography>

              <Typography
                variant="h6"
                sx={{
                  mb: 4,
                  opacity: 0.9,
                  maxWidth: '600px',
                  mx: 'auto',
                  fontSize: { xs: '0.9rem', md: '1rem' },
                  lineHeight: 1.6,
                }}
              >
                The most advanced AI-powered data cleaning and quality analysis platform.
                Upload, analyze, and clean your datasets with professional-grade precision.
              </Typography>


              <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={3}
                justifyContent="center"
                alignItems="center"
              >
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGetStarted}
                  startIcon={<AutoFixIcon />}
                  sx={{
                    py: 2,
                    px: 6,
                    fontSize: '1.2rem',
                    fontWeight: 700,
                    borderRadius: 3,
                    background: 'linear-gradient(45deg, #ffffff, #f8f9fa)',
                    color: '#ff6b35',
                    boxShadow: '0 8px 32px rgba(255, 107, 53, 0.3)',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #f8f9fa, #e9ecef)',
                      boxShadow: '0 12px 40px rgba(255, 107, 53, 0.4)',
                      transform: 'translateY(-2px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Start Cleaning Data
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  sx={{
                    py: 2,
                    px: 6,
                    fontSize: '1.2rem',
                    fontWeight: 600,
                    borderRadius: 3,
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    color: 'white',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      transform: 'translateY(-2px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Watch Demo
                </Button>
              </Stack>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Features Section */}
      <Box sx={{
        py: { xs: 8, md: 12 },
        backgroundColor: '#f8f9fa',
        position: 'relative',
      }}>
        {/* Background Pattern */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `
              radial-gradient(circle at 10% 20%, rgba(255, 107, 53, 0.05) 0%, transparent 50%),
              radial-gradient(circle at 90% 80%, rgba(78, 205, 196, 0.05) 0%, transparent 50%)
            `,
          }}
        />

        <Container maxWidth="xl">
          <Box sx={{ textAlign: 'center', mb: 8 }}>
            <Chip
              label="✨ Features"
              sx={{
                mb: 2,
                backgroundColor: '#ff6b35',
                color: 'white',
                fontWeight: 600,
                fontSize: '0.9rem',
              }}
            />
            <Typography
              variant="h2"
              component="h2"
              gutterBottom
              sx={{
                mb: 2,
                fontWeight: 800,
                color: '#2c3e50',
                fontSize: { xs: '1.8rem', md: '2.5rem' },
              }}
            >
              Why Choose AutoDataFix?
            </Typography>
            <Typography
              variant="h6"
              sx={{
                color: '#6c757d',
                maxWidth: '600px',
                mx: 'auto',
                fontSize: { xs: '1rem', md: '1.1rem' },
                lineHeight: 1.6,
              }}
            >
              Powerful features designed to make data cleaning effortless and professional
            </Typography>
          </Box>

          <Grid container spacing={4} justifyContent="center">
            {features.map((feature, index) => (
              <Grid item xs={12} sm={6} md={4} key={index} sx={{ px: 0.5 }}>
                <Fade in timeout={1000 + index * 200}>
                  <Card
                    sx={{
                      height: '100%',
                      display: 'flex',
                      flexDirection: 'column',
                      borderRadius: 3,
                      overflow: 'hidden',
                      position: 'relative',
                      background: 'white',
                      border: '1px solid rgba(0,0,0,0.05)',
                      maxWidth: 350,
                      mx: 'auto',
                      transition: 'all 0.3s ease',
                      '&:hover': {
                        transform: 'translateY(-8px)',
                        boxShadow: '0 15px 30px rgba(0,0,0,0.1)',
                        '& .feature-icon': {
                          transform: 'scale(1.05)',
                        },
                        '& .feature-bg': {
                          opacity: 1,
                        },
                      },
                    }}
                  >
                    {/* Background Gradient */}
                    <Box
                      className="feature-bg"
                      sx={{
                        position: 'absolute',
                        top: 0,
                        left: 0,
                        right: 0,
                        bottom: 0,
                        background: `linear-gradient(135deg, ${feature.bgColor}, transparent)`,
                        opacity: 0,
                        transition: 'opacity 0.3s ease',
                      }}
                    />

                    <CardContent sx={{
                      p: 3,
                      flexGrow: 1,
                      position: 'relative',
                      zIndex: 1,
                    }}>
                      <Box
                        className="feature-icon"
                        sx={{
                          mb: 2,
                          display: 'flex',
                          justifyContent: 'center',
                          transition: 'transform 0.3s ease',
                        }}
                      >
                        <Box
                          sx={{
                            p: 1.5,
                            borderRadius: 2,
                            backgroundColor: feature.bgColor,
                            display: 'flex',
                            alignItems: 'center',
                            justifyContent: 'center',
                          }}
                        >
                          {feature.icon}
                        </Box>
                      </Box>

                      <Typography
                        variant="h6"
                        component="h3"
                        gutterBottom
                        sx={{
                          fontWeight: 700,
                          color: '#2c3e50',
                          mb: 1.5,
                          fontSize: '1.2rem',
                        }}
                      >
                        {feature.title}
                      </Typography>

                      <Typography
                        variant="body2"
                        sx={{
                          color: '#6c757d',
                          lineHeight: 1.6,
                          fontSize: '0.95rem',
                        }}
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
          py: { xs: 10, md: 16 },
          background: 'linear-gradient(135deg, #2c3e50 0%, #34495e 100%)',
          color: 'white',
          position: 'relative',
          overflow: 'hidden',
        }}
      >
        {/* Background Elements */}
        <Box
          sx={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: `
              radial-gradient(circle at 30% 70%, rgba(255, 107, 53, 0.1) 0%, transparent 50%),
              radial-gradient(circle at 70% 30%, rgba(78, 205, 196, 0.1) 0%, transparent 50%)
            `,
          }}
        />

        <Container maxWidth="lg">
          <Fade in timeout={1500}>
            <Box sx={{ textAlign: 'center', position: 'relative', zIndex: 1 }}>
              <Chip
                label="🚀 Ready to Transform Your Data?"
                sx={{
                  mb: 4,
                  backgroundColor: '#ff6b35',
                  color: 'white',
                  fontWeight: 600,
                  fontSize: '1rem',
                  py: 1,
                  px: 2,
                }}
              />

              <Typography
                variant="h1"
                component="h2"
                gutterBottom
                sx={{
                  fontWeight: 800,
                  mb: 4,
                  fontSize: { xs: '2.2rem', md: '3.5rem' },
                }}
              >
                Start Your Data Journey
                <Box component="span" sx={{ color: '#4ecdc4', ml: 1 }}>
                  Today
                </Box>
              </Typography>

              <Typography
                variant="h5"
                sx={{
                  mb: 6,
                  opacity: 0.9,
                  maxWidth: '700px',
                  mx: 'auto',
                  fontSize: { xs: '1.1rem', md: '1.4rem' },
                  lineHeight: 1.6,
                }}
              >
                Join data professionals who trust AutoDataFix for their data cleaning needs.
                Experience the power of AI-driven data transformation.
              </Typography>

              <Stack
                direction={{ xs: 'column', sm: 'row' }}
                spacing={3}
                justifyContent="center"
                alignItems="center"
              >
                <Button
                  variant="contained"
                  size="large"
                  onClick={handleGetStarted}
                  startIcon={<AutoFixIcon />}
                  sx={{
                    py: 3,
                    px: 10,
                    fontSize: '1.4rem',
                    fontWeight: 700,
                    borderRadius: 4,
                    background: 'linear-gradient(45deg, #ff6b35, #f7931e)',
                    color: 'white',
                    boxShadow: '0 8px 32px rgba(255, 107, 53, 0.4)',
                    '&:hover': {
                      background: 'linear-gradient(45deg, #e55a2b, #e8841a)',
                      boxShadow: '0 12px 40px rgba(255, 107, 53, 0.5)',
                      transform: 'translateY(-3px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  Get Started Free
                </Button>

                <Button
                  variant="outlined"
                  size="large"
                  sx={{
                    py: 3,
                    px: 10,
                    fontSize: '1.4rem',
                    fontWeight: 600,
                    borderRadius: 4,
                    borderColor: 'rgba(255, 255, 255, 0.8)',
                    color: 'white',
                    backgroundColor: 'rgba(255, 255, 255, 0.1)',
                    backdropFilter: 'blur(10px)',
                    '&:hover': {
                      borderColor: 'white',
                      backgroundColor: 'rgba(255, 255, 255, 0.2)',
                      transform: 'translateY(-3px)',
                    },
                    transition: 'all 0.3s ease',
                  }}
                >
                  View Pricing
                </Button>
              </Stack>
            </Box>
          </Fade>
        </Container>
      </Box>

      {/* Footer */}
      <Box
        sx={{
          py: 8,
          backgroundColor: '#1a1a1a',
          color: 'white',
          position: 'relative',
        }}
      >
        <Container maxWidth="lg">
          <Grid container spacing={4} alignItems="center">
            <Grid item xs={12} md={6}>
              <Typography variant="h6" sx={{ fontWeight: 700, mb: 2 }}>
                AutoDataFix
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.8, mb: 2 }}>
                The most advanced AI-powered data cleaning and quality analysis platform.
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.6 }}>
                © 2024 AutoDataFix. All rights reserved. Built with ❤️ for data professionals.
              </Typography>
            </Grid>
            <Grid item xs={12} md={6}>
              <Box sx={{ textAlign: { xs: 'left', md: 'right' } }}>
                <Typography variant="body2" sx={{ opacity: 0.8, mb: 1 }}>
                  Ready to transform your data?
                </Typography>
                <Button
                  variant="contained"
                  onClick={handleGetStarted}
                  sx={{
                    backgroundColor: '#ff6b35',
                    color: 'white',
                    fontWeight: 600,
                    '&:hover': {
                      backgroundColor: '#e55a2b',
                    },
                  }}
                >
                  Start Now
                </Button>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>
    </Box>
  );
};

export default Home;

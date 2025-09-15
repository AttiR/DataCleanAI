import React, { useState, useEffect } from 'react';
import {
  Box,
  CardContent,
  Button,
  Typography,
  Alert,
  Container,
  Paper,
  Fade,
  CircularProgress,
} from '@mui/material';
import {
  CheckCircle,
  Error,
  Email,
  Refresh,
  ArrowBack,
} from '@mui/icons-material';
import { useNavigate, Link as RouterLink, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

const VerifyEmail: React.FC = () => {
  const [searchParams] = useSearchParams();
  const [isVerifying, setIsVerifying] = useState(false);
  const [verificationStatus, setVerificationStatus] = useState<'pending' | 'success' | 'error'>('pending');
  const [message, setMessage] = useState('');
  const [email, setEmail] = useState('');

  const { verifyEmail, resendVerification } = useAuth();
  const navigate = useNavigate();

  const token = searchParams.get('token');

  useEffect(() => {
    if (token) {
      handleVerification(token);
    }
  }, [token]); // eslint-disable-line react-hooks/exhaustive-deps

  const handleVerification = async (verificationToken: string) => {
    setIsVerifying(true);
    try {
      await verifyEmail(verificationToken);
      setVerificationStatus('success');
      setMessage('Your email has been successfully verified! You can now sign in to your account.');
      // Extract email from token or use a placeholder
      setEmail('your-email@example.com');
    } catch (error: any) {
      setVerificationStatus('error');
      setMessage(error.message || 'Email verification failed. The token may be invalid or expired.');
    } finally {
      setIsVerifying(false);
    }
  };

  const handleResendVerification = async () => {
    if (!email) {
      setMessage('Please enter your email address to resend verification.');
      return;
    }

    try {
      await resendVerification(email);
      setMessage('Verification email sent successfully! Please check your inbox.');
    } catch (error: any) {
      setMessage(error.message || 'Failed to resend verification email.');
    }
  };

  const getStatusIcon = () => {
    switch (verificationStatus) {
      case 'success':
        return <CheckCircle sx={{ fontSize: 80, color: 'success.main' }} />;
      case 'error':
        return <Error sx={{ fontSize: 80, color: 'error.main' }} />;
      default:
        return <Email sx={{ fontSize: 80, color: 'primary.main' }} />;
    }
  };

  const getStatusColor = () => {
    switch (verificationStatus) {
      case 'success':
        return 'success';
      case 'error':
        return 'error';
      default:
        return 'info';
    }
  };

  return (
    <Box
      sx={{
        minHeight: '100vh',
        background: '#f8fafc',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: 4,
      }}
    >
      <Box
        sx={{
          width: '100%',
          maxWidth: 400,
          mx: 'auto',
        }}
      >
        <Fade in timeout={800}>
          <Paper
            elevation={8}
            sx={{
              borderRadius: 3,
              overflow: 'hidden',
              background: '#ffffff',
              border: '1px solid #e2e8f0',
            }}
          >
            <Box
              sx={{
                background: 'linear-gradient(135deg, #1976d2, #42a5f5)',
                color: 'white',
                padding: 4,
                textAlign: 'center',
              }}
            >
              <Typography variant="h4" component="h1" fontWeight="bold">
                Email Verification
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9, mt: 1 }}>
                Verify your email address to activate your account
              </Typography>
            </Box>

            <CardContent sx={{ padding: 4, textAlign: 'center' }}>
              {isVerifying ? (
                <Box sx={{ py: 4 }}>
                  <CircularProgress size={60} sx={{ mb: 2 }} />
                  <Typography variant="h6" gutterBottom>
                    Verifying your email...
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Please wait while we verify your email address.
                  </Typography>
                </Box>
              ) : (
                <Box sx={{ py: 2 }}>
                  {getStatusIcon()}

                  <Typography
                    variant="h5"
                    gutterBottom
                    sx={{
                      mt: 2,
                      color: verificationStatus === 'success' ? 'success.main' :
                             verificationStatus === 'error' ? 'error.main' : 'text.primary'
                    }}
                  >
                    {verificationStatus === 'success' && 'Verification Successful!'}
                    {verificationStatus === 'error' && 'Verification Failed'}
                    {verificationStatus === 'pending' && 'Check Your Email'}
                  </Typography>

                  <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
                    {message}
                  </Typography>

                  {verificationStatus === 'success' && (
                    <Box sx={{ mt: 3 }}>
                      <Button
                        component={RouterLink}
                        to="/login"
                        variant="contained"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                          mr: 2,
                        }}
                      >
                        Sign In Now
                      </Button>
                      <Button
                        component={RouterLink}
                        to="/"
                        variant="outlined"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                        }}
                      >
                        Go to Home
                      </Button>
                    </Box>
                  )}

                  {verificationStatus === 'error' && (
                    <Box sx={{ mt: 3 }}>
                      <Alert
                        severity="warning"
                        sx={{ mb: 3, textAlign: 'left' }}
                        action={
                          <Button
                            color="inherit"
                            size="small"
                            onClick={handleResendVerification}
                            startIcon={<Refresh />}
                          >
                            Resend
                          </Button>
                        }
                      >
                        The verification link may have expired. You can request a new verification email.
                      </Alert>

                      <Button
                        component={RouterLink}
                        to="/login"
                        variant="contained"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                          mr: 2,
                        }}
                      >
                        Back to Login
                      </Button>
                      <Button
                        component={RouterLink}
                        to="/register"
                        variant="outlined"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                        }}
                      >
                        Register Again
                      </Button>
                    </Box>
                  )}

                  {verificationStatus === 'pending' && !token && (
                    <Box sx={{ mt: 3 }}>
                      <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                        We've sent a verification email to your registered email address.
                        Please check your inbox and click the verification link.
                      </Typography>

                      <Button
                        component={RouterLink}
                        to="/login"
                        variant="contained"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                          mr: 2,
                        }}
                      >
                        Back to Login
                      </Button>
                      <Button
                        component={RouterLink}
                        to="/"
                        variant="outlined"
                        size="large"
                        sx={{
                          borderRadius: 2,
                          py: 1.5,
                          px: 4,
                          textTransform: 'none',
                          fontSize: '1rem',
                          fontWeight: 600,
                        }}
                      >
                        Go to Home
                      </Button>
                    </Box>
                  )}

                  <Box sx={{ textAlign: 'center', mt: 4 }}>
                    <Button
                      onClick={() => navigate('/')}
                      startIcon={<ArrowBack />}
                      sx={{
                        color: 'text.secondary',
                        textTransform: 'none',
                      }}
                    >
                      Back to Home
                    </Button>
                  </Box>
                </Box>
              )}
            </CardContent>
          </Paper>
        </Fade>
      </Box>
    </Box>
  );
};

export default VerifyEmail;

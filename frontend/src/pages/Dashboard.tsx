import React, { useState } from 'react';
import {
  Box,
  Grid,
  Card,
  CardContent,
  Typography,
  Button,
  LinearProgress,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  List,
  ListItem,
  ListItemText,
  Alert,
  Divider,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  DialogContentText,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  Storage as DatasetIcon,
  Analytics as AnalyticsIcon,
  CleaningServices as CleaningIcon,
  TrendingUp as TrendingUpIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon,
  ExpandMore as ExpandMoreIcon,
  Download as DownloadIcon,
  ErrorOutline as ErrorIcon,
  Info as InfoIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { apiService } from '../services/apiService';

const QualityInsights: React.FC<{ datasets: any[] }> = ({ datasets }) => {
  const [analysisData, setAnalysisData] = useState<any>(null);
  const [cleaningData, setCleaningData] = useState<any>(null);
  const [isCleaningInProgress, setIsCleaningInProgress] = useState(false);

  // Get latest analyzed dataset
  const latestDataset = datasets.find(d => d.status === 'analyzed' || d.status === 'cleaned');

  // Fetch analysis and cleaning results for the latest dataset
  React.useEffect(() => {
    if (latestDataset) {
      apiService.getAnalysisResults(latestDataset.id)
        .then(response => setAnalysisData(response.data))
        .catch(console.error);

      if (latestDataset.status === 'cleaned') {
        apiService.getCleaningResults(latestDataset.id)
          .then(response => setCleaningData(response.data))
          .catch(console.error);
      }
    }
  }, [latestDataset]);

  const downloadCleanedFile = async (datasetId: number, filename: string) => {
    try {
      const response = await apiService.downloadCleanedDataset(datasetId);
      const url = window.URL.createObjectURL(new Blob([response.data]));
      const link = document.createElement('a');
      link.href = url;
      link.setAttribute('download', `cleaned_${filename}`);
      document.body.appendChild(link);
      link.click();
      link.remove();
      window.URL.revokeObjectURL(url);
    } catch (error) {
      console.error('Download failed:', error);
    }
  };

  const handleCleanDataset = async (datasetId: number) => {
    try {
      setIsCleaningInProgress(true);
      await apiService.cleanDataset(datasetId);

      // Wait a bit and then refresh the data
      setTimeout(() => {
        window.location.reload();
      }, 3000);
    } catch (error) {
      console.error('Cleaning failed:', error);
      setIsCleaningInProgress(false);
    }
  };



  if (!latestDataset || !analysisData) {
    return null;
  }

  const qualityScore = analysisData.results?.quality_score || 0;
  const recommendations = analysisData.results?.recommendations || [];
  const missingData = analysisData.results?.missing_data;
  const outliers = analysisData.results?.outliers;
  const duplicates = analysisData.results?.duplicates;

  return (
    <Box sx={{ mb: 4 }}>
      <Card sx={{ border: '1px solid', borderColor: 'divider', boxShadow: '0 4px 12px rgba(0,0,0,0.05)' }}>
        <CardContent sx={{ p: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h5" sx={{ fontWeight: 600 }}>
              📊 Data Quality Insights - {latestDataset.filename}
            </Typography>
            {latestDataset.status === 'cleaned' && (
              <Button
                variant="contained"
                startIcon={<DownloadIcon />}
                onClick={() => downloadCleanedFile(latestDataset.id, latestDataset.filename)}
                sx={{
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  textTransform: 'none',
                  borderRadius: 2,
                  px: 3
                }}
              >
                Download Cleaned Data
              </Button>
            )}
          </Box>

          <Grid container spacing={3}>
            {/* Quality Score Card */}
            <Grid item xs={12} md={3}>
              <Card sx={{
                background: qualityScore >= 80 ? 'linear-gradient(135deg, #4CAF50, #45a049)' :
                           qualityScore >= 60 ? 'linear-gradient(135deg, #FF9800, #F57C00)' :
                           'linear-gradient(135deg, #F44336, #D32F2F)',
                color: 'white',
                textAlign: 'center',
                p: 2
              }}>
                <Typography variant="h3" sx={{ fontWeight: 700 }}>
                  {qualityScore.toFixed(1)}%
                </Typography>
                <Typography variant="body2" sx={{ opacity: 0.9 }}>
                  Quality Score
                </Typography>
              </Card>
            </Grid>

            {/* Issues Summary */}
            <Grid item xs={12} md={9}>
              <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2 }}>
                {missingData?.total_missing > 0 && (
                  <Chip
                    icon={<WarningIcon />}
                    label={`${missingData.total_missing} Missing Values`}
                    color="warning"
                    variant="outlined"
                  />
                )}
                {duplicates?.exact_duplicates > 0 && (
                  <Chip
                    icon={<ErrorIcon />}
                    label={`${duplicates.exact_duplicates} Duplicate Rows`}
                    color="error"
                    variant="outlined"
                  />
                )}
                {outliers?.combined?.total_outliers > 0 && (
                  <Chip
                    icon={<InfoIcon />}
                    label={`${outliers.combined.total_outliers} Outliers`}
                    color="info"
                    variant="outlined"
                  />
                )}
                {recommendations.length === 0 && (
                  <Chip
                    icon={<CheckCircleIcon />}
                    label="No Issues Found"
                    color="success"
                    variant="outlined"
                  />
                )}
              </Box>
            </Grid>
          </Grid>

          {/* Detailed Breakdown */}
          <Accordion sx={{ mt: 3, border: '1px solid', borderColor: 'divider' }}>
            <AccordionSummary expandIcon={<ExpandMoreIcon />}>
              <Typography variant="h6" sx={{ fontWeight: 600 }}>
                🔍 Why is Quality {qualityScore.toFixed(1)}%? (Click to see details)
              </Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={3}>
                {/* Issues Found */}
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: 'error.main' }}>
                    🚨 Issues Found:
                  </Typography>
                  {recommendations.length > 0 ? (
                    <List dense>
                      {recommendations.map((rec: string, index: number) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemText
                            primary={rec}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  ) : (
                    <Alert severity="success" sx={{ mt: 1 }}>
                      No data quality issues detected!
                    </Alert>
                  )}
                </Grid>

                {/* What Was Cleaned */}
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 2, color: 'success.main' }}>
                    ✅ What Was Cleaned:
                  </Typography>
                  {cleaningData?.results ? (
                    <List dense>
                      {cleaningData.results.cleaning_steps?.map((step: string, index: number) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemText
                            primary={step}
                            primaryTypographyProps={{ variant: 'body2' }}
                          />
                        </ListItem>
                      )) || []}
                      <ListItem sx={{ py: 0.5 }}>
                        <ListItemText
                          primary={`Rows processed: ${cleaningData.results.original_shape?.[0] || 0} → ${cleaningData.results.final_shape?.[0] || 0}`}
                          primaryTypographyProps={{ variant: 'body2', fontWeight: 600 }}
                        />
                      </ListItem>
                    </List>
                  ) : latestDataset.status === 'cleaned' ? (
                    <Alert severity="info" sx={{ mt: 1 }}>
                      Data has been cleaned. Download to see the results!
                    </Alert>
                  ) : (
                    <Alert severity="warning" sx={{ mt: 1 }}>
                      Data not yet cleaned. Click "Clean Data" to fix issues.
                    </Alert>
                  )}
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* Cleaning Actions */}
          {latestDataset.status === 'analyzed' && (
            <Box sx={{ mt: 3, p: 2, bgcolor: 'action.hover', borderRadius: 2 }}>
              <Typography variant="body2" sx={{ mb: 2 }}>
                💡 <strong>Next Step:</strong> Clean your data to improve quality score and fix detected issues.
              </Typography>
              <Button
                variant="contained"
                startIcon={<CleaningIcon />}
                disabled={isCleaningInProgress}
                sx={{
                  background: isCleaningInProgress
                    ? 'linear-gradient(135deg, #ccc, #999)'
                    : 'linear-gradient(135deg, #4CAF50, #45a049)',
                  textTransform: 'none',
                  borderRadius: 2
                }}
                onClick={() => handleCleanDataset(latestDataset.id)}
              >
                {isCleaningInProgress ? 'Cleaning in Progress...' : 'Clean This Dataset'}
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>
    </Box>
  );
};

const Dashboard: React.FC = () => {
  const navigate = useNavigate();
  const [clearDialogOpen, setClearDialogOpen] = useState(false);

  const { data: datasets, isLoading: datasetsLoading } = useQuery(
    'datasets',
    apiService.getDatasets
  );

  const { data: jobs, isLoading: jobsLoading } = useQuery(
    'jobs',
    apiService.getJobs
  );

  const getStats = () => {
    if (!datasets?.data?.datasets) return { total: 0, analyzed: 0, cleaned: 0, quality: 0 };

    const total = datasets.data.datasets.length;
    const analyzed = datasets.data.datasets.filter((d: any) => d.status === 'analyzed').length;
    const cleaned = datasets.data.datasets.filter((d: any) => d.status === 'cleaned').length;

    // Avoid NaN by checking if total is 0
    const avgQuality = total > 0
      ? datasets.data.datasets.reduce((acc: number, d: any) => acc + (d.quality_score || 0), 0) / total
      : 0;

    return { total, analyzed, cleaned, quality: avgQuality };
  };

  const getRecentJobs = () => {
    if (!jobs?.data?.jobs) return [];
    return jobs.data.jobs.slice(0, 5);
  };

  const stats = getStats();
  const recentJobs = getRecentJobs();

  const clearAllData = async () => {
    try {
      // Delete all datasets and jobs
      const response = await apiService.deleteAllDatasets();
      console.log('Clear result:', response.data);

      // Close dialog and refresh
      setClearDialogOpen(false);
      window.location.reload();
    } catch (error) {
      console.error('Failed to clear data:', error);
      alert('Failed to clear data. Please try again.');
    }
  };

    const StatCard: React.FC<{
    title: string;
    value: string | number;
    icon: React.ReactNode;
    color: string;
    subtitle?: string;
  }> = ({ title, value, icon, color, subtitle }) => (
    <Card
      sx={{
        height: '100%',
        background: `linear-gradient(135deg, ${color}15 0%, ${color}05 100%)`,
        border: `1px solid ${color}30`,
        transition: 'transform 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-2px)',
          boxShadow: 2
        }
      }}
    >
      <CardContent sx={{ height: '100%', display: 'flex', flexDirection: 'column', justifyContent: 'space-between' }}>
        <Box sx={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
          <Box sx={{ flex: 1 }}>
            <Typography variant="h4" component="div" sx={{ fontWeight: 'bold', color: color, mb: 1 }}>
              {typeof value === 'string' ? value : value.toLocaleString()}
            </Typography>
            <Typography variant="h6" sx={{ color: 'text.primary', mb: 0.5 }}>
              {title}
            </Typography>
            {subtitle && (
              <Typography variant="body2" color="text.secondary">
                {subtitle}
              </Typography>
            )}
          </Box>
          <Box
            sx={{
              backgroundColor: color,
              borderRadius: 2,
              p: 1.5,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              boxShadow: 1
            }}
          >
            <Box sx={{ color: 'white' }}>
              {icon}
            </Box>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );

  const JobCard: React.FC<{ job: any }> = ({ job }) => {
    const getStatusColor = (status: string) => {
      switch (status) {
        case 'completed':
          return 'success';
        case 'running':
          return 'primary';
        case 'failed':
          return 'error';
        default:
          return 'default';
      }
    };

    const getStatusIcon = (status: string): React.ReactElement | undefined => {
      switch (status) {
        case 'completed':
          return <CheckCircleIcon />;
        case 'running':
          return <TrendingUpIcon />;
        case 'failed':
          return <WarningIcon />;
        default:
          return undefined;
      }
    };

    return (
      <Card sx={{
        border: '1px solid',
        borderColor: 'divider',
        boxShadow: '0 2px 8px rgba(0,0,0,0.04)',
        transition: 'all 0.2s ease-in-out',
        '&:hover': {
          boxShadow: '0 4px 16px rgba(0,0,0,0.08)',
          transform: 'translateY(-1px)',
        }
      }}>
        <CardContent sx={{ p: 2.5 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
            <Box sx={{ flex: 1 }}>
              <Typography variant="subtitle1" sx={{ fontWeight: 600, mb: 0.5 }}>
                {job.job_type.charAt(0).toUpperCase() + job.job_type.slice(1)} Processing
              </Typography>
              <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                Dataset ID: {job.dataset_id}
              </Typography>
              <Typography variant="caption" color="text.secondary">
                {new Date(job.created_at).toLocaleDateString()} at {new Date(job.created_at).toLocaleTimeString()}
              </Typography>
            </Box>
            <Chip
              {...(getStatusIcon(job.status) && { icon: getStatusIcon(job.status) })}
              label={job.status.charAt(0).toUpperCase() + job.status.slice(1)}
              color={getStatusColor(job.status) as any}
              size="small"
              sx={{
                fontWeight: 500,
                borderRadius: 1.5,
                minWidth: 90
              }}
            />
          </Box>

          {job.status === 'running' && (
            <Box sx={{ mt: 2 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 1 }}>
                <Typography variant="caption" color="text.secondary">
                  Progress
                </Typography>
                <Typography variant="caption" sx={{ fontWeight: 600 }}>
                  {job.progress}%
                </Typography>
              </Box>
              <LinearProgress
                variant="determinate"
                value={job.progress}
                sx={{
                  height: 6,
                  borderRadius: 3,
                  backgroundColor: 'action.hover',
                  '& .MuiLinearProgress-bar': {
                    borderRadius: 3,
                  }
                }}
              />
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

    return (
    <Box sx={{
      p: { xs: 2, sm: 3, md: 4 },
      minHeight: 'calc(100vh - 64px)', // Account for AppBar height
      width: '100%',
      maxWidth: '100%'
    }}>
      {/* Header Section */}
      <Box sx={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        mb: 4
      }}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            Dashboard
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Monitor your data quality and processing status
          </Typography>
        </Box>
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            startIcon={<UploadIcon />}
            onClick={() => navigate('/upload')}
          >
            Upload Dataset
          </Button>
          {stats.total > 0 && (
            <Button
              variant="outlined"
              color="error"
              onClick={() => setClearDialogOpen(true)}
            >
              Clear All Data
            </Button>
          )}
        </Box>
      </Box>

      {/* Stats Cards */}
      <Grid container spacing={{ xs: 2, sm: 3, md: 4 }} sx={{ mb: 5, width: '100%' }}>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Total Datasets"
            value={stats.total}
            icon={<DatasetIcon fontSize="large" />}
            color="#1976d2"
            subtitle="Uploaded datasets"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Analyzed"
            value={stats.analyzed}
            icon={<AnalyticsIcon fontSize="large" />}
            color="#2e7d32"
            subtitle="Quality analyzed"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Cleaned"
            value={stats.cleaned}
            icon={<CleaningIcon fontSize="large" />}
            color="#ed6c02"
            subtitle="AI cleaned"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <StatCard
            title="Avg Quality"
            value={stats.total > 0 ? `${stats.quality.toFixed(1)}%` : "No Data"}
            icon={<TrendingUpIcon fontSize="large" />}
            color="#9c27b0"
            subtitle={stats.total > 0 ? "Data quality score" : "Upload data to see quality"}
          />
        </Grid>
      </Grid>

      {/* Quality Insights Section */}
      <QualityInsights datasets={datasets?.data?.datasets || []} />

      {/* Recent Activity Section */}
      <Grid container spacing={3}>
        <Grid item xs={12} lg={8}>
          <Card sx={{
            height: '100%',
            border: '1px solid',
            borderColor: 'divider',
            boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
          }}>
            <CardContent sx={{ p: 3 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
                <Typography variant="h5" sx={{ fontWeight: 600 }}>
                  Recent Processing Jobs
                </Typography>
                <Button
                  variant="outlined"
                  onClick={() => navigate('/jobs')}
                  sx={{
                    textTransform: 'none',
                    borderRadius: 2,
                    px: 2
                  }}
                >
                  View All Jobs
                </Button>
              </Box>

              {jobsLoading ? (
                <Box sx={{ py: 4 }}>
                  <LinearProgress sx={{ mb: 2 }} />
                  <Typography variant="body2" color="text.secondary" textAlign="center">
                    Loading recent jobs...
                  </Typography>
                </Box>
              ) : recentJobs.length > 0 ? (
                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  {recentJobs.map((job: any) => (
                    <JobCard key={job.id} job={job} />
                  ))}
                </Box>
              ) : (
                <Box sx={{
                  py: 6,
                  textAlign: 'center',
                  color: 'text.secondary'
                }}>
                  <DatasetIcon sx={{ fontSize: 48, mb: 2, opacity: 0.3 }} />
                  <Typography variant="h6" gutterBottom>
                    No recent jobs
                  </Typography>
                  <Typography variant="body2">
                    Upload a dataset to start processing
                  </Typography>
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} lg={4}>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 3 }}>
            {/* Quick Actions Card */}
            <Card sx={{
              border: '1px solid',
              borderColor: 'divider',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h5" sx={{ fontWeight: 600, mb: 3 }}>
                  Quick Actions
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Button
                    variant="outlined"
                    startIcon={<UploadIcon />}
                    onClick={() => navigate('/upload')}
                    sx={{
                      justifyContent: 'flex-start',
                      textTransform: 'none',
                      py: 1.5,
                      borderRadius: 2,
                    }}
                  >
                    Upload New Dataset
                  </Button>

                  <Button
                    variant="outlined"
                    startIcon={<DatasetIcon />}
                    onClick={() => navigate('/datasets')}
                    sx={{
                      justifyContent: 'flex-start',
                      textTransform: 'none',
                      py: 1.5,
                      borderRadius: 2,
                    }}
                  >
                    View All Datasets
                  </Button>

                  <Button
                    variant="outlined"
                    startIcon={<AnalyticsIcon />}
                    onClick={() => navigate('/datasets')}
                    sx={{
                      justifyContent: 'flex-start',
                      textTransform: 'none',
                      py: 1.5,
                      borderRadius: 2,
                    }}
                  >
                    Run Analysis
                  </Button>

                  <Button
                    variant="outlined"
                    startIcon={<CleaningIcon />}
                    onClick={() => navigate('/datasets')}
                    sx={{
                      justifyContent: 'flex-start',
                      textTransform: 'none',
                      py: 1.5,
                      borderRadius: 2,
                    }}
                  >
                    Clean Data
                  </Button>
                </Box>
              </CardContent>
            </Card>

            {/* System Status Card */}
            <Card sx={{
              border: '1px solid',
              borderColor: 'divider',
              boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
            }}>
              <CardContent sx={{ p: 3 }}>
                <Typography variant="h6" sx={{ fontWeight: 600, mb: 2 }}>
                  System Status
                </Typography>

                <Box sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body2">API Status</Typography>
                    <Chip
                      label="Online"
                      color="success"
                      size="small"
                      sx={{ borderRadius: 1.5 }}
                    />
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body2">Processing Queue</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {recentJobs.filter((job: any) => job.status === 'running').length} active
                    </Typography>
                  </Box>

                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <Typography variant="body2">Storage Used</Typography>
                    <Typography variant="body2" color="text.secondary">
                      {(stats.total * 2.5).toFixed(1)} MB
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Box>
        </Grid>
      </Grid>

      {/* Clear Data Confirmation Dialog */}
      <Dialog
        open={clearDialogOpen}
        onClose={() => setClearDialogOpen(false)}
        aria-labelledby="clear-dialog-title"
        aria-describedby="clear-dialog-description"
      >
        <DialogTitle id="clear-dialog-title">
          🗑️ Clear All Data
        </DialogTitle>
        <DialogContent>
          <DialogContentText id="clear-dialog-description">
            Are you sure you want to delete all datasets and processing jobs? This action cannot be undone.
            <br /><br />
            <strong>This will delete:</strong>
            <br />• {stats.total} dataset(s)
            <br />• All analysis and cleaning results
            <br />• All uploaded and cleaned files
          </DialogContentText>
        </DialogContent>
        <DialogActions>
          <Button
            onClick={() => setClearDialogOpen(false)}
            color="inherit"
            sx={{ textTransform: 'none' }}
          >
            Cancel
          </Button>
          <Button
            onClick={clearAllData}
            color="error"
            variant="contained"
            sx={{ textTransform: 'none' }}
          >
            Yes, Clear All Data
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Dashboard;

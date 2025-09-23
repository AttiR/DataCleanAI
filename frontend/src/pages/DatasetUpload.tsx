import React, { useState, useCallback } from 'react';
import {
  Box,
  Card,
  CardContent,
  Typography,
  Button,
  Alert,
  LinearProgress,
  Chip,
  Paper,
} from '@mui/material';
import {
  CloudUpload as UploadIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { useDropzone } from 'react-dropzone';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from 'react-query';
import { apiService } from '../services/apiService';

const DatasetUpload: React.FC = () => {
  const [uploadStatus, setUploadStatus] = useState<'idle' | 'uploading' | 'success' | 'error'>('idle');
  const [uploadMessage, setUploadMessage] = useState('');
  const [uploadedDataset, setUploadedDataset] = useState<any>(null);
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const uploadMutation = useMutation(apiService.uploadDataset, {
    onSuccess: (response) => {
      console.log('Upload success:', response);
      setUploadStatus('success');
      setUploadMessage('Dataset uploaded successfully!');
      setUploadedDataset(response.data);
      queryClient.invalidateQueries('datasets');
    },
    onError: (error: any) => {
      console.error('Upload error:', error);
      setUploadStatus('error');
      setUploadMessage(error.response?.data?.detail || error.message || 'Upload failed');
    },
  });

  const onDrop = useCallback((acceptedFiles: File[]) => {
    console.log('Files dropped:', acceptedFiles);
    if (acceptedFiles.length > 0) {
      const file = acceptedFiles[0];
      console.log('Uploading file:', file.name, 'Size:', file.size);
      setUploadStatus('uploading');
      setUploadMessage('Uploading dataset...');
      uploadMutation.mutate(file);
    }
  }, [uploadMutation]);

  const { getRootProps, getInputProps, isDragActive, acceptedFiles } = useDropzone({
    onDrop,
    accept: {
      'text/csv': ['.csv'],
      'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet': ['.xlsx'],
      'application/vnd.ms-excel': ['.xls'],
      'application/octet-stream': ['.parquet'],
    },
    multiple: false,
    maxSize: 100 * 1024 * 1024, // 100MB
  });

  const handleViewDataset = () => {
    if (uploadedDataset) {
      navigate(`/datasets/${uploadedDataset.dataset_id}`);
    }
  };

  const handleAnalyzeDataset = () => {
    if (uploadedDataset) {
      navigate(`/datasets/${uploadedDataset.dataset_id}/analysis`);
    }
  };

  const getFileIcon = (fileName: string) => {
    const extension = fileName.split('.').pop()?.toLowerCase();
    switch (extension) {
      case 'csv':
        return '📊';
      case 'xlsx':
      case 'xls':
        return '📈';
      case 'parquet':
        return '🗃️';
      default:
        return '📄';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  return (
    <Box>
      <Typography variant="h4" component="h1" gutterBottom>
        Upload Dataset
      </Typography>

      {uploadStatus === 'success' && uploadedDataset && (
        <Alert
          severity="success"
          action={
            <Box sx={{ display: 'flex', gap: 1 }}>
              <Button color="inherit" size="small" onClick={handleViewDataset}>
                View Dataset
              </Button>
              <Button color="inherit" size="small" onClick={handleAnalyzeDataset}>
                Analyze
              </Button>
            </Box>
          }
          sx={{ mb: 3 }}
        >
          <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
            Upload Successful!
          </Typography>
          <Typography variant="body2">
            Dataset: {uploadedDataset.filename} |
            Shape: {uploadedDataset.shape[0]} rows × {uploadedDataset.shape[1]} columns
          </Typography>
        </Alert>
      )}

      {uploadStatus === 'error' && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {uploadMessage}
        </Alert>
      )}

      <Card>
        <CardContent>
          <Paper
            {...getRootProps()}
            sx={{
              border: '2px dashed',
              borderColor: isDragActive ? '#ff6b35' : 'grey.300',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              backgroundColor: isDragActive ? 'rgba(255, 107, 53, 0.1)' : 'grey.50',
              transition: 'all 0.2s ease',
              '&:hover': {
                borderColor: '#ff6b35',
                backgroundColor: 'rgba(255, 107, 53, 0.1)',
              },
            }}
          >
            <input {...getInputProps()} />
            <UploadIcon sx={{ fontSize: 48, color: '#ff6b35', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {isDragActive ? 'Drop the file here' : 'Drag & drop a dataset file here'}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              or click to select a file
            </Typography>
            <Typography variant="caption" color="text.secondary">
              Supported formats: CSV, Excel (.xlsx, .xls), Parquet | Max size: 100MB
            </Typography>
          </Paper>

          {acceptedFiles.length > 0 && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="h6" gutterBottom>
                Selected File:
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 2 }}>
                <Typography variant="h4">
                  {getFileIcon(acceptedFiles[0].name)}
                </Typography>
                <Box>
                  <Typography variant="body1" sx={{ fontWeight: 'bold' }}>
                    {acceptedFiles[0].name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {formatFileSize(acceptedFiles[0].size)}
                  </Typography>
                </Box>
                <Chip
                  label={acceptedFiles[0].type || 'Unknown type'}
                  size="small"
                  sx={{ backgroundColor: '#ff6b35', color: 'white' }}
                />
              </Box>
            </Box>
          )}

          {uploadStatus === 'uploading' && (
            <Box sx={{ mt: 3 }}>
              <Typography variant="body2" gutterBottom>
                Uploading dataset...
              </Typography>
              <LinearProgress />
            </Box>
          )}

          {uploadStatus === 'success' && (
            <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
              <Button
                variant="contained"
                startIcon={<CheckCircleIcon />}
                onClick={handleViewDataset}
                sx={{
                  backgroundColor: '#ff6b35',
                  '&:hover': {
                    backgroundColor: '#e55a2b',
                  },
                }}
              >
                View Dataset
              </Button>
              <Button
                variant="outlined"
                onClick={handleAnalyzeDataset}
                sx={{
                  borderColor: '#ff6b35',
                  color: '#ff6b35',
                  '&:hover': {
                    borderColor: '#e55a2b',
                    backgroundColor: 'rgba(255, 107, 53, 0.1)',
                  },
                }}
              >
                Analyze Quality
              </Button>
              <Button
                variant="outlined"
                onClick={() => {
                  setUploadStatus('idle');
                  setUploadMessage('');
                  setUploadedDataset(null);
                }}
                sx={{
                  borderColor: '#4ecdc4',
                  color: '#4ecdc4',
                  '&:hover': {
                    borderColor: '#3bb5b0',
                    backgroundColor: 'rgba(78, 205, 196, 0.1)',
                  },
                }}
              >
                Upload Another
              </Button>
            </Box>
          )}
        </CardContent>
      </Card>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Upload Guidelines
          </Typography>
          <Box component="ul" sx={{ pl: 2 }}>
            <Typography component="li" variant="body2" sx={{ mb: 1 }}>
              Ensure your dataset has a header row with column names
            </Typography>
            <Typography component="li" variant="body2" sx={{ mb: 1 }}>
              Use consistent data formats within columns
            </Typography>
            <Typography component="li" variant="body2" sx={{ mb: 1 }}>
              Remove any sensitive or personal information before uploading
            </Typography>
            <Typography component="li" variant="body2" sx={{ mb: 1 }}>
              For large datasets, consider splitting into smaller files
            </Typography>
            <Typography component="li" variant="body2">
              Supported file formats: CSV, Excel (.xlsx, .xls), Parquet
            </Typography>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DatasetUpload;

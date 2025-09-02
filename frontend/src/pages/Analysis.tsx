import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';
import { useMutation } from 'react-query';
import { apiService } from '../services/apiService';

const Analysis: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const datasetId = parseInt(id || '0');

  const analyzeMutation = useMutation(() => apiService.analyzeDataset(datasetId));

  const handleAnalyze = () => {
    analyzeMutation.mutate();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Data Analysis
      </Typography>
      <Button variant="contained" onClick={handleAnalyze}>
        Start Analysis
      </Button>
    </Box>
  );
};

export default Analysis;

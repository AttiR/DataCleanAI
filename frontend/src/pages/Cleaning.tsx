import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Button } from '@mui/material';
import { useMutation } from 'react-query';
import { apiService } from '../services/apiService';

const Cleaning: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const datasetId = parseInt(id || '0');

  const cleanMutation = useMutation(() => apiService.cleanDataset(datasetId));

  const handleClean = () => {
    cleanMutation.mutate();
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Data Cleaning
      </Typography>
      <Button variant="contained" onClick={handleClean}>
        Start Cleaning
      </Button>
    </Box>
  );
};

export default Cleaning;

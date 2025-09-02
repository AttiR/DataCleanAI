import React from 'react';
import { useParams } from 'react-router-dom';
import { Box, Typography, Card, CardContent, Button } from '@mui/material';
import { useQuery } from 'react-query';
import { apiService } from '../services/apiService';

const DatasetDetail: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const datasetId = parseInt(id || '0');

  const { data: dataset, isLoading } = useQuery(
    ['dataset', datasetId],
    () => apiService.getDataset(datasetId)
  );

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  if (!dataset) {
    return <Typography>Dataset not found</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dataset Details
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="h6">{dataset?.data?.filename}</Typography>
          <Typography>Shape: {dataset?.data?.shape?.[0]} rows × {dataset?.data?.shape?.[1]} columns</Typography>
          <Typography>Quality Score: {dataset?.data?.quality_score}%</Typography>
          <Typography>Status: {dataset?.data?.status}</Typography>
        </CardContent>
      </Card>
    </Box>
  );
};

export default DatasetDetail;

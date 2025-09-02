import React from 'react';
import { Box, Typography } from '@mui/material';
import { useQuery } from 'react-query';
import { apiService } from '../services/apiService';

const Jobs: React.FC = () => {
  const { data: jobs, isLoading } = useQuery('jobs', apiService.getJobs);

  if (isLoading) {
    return <Typography>Loading...</Typography>;
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Processing Jobs
      </Typography>
      <Typography>Total jobs: {jobs?.data?.jobs?.length || 0}</Typography>
    </Box>
  );
};

export default Jobs;

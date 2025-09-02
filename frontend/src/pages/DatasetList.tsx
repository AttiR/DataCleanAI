import React from 'react';
import {
  Box,
  Typography,
  Button,
  Chip,
  IconButton,
  Tooltip,
  Alert,
} from '@mui/material';
import {
  DataGrid,
  GridColDef,
  GridActionsCellItem,
  GridValueGetterParams,
} from '@mui/x-data-grid';
import {
  Visibility as ViewIcon,
  Analytics as AnalyzeIcon,
  CleaningServices as CleanIcon,
  Delete as DeleteIcon,
  CloudUpload as UploadIcon,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';
import { useQuery, useMutation, useQueryClient } from 'react-query';
import { apiService } from '../services/apiService';

const DatasetList: React.FC = () => {
  const navigate = useNavigate();
  const queryClient = useQueryClient();

  const { data: datasets, isLoading, error } = useQuery('datasets', apiService.getDatasets);

  const deleteMutation = useMutation(apiService.deleteDataset, {
    onSuccess: () => {
      queryClient.invalidateQueries('datasets');
    },
  });

  const handleDelete = (id: number) => {
    if (window.confirm('Are you sure you want to delete this dataset?')) {
      deleteMutation.mutate(id);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'uploaded':
        return 'default';
      case 'analyzed':
        return 'primary';
      case 'cleaned':
        return 'success';
      case 'failed':
        return 'error';
      default:
        return 'default';
    }
  };

  const columns: GridColDef[] = [
    {
      field: 'filename',
      headerName: 'Dataset Name',
      flex: 1,
      minWidth: 200,
    },
    {
      field: 'file_type',
      headerName: 'Type',
      width: 100,
      renderCell: (params) => (
        <Chip
          label={params.value.toUpperCase()}
          size="small"
          color="primary"
          variant="outlined"
        />
      ),
    },
    {
      field: 'shape',
      headerName: 'Shape',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => {
        const shape = params.row.shape;
        return `${shape[0]} × ${shape[1]}`;
      },
    },
    {
      field: 'quality_score',
      headerName: 'Quality Score',
      width: 130,
      renderCell: (params) => {
        const score = params.value || 0;
        const color = score >= 80 ? 'success' : score >= 60 ? 'warning' : 'error';
        return (
          <Chip
            label={`${score.toFixed(1)}%`}
            color={color}
            size="small"
          />
        );
      },
    },
    {
      field: 'status',
      headerName: 'Status',
      width: 120,
      renderCell: (params) => (
        <Chip
          label={params.value}
          color={getStatusColor(params.value)}
          size="small"
        />
      ),
    },
    {
      field: 'created_at',
      headerName: 'Uploaded',
      width: 120,
      valueGetter: (params: GridValueGetterParams) => {
        return new Date(params.value).toLocaleDateString();
      },
    },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 200,
      getActions: (params) => [
        <GridActionsCellItem
          icon={<ViewIcon />}
          label="View"
          onClick={() => navigate(`/datasets/${params.id}`)}
        />,
        <GridActionsCellItem
          icon={<AnalyzeIcon />}
          label="Analyze"
          onClick={() => navigate(`/datasets/${params.id}/analysis`)}
        />,
        <GridActionsCellItem
          icon={<CleanIcon />}
          label="Clean"
          onClick={() => navigate(`/datasets/${params.id}/cleaning`)}
        />,
        <GridActionsCellItem
          icon={<DeleteIcon />}
          label="Delete"
          onClick={() => handleDelete(params.id as number)}
          sx={{ color: 'error.main' }}
        />,
      ],
    },
  ];

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        Failed to load datasets: {(error as any)?.message || 'Unknown error'}
      </Alert>
    );
  }

  return (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1">
          Datasets
        </Typography>
        <Button
          variant="contained"
          startIcon={<UploadIcon />}
          onClick={() => navigate('/upload')}
        >
          Upload Dataset
        </Button>
      </Box>

      <Box sx={{ height: 600, width: '100%' }}>
        <DataGrid
          rows={datasets?.data?.datasets || []}
          columns={columns}
          loading={isLoading}
          pageSizeOptions={[10, 25, 50]}
          initialState={{
            pagination: {
              paginationModel: { page: 0, pageSize: 25 },
            },
          }}
          disableRowSelectionOnClick
          sx={{
            '& .MuiDataGrid-cell:focus': {
              outline: 'none',
            },
          }}
        />
      </Box>
    </Box>
  );
};

export default DatasetList;

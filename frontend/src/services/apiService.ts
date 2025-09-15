import axios, { AxiosInstance } from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000/api/v1';

// Extend AxiosInstance to include setAuthToken method
interface ExtendedAxiosInstance extends AxiosInstance {
  setAuthToken: (token: string | null) => void;
}

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
}) as ExtendedAxiosInstance;

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add auth token if available
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle 401 errors (unauthorized)
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }

    console.error('API Error:', error);
    console.error('Error details:', {
      message: error.message,
      code: error.code,
      config: error.config,
      response: error.response
    });
    return Promise.reject(error);
  }
);

// Add method to set auth token
api.setAuthToken = (token: string | null) => {
  if (token) {
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
  } else {
    delete api.defaults.headers.common['Authorization'];
  }
};

export const apiService = {
  // Generic HTTP methods
  get: (url: string) => api.get(url),
  post: (url: string, data?: any) => api.post(url, data),
  put: (url: string, data?: any) => api.put(url, data),
  delete: (url: string) => api.delete(url),

  // Set auth token
  setAuthToken: (token: string | null) => api.setAuthToken(token),

  // Dataset endpoints
  getDatasets: () => api.get('/datasets'),
  getDataset: (id: number) => api.get(`/datasets/${id}`),
  uploadDataset: (file: File) => {
    const formData = new FormData();
    formData.append('file', file);
    return api.post('/datasets/upload', formData, {
      headers: {
        'Content-Type': 'multipart/form-data',
      },
    });
  },
  deleteDataset: (id: number) => api.delete(`/datasets/${id}`),
  deleteAllDatasets: () => api.delete('/datasets'),

  // Analysis endpoints
  analyzeDataset: (id: number) => api.post(`/analysis/${id}/analyze`),
  getAnalysisResults: (id: number) => api.get(`/analysis/${id}/analysis`),
  analyzeDatasetSync: (id: number) => api.post(`/analysis/${id}/analyze/sync`),
  getAnalysisVisualizations: (id: number) => api.get(`/analysis/${id}/analysis/visualizations`),
  getAnalysisRecommendations: (id: number) => api.get(`/analysis/${id}/analysis/recommendations`),

  // Cleaning endpoints
  cleanDataset: (id: number) => api.post(`/cleaning/${id}/clean`),
  getCleaningResults: (id: number) => api.get(`/cleaning/${id}/cleaning`),
  cleanDatasetSync: (id: number) => api.post(`/cleaning/${id}/clean/sync`),
  getCleaningSummary: (id: number) => api.get(`/cleaning/${id}/cleaning/summary`),

  // Jobs endpoints
  getJobs: () => api.get('/jobs'),
  getJob: (id: number) => api.get(`/jobs/${id}`),
  getDatasetJobs: (id: number) => api.get(`/jobs/dataset/${id}`),
  cancelJob: (id: number) => api.delete(`/jobs/${id}`),

  // Download endpoints
  downloadCleanedDataset: (id: number) => api.get(`/datasets/${id}/download`, {
    responseType: 'blob',
  }),
};

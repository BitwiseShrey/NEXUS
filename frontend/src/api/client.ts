import axios from 'axios';

// When running with Vite proxy, empty string calls /api/v1 directly; or falls back to http://127.0.0.1:8000
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || '';

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const errorMsg =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected network error occurred';
    console.error(`[NEXUS API Error] ${error.config?.url}:`, errorMsg);
    return Promise.reject(error);
  }
);

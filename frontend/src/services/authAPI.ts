import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://127.0.0.1:8000';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add request interceptor to include auth token
api.interceptors.request.use(
  (config) => {
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

// Add response interceptor to handle auth errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

export const authAPI = {
  // Login user
  login: async (credentials: { username: string; password: string }) => {
    const response = await api.post('/users/login/', credentials);
    return response.data;
  },

  // Register user
  register: async (userData: {
    username: string;
    email: string;
    password: string;
    password_confirm: string;
    first_name: string;
    last_name: string;
    role: string;
    organization: string;
    badge_number: string;
  }) => {
    const response = await api.post('/users/register/', userData);
    return response.data;
  },

  // Logout user
  logout: async () => {
    const response = await api.post('/users/logout/');
    return response.data;
  },

  // Get current user info
  getCurrentUser: async () => {
    const response = await api.get('/users/me/');
    return response.data;
  },

  // Change password
  changePassword: async (passwordData: {
    old_password: string;
    new_password: string;
    new_password_confirm: string;
  }) => {
    const response = await api.post('/users/change_password/', passwordData);
    return response.data;
  },

  // Refresh token
  refreshToken: async (refresh: string) => {
    const response = await api.post('/users/refresh/', { refresh });
    return response.data;
  },
};

export default api;

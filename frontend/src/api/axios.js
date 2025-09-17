import axios from 'axios';
import { useAuthStore } from '../stores/auth';

const instance = axios.create({
  baseURL: 'http://localhost:8000', // Your backend API base URL
  timeout: 5000, // Request timeout
});

// Request interceptor to add the auth token
instance.interceptors.request.use(
  (config) => {
    const authStore = useAuthStore();
    if (authStore.token) {
      config.headers.Authorization = `Bearer ${authStore.token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle token expiration or invalid tokens
instance.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    const authStore = useAuthStore();
    if (error.response && error.response.status === 401) {
      // Token expired or invalid, log out the user
      authStore.logout();
      // Optionally redirect to login page
      // router.push('/login');
    }
    return Promise.reject(error);
  }
);

export default instance;

// (C) 2025 by OPNLAB Development. All rights reserved.
import { defineStore } from 'pinia';
import axios from '../api/axios';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        const response = await axios.post('/token', new URLSearchParams({
          username: username,
          password: password,
        }));
        this.token = response.data.access_token;
        localStorage.setItem('token', this.token);
        return true;
      } catch (error) {
        console.error('Login failed:', error);
        this.token = null;
        localStorage.removeItem('token');
        return false;
      }
    },
    logout() {
      this.token = null;
      localStorage.removeItem('token');
    },
  },
});

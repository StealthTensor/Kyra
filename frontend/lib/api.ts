import axios from 'axios';
import { useAuthStore } from '@/store/useAuthStore';

// In production, use env var. For MVP, hardcode localhost to avoid config drift.
const BASE_URL = 'http://localhost:8000/api/v1';

export const api = axios.create({
    baseURL: BASE_URL,
    headers: {
        'Content-Type': 'application/json',
    },
});

// Request interceptor to add token
api.interceptors.request.use(
    (config) => {
        // Read directly from store state (zustand persist works with localStorage)
        // But we can also access the store instance directly if needed.
        // However, react hooks rules apply. 
        // Best way in non-component files is accessing the store's getState().

        const state = useAuthStore.getState();
        const token = state.token;

        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// Response interceptor to handle 401
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            useAuthStore.getState().logout();
            if (typeof window !== 'undefined') {
                window.location.href = '/auth/login';
            }
        }
        return Promise.reject(error);
    }
);

export const isMockAPI = import.meta.env.VITE_USE_MOCK_API === 'true';
export const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'https://placement-os-backend-uc.a.run.app';

// Utility to simulate network delay for mock promises
export const delay = (ms: number = 800) => new Promise(resolve => setTimeout(resolve, ms));


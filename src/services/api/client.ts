export const isMockAPI = import.meta.env.VITE_USE_MOCK_API === 'true';

// Utility to simulate network delay for mock promises
export const delay = (ms: number = 800) => new Promise(resolve => setTimeout(resolve, ms));

/**
 * API Configuration
 * Centralized configuration for API base URL
 * Reads from environment variable VITE_API_BASE_URL
 */
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8001';

export default {
  baseURL: API_BASE_URL,
  // Helper function to build full API URLs
  url(path) {
    // Remove leading slash if present to avoid double slashes
    const cleanPath = path.startsWith('/') ? path.slice(1) : path;
    return `${API_BASE_URL}/${cleanPath}`;
  }
};


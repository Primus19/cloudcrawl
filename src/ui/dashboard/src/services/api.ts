/**
 * Base API service for making HTTP requests
 */

const API_BASE_URL = '/api/v1';

/**
 * Generic fetch wrapper with error handling
 */
export const fetchApi = async (endpoint: string, options: RequestInit = {}) => {
  try {
    // Get token from localStorage
    const token = localStorage.getItem('auth_token');
    
    // Set default headers
    const headers = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...(options.headers || {})
    };
    
    // Merge options
    const mergedOptions = {
      ...options,
      headers
    };
    
    // Make the request
    const response = await fetch(`${API_BASE_URL}${endpoint}`, mergedOptions);
    
    // Check if response is JSON
    const contentType = response.headers.get('content-type');
    if (contentType && contentType.includes('application/json')) {
      const data = await response.json();
      
      // Check if response is ok
      if (!response.ok) {
        throw new Error(data.error || 'An error occurred');
      }
      
      return data;
    } else {
      // Handle non-JSON responses
      const text = await response.text();
      if (!response.ok) {
        throw new Error(`Server returned ${response.status}: ${text}`);
      }
      return text;
    }
  } catch (error) {
    console.error('API request failed:', error);
    throw error;
  }
};

/**
 * HTTP GET request
 */
export const get = (endpoint: string, options: RequestInit = {}) => {
  return fetchApi(endpoint, {
    method: 'GET',
    ...options
  });
};

/**
 * HTTP POST request
 */
export const post = (endpoint: string, data: any, options: RequestInit = {}) => {
  return fetchApi(endpoint, {
    method: 'POST',
    body: JSON.stringify(data),
    ...options
  });
};

/**
 * HTTP PUT request
 */
export const put = (endpoint: string, data: any, options: RequestInit = {}) => {
  return fetchApi(endpoint, {
    method: 'PUT',
    body: JSON.stringify(data),
    ...options
  });
};

/**
 * HTTP DELETE request
 */
export const del = (endpoint: string, options: RequestInit = {}) => {
  return fetchApi(endpoint, {
    method: 'DELETE',
    ...options
  });
};

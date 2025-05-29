/**
 * Authentication Service
 * Handles user authentication API calls
 */

import { post, get } from './api';

// API endpoints
const AUTH_ENDPOINT = '/auth';

/**
 * Login user
 */
export const login = async (username: string, password: string) => {
  return post(`${AUTH_ENDPOINT}/login`, { username, password });
};

/**
 * Logout user
 */
export const logout = async () => {
  return post(`${AUTH_ENDPOINT}/logout`, {});
};

/**
 * Get current user information
 */
export const getCurrentUser = async () => {
  return get(`${AUTH_ENDPOINT}/me`);
};

/**
 * Register a new user
 */
export const register = async (userData: {
  username: string;
  email: string;
  password: string;
  full_name: string;
}) => {
  return post(`${AUTH_ENDPOINT}/register`, userData);
};

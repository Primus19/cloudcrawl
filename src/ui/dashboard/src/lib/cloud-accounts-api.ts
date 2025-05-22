/**
 * API service for managing cloud accounts
 */
import { CloudAccount, ApiResponse } from './types';

// Base API URL - would be configured based on environment in a real app
const API_BASE_URL = '/api/v1';

// Helper function for API requests
async function apiRequest<T>(
  endpoint: string, 
  method: 'GET' | 'POST' | 'PUT' | 'DELETE' = 'GET',
  data?: any
): Promise<ApiResponse<T>> {
  try {
    const options: RequestInit = {
      method,
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
    };

    if (data) {
      options.body = JSON.stringify(data);
    }

    const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
    const responseData = await response.json();

    if (!response.ok) {
      return {
        success: false,
        error: responseData.error || `API error: ${response.status}`,
        message: responseData.message || 'An error occurred while processing your request'
      };
    }

    return {
      success: true,
      data: responseData.data,
      message: responseData.message
    };
  } catch (error) {
    console.error('API request failed:', error);
    return {
      success: false,
      error: error instanceof Error ? error.message : 'Unknown error',
      message: 'Failed to communicate with the server'
    };
  }
}

// Cloud Accounts API
export async function getCloudAccounts(): Promise<ApiResponse<CloudAccount[]>> {
  return apiRequest<CloudAccount[]>('/accounts');
}

export async function getCloudAccount(accountId: string): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>(`/accounts/${accountId}`);
}

export async function createCloudAccount(account: any): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>('/accounts', 'POST', account);
}

export async function updateCloudAccount(accountId: string, updates: any): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>(`/accounts/${accountId}`, 'PUT', updates);
}

export async function deleteCloudAccount(accountId: string): Promise<ApiResponse<void>> {
  return apiRequest<void>(`/accounts/${accountId}`, 'DELETE');
}

export async function validateCloudAccount(account: any): Promise<ApiResponse<{ valid: boolean }>> {
  return apiRequest<{ valid: boolean }>('/accounts/validate', 'POST', account);
}

export async function syncCloudAccount(accountId: string): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>(`/accounts/${accountId}/sync`, 'POST');
}

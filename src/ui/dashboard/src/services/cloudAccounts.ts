/**
 * Cloud Accounts API service
 * Handles all API calls related to cloud provider accounts
 */

import { get, post, put, del } from './api';

// Types
export interface CloudAccount {
  id: string;
  name: string;
  provider: string;
  status: string;
  [key: string]: any; // Additional provider-specific fields
}

export interface AWSAccount extends CloudAccount {
  account_id: string;
  access_key: string;
  secret_key: string;
  regions: string[];
}

export interface AzureAccount extends CloudAccount {
  subscription_id: string;
  tenant_id: string;
}

export interface GCPAccount extends CloudAccount {
  project_id: string;
}

// API endpoints
const CLOUD_ACCOUNTS_ENDPOINT = '/cloud-accounts';

/**
 * Get all cloud accounts
 */
export const getAllCloudAccounts = async () => {
  return get(CLOUD_ACCOUNTS_ENDPOINT);
};

/**
 * Get cloud accounts by provider
 */
export const getCloudAccountsByProvider = async (provider: string) => {
  return get(`${CLOUD_ACCOUNTS_ENDPOINT}/${provider}`);
};

/**
 * Get a specific cloud account
 */
export const getCloudAccount = async (provider: string, accountId: string) => {
  return get(`${CLOUD_ACCOUNTS_ENDPOINT}/${provider}/${accountId}`);
};

/**
 * Add a new AWS account
 */
export const addAWSAccount = async (account: Omit<AWSAccount, 'id' | 'provider' | 'status'>) => {
  return post(`${CLOUD_ACCOUNTS_ENDPOINT}/aws`, {
    name: account.name,
    account_id: account.account_id,
    access_key: account.access_key,
    secret_key: account.secret_key,
    regions: account.regions || ['us-east-1']
  });
};

/**
 * Add a new Azure account
 */
export const addAzureAccount = async (account: Omit<AzureAccount, 'id' | 'provider' | 'status'>) => {
  return post(`${CLOUD_ACCOUNTS_ENDPOINT}/azure`, {
    name: account.name,
    subscription_id: account.subscription_id,
    tenant_id: account.tenant_id
  });
};

/**
 * Add a new GCP account
 */
export const addGCPAccount = async (account: Omit<GCPAccount, 'id' | 'provider' | 'status'>) => {
  return post(`${CLOUD_ACCOUNTS_ENDPOINT}/gcp`, {
    name: account.name,
    project_id: account.project_id
  });
};

/**
 * Update a cloud account
 */
export const updateCloudAccount = async (provider: string, accountId: string, updates: Partial<CloudAccount>) => {
  return put(`${CLOUD_ACCOUNTS_ENDPOINT}/${provider}/${accountId}`, updates);
};

/**
 * Delete a cloud account
 */
export const deleteCloudAccount = async (provider: string, accountId: string) => {
  return del(`${CLOUD_ACCOUNTS_ENDPOINT}/${provider}/${accountId}`);
};

/**
 * Get cost data for a cloud account
 */
export const getCloudAccountCosts = async (provider: string, accountId: string) => {
  return get(`${CLOUD_ACCOUNTS_ENDPOINT}/${provider}/${accountId}/costs`);
};

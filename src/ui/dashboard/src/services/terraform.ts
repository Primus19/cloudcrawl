/**
 * Terraform API service
 * Handles all API calls related to Terraform templates and deployments
 */

import { get, post, put, del } from './api';

// Types
export interface TerraformTemplate {
  id: string;
  name: string;
  description: string;
  provider: string;
  category: string;
  variables: TerraformVariable[];
  content: string;
  created_at: string;
  updated_at: string;
}

export interface TerraformVariable {
  name: string;
  description: string;
  type: string;
  default?: string;
  required: boolean;
}

export interface TerraformDeployment {
  id: string;
  template_id: string;
  name: string;
  status: 'planning' | 'applying' | 'completed' | 'failed' | 'destroyed';
  variables: Record<string, string>;
  outputs: Record<string, string>;
  created_at: string;
  updated_at: string;
}

// API endpoints
const TERRAFORM_ENDPOINT = '/terraform';

/**
 * Get all Terraform templates
 */
export const getAllTemplates = async () => {
  return get(`${TERRAFORM_ENDPOINT}/templates`);
};

/**
 * Get a specific Terraform template
 */
export const getTemplate = async (templateId: string) => {
  return get(`${TERRAFORM_ENDPOINT}/templates/${templateId}`);
};

/**
 * Create a new Terraform template
 */
export const createTemplate = async (template: Omit<TerraformTemplate, 'id' | 'created_at' | 'updated_at'>) => {
  return post(`${TERRAFORM_ENDPOINT}/templates`, template);
};

/**
 * Update a Terraform template
 */
export const updateTemplate = async (templateId: string, updates: Partial<TerraformTemplate>) => {
  return put(`${TERRAFORM_ENDPOINT}/templates/${templateId}`, updates);
};

/**
 * Delete a Terraform template
 */
export const deleteTemplate = async (templateId: string) => {
  return del(`${TERRAFORM_ENDPOINT}/templates/${templateId}`);
};

/**
 * Get all Terraform deployments
 */
export const getAllDeployments = async () => {
  return get(`${TERRAFORM_ENDPOINT}/deployments`);
};

/**
 * Get a specific Terraform deployment
 */
export const getDeployment = async (deploymentId: string) => {
  return get(`${TERRAFORM_ENDPOINT}/deployments/${deploymentId}`);
};

/**
 * Create a new Terraform deployment
 */
export const createDeployment = async (deployment: {
  template_id: string;
  name: string;
  variables: Record<string, string>;
}) => {
  return post(`${TERRAFORM_ENDPOINT}/deployments`, deployment);
};

/**
 * Apply a Terraform deployment
 */
export const applyDeployment = async (deploymentId: string) => {
  return post(`${TERRAFORM_ENDPOINT}/deployments/${deploymentId}/apply`, {});
};

/**
 * Destroy a Terraform deployment
 */
export const destroyDeployment = async (deploymentId: string) => {
  return post(`${TERRAFORM_ENDPOINT}/deployments/${deploymentId}/destroy`, {});
};

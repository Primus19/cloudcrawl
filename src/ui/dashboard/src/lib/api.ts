/**
 * API service for interacting with the Cloud Cost Optimizer backend
 */
import { 
  CloudAccount, 
  CloudResource, 
  Recommendation, 
  Action, 
  Workflow,
  CostData,
  CostBreakdown,
  CostTrend,
  ResourceFilter,
  CostFilter,
  RecommendationFilter,
  ActionFilter,
  ApiResponse,
  TerraformTemplate,
  TerraformDeployment
} from './types';

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

// Cloud Accounts
export async function getCloudAccounts(): Promise<ApiResponse<CloudAccount[]>> {
  return apiRequest<CloudAccount[]>('/accounts');
}

export async function getCloudAccount(accountId: string): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>(`/accounts/${accountId}`);
}

export async function createCloudAccount(account: Partial<CloudAccount>): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>('/accounts', 'POST', account);
}

export async function updateCloudAccount(accountId: string, updates: Partial<CloudAccount>): Promise<ApiResponse<CloudAccount>> {
  return apiRequest<CloudAccount>(`/accounts/${accountId}`, 'PUT', updates);
}

export async function deleteCloudAccount(accountId: string): Promise<ApiResponse<void>> {
  return apiRequest<void>(`/accounts/${accountId}`, 'DELETE');
}

// Resources
export async function getResources(accountId: string, filters?: ResourceFilter): Promise<ApiResponse<CloudResource[]>> {
  const queryParams = new URLSearchParams();
  
  if (filters) {
    if (filters.providers && filters.providers.length > 0) {
      queryParams.append('providers', filters.providers.join(','));
    }
    if (filters.regions && filters.regions.length > 0) {
      queryParams.append('regions', filters.regions.join(','));
    }
    if (filters.types && filters.types.length > 0) {
      queryParams.append('types', filters.types.join(','));
    }
    if (filters.status && filters.status.length > 0) {
      queryParams.append('status', filters.status.join(','));
    }
    if (filters.search) {
      queryParams.append('search', filters.search);
    }
    if (filters.tags) {
      Object.entries(filters.tags).forEach(([key, value]) => {
        queryParams.append(`tag:${key}`, value);
      });
    }
  }

  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return apiRequest<CloudResource[]>(`/accounts/${accountId}/resources${queryString}`);
}

export async function getResource(accountId: string, resourceId: string): Promise<ApiResponse<CloudResource>> {
  return apiRequest<CloudResource>(`/accounts/${accountId}/resources/${resourceId}`);
}

// Cost Data
export async function getCostSummary(accountId: string, filter: CostFilter): Promise<ApiResponse<CostData>> {
  const queryParams = new URLSearchParams({
    startDate: filter.startDate,
    endDate: filter.endDate,
    granularity: filter.granularity
  });
  
  if (filter.groupBy) {
    queryParams.append('groupBy', filter.groupBy);
  }

  return apiRequest<CostData>(`/accounts/${accountId}/costs/summary?${queryParams.toString()}`);
}

export async function getCostBreakdown(accountId: string, filter: CostFilter): Promise<ApiResponse<CostBreakdown[]>> {
  const queryParams = new URLSearchParams({
    startDate: filter.startDate,
    endDate: filter.endDate,
    granularity: filter.granularity
  });
  
  if (filter.groupBy) {
    queryParams.append('groupBy', filter.groupBy);
  }

  return apiRequest<CostBreakdown[]>(`/accounts/${accountId}/costs/breakdown?${queryParams.toString()}`);
}

export async function getCostTrend(accountId: string, filter: CostFilter): Promise<ApiResponse<CostTrend[]>> {
  const queryParams = new URLSearchParams({
    startDate: filter.startDate,
    endDate: filter.endDate,
    granularity: filter.granularity
  });

  return apiRequest<CostTrend[]>(`/accounts/${accountId}/costs/trend?${queryParams.toString()}`);
}

// Recommendations
export async function getRecommendations(accountId: string, filters?: RecommendationFilter): Promise<ApiResponse<Recommendation[]>> {
  const queryParams = new URLSearchParams();
  
  if (filters) {
    if (filters.priority && filters.priority.length > 0) {
      queryParams.append('priority', filters.priority.join(','));
    }
    if (filters.status && filters.status.length > 0) {
      queryParams.append('status', filters.status.join(','));
    }
    if (filters.types && filters.types.length > 0) {
      queryParams.append('types', filters.types.join(','));
    }
    if (filters.resourceTypes && filters.resourceTypes.length > 0) {
      queryParams.append('resourceTypes', filters.resourceTypes.join(','));
    }
    if (filters.search) {
      queryParams.append('search', filters.search);
    }
  }

  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return apiRequest<Recommendation[]>(`/accounts/${accountId}/recommendations${queryString}`);
}

export async function getRecommendation(accountId: string, recommendationId: string): Promise<ApiResponse<Recommendation>> {
  return apiRequest<Recommendation>(`/accounts/${accountId}/recommendations/${recommendationId}`);
}

export async function updateRecommendationStatus(
  accountId: string, 
  recommendationId: string, 
  status: 'in_progress' | 'applied' | 'dismissed'
): Promise<ApiResponse<Recommendation>> {
  return apiRequest<Recommendation>(
    `/accounts/${accountId}/recommendations/${recommendationId}/status`, 
    'PUT', 
    { status }
  );
}

export async function createActionFromRecommendation(
  accountId: string,
  recommendationId: string,
  requiresApproval: boolean = true
): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(
    `/accounts/${accountId}/recommendations/${recommendationId}/actions`,
    'POST',
    { requiresApproval }
  );
}

// Actions
export async function getActions(accountId: string, filters?: ActionFilter): Promise<ApiResponse<Action[]>> {
  const queryParams = new URLSearchParams();
  
  if (filters) {
    if (filters.status && filters.status.length > 0) {
      queryParams.append('status', filters.status.join(','));
    }
    if (filters.approvalStatus && filters.approvalStatus.length > 0) {
      queryParams.append('approvalStatus', filters.approvalStatus.join(','));
    }
    if (filters.types && filters.types.length > 0) {
      queryParams.append('types', filters.types.join(','));
    }
    if (filters.resourceTypes && filters.resourceTypes.length > 0) {
      queryParams.append('resourceTypes', filters.resourceTypes.join(','));
    }
    if (filters.search) {
      queryParams.append('search', filters.search);
    }
  }

  const queryString = queryParams.toString() ? `?${queryParams.toString()}` : '';
  return apiRequest<Action[]>(`/accounts/${accountId}/actions${queryString}`);
}

export async function getAction(accountId: string, actionId: string): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(`/accounts/${accountId}/actions/${actionId}`);
}

export async function approveAction(accountId: string, actionId: string): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(
    `/accounts/${accountId}/actions/${actionId}/approve`,
    'PUT'
  );
}

export async function rejectAction(accountId: string, actionId: string, reason?: string): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(
    `/accounts/${accountId}/actions/${actionId}/reject`,
    'PUT',
    { reason }
  );
}

export async function executeAction(accountId: string, actionId: string): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(
    `/accounts/${accountId}/actions/${actionId}/execute`,
    'POST'
  );
}

export async function scheduleAction(
  accountId: string, 
  actionId: string, 
  scheduledTime: string
): Promise<ApiResponse<Action>> {
  return apiRequest<Action>(
    `/accounts/${accountId}/actions/${actionId}/schedule`,
    'PUT',
    { scheduledTime }
  );
}

// Workflows
export async function getWorkflows(accountId: string): Promise<ApiResponse<Workflow[]>> {
  return apiRequest<Workflow[]>(`/accounts/${accountId}/workflows`);
}

export async function getWorkflow(accountId: string, workflowId: string): Promise<ApiResponse<Workflow>> {
  return apiRequest<Workflow>(`/accounts/${accountId}/workflows/${workflowId}`);
}

export async function createWorkflow(accountId: string, workflow: Partial<Workflow>): Promise<ApiResponse<Workflow>> {
  return apiRequest<Workflow>(`/accounts/${accountId}/workflows`, 'POST', workflow);
}

export async function updateWorkflow(accountId: string, workflowId: string, updates: Partial<Workflow>): Promise<ApiResponse<Workflow>> {
  return apiRequest<Workflow>(`/accounts/${accountId}/workflows/${workflowId}`, 'PUT', updates);
}

export async function deleteWorkflow(accountId: string, workflowId: string): Promise<ApiResponse<void>> {
  return apiRequest<void>(`/accounts/${accountId}/workflows/${workflowId}`, 'DELETE');
}

export async function executeWorkflow(accountId: string, workflowId: string): Promise<ApiResponse<any>> {
  return apiRequest<any>(
    `/accounts/${accountId}/workflows/${workflowId}/execute`,
    'POST'
  );
}

// Terraform
export async function getTerraformTemplates(): Promise<ApiResponse<TerraformTemplate[]>> {
  return apiRequest<TerraformTemplate[]>('/terraform/templates');
}

export async function getTerraformTemplate(templateId: string): Promise<ApiResponse<TerraformTemplate>> {
  return apiRequest<TerraformTemplate>(`/terraform/templates/${templateId}`);
}

export async function createTerraformTemplate(template: Partial<TerraformTemplate>): Promise<ApiResponse<TerraformTemplate>> {
  return apiRequest<TerraformTemplate>('/terraform/templates', 'POST', template);
}

export async function updateTerraformTemplate(templateId: string, updates: Partial<TerraformTemplate>): Promise<ApiResponse<TerraformTemplate>> {
  return apiRequest<TerraformTemplate>(`/terraform/templates/${templateId}`, 'PUT', updates);
}

export async function deleteTerraformTemplate(templateId: string): Promise<ApiResponse<void>> {
  return apiRequest<void>(`/terraform/templates/${templateId}`, 'DELETE');
}

export async function deployTerraformTemplate(
  templateId: string, 
  variables: Record<string, any>
): Promise<ApiResponse<TerraformDeployment>> {
  return apiRequest<TerraformDeployment>(
    `/terraform/templates/${templateId}/deploy`,
    'POST',
    { variables }
  );
}

export async function getTerraformDeployments(): Promise<ApiResponse<TerraformDeployment[]>> {
  return apiRequest<TerraformDeployment[]>('/terraform/deployments');
}

export async function getTerraformDeployment(deploymentId: string): Promise<ApiResponse<TerraformDeployment>> {
  return apiRequest<TerraformDeployment>(`/terraform/deployments/${deploymentId}`);
}

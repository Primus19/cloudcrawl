/**
 * Type definitions for the Cloud Cost Optimizer application
 */

// Cloud Provider Types
export type CloudProvider = 'aws' | 'azure' | 'gcp';

// Account Types
export interface CloudAccount {
  id: string;
  name: string;
  provider: CloudProvider;
  status: 'active' | 'inactive' | 'error';
  lastSyncTime?: string;
}

export interface Organization {
  id: string;
  name: string;
  accounts: CloudAccount[];
}

// Resource Types
export interface CloudResource {
  id: string;
  name: string;
  type: string;
  region: string;
  status: string;
  createdAt: string;
  tags: Record<string, string>;
  properties: Record<string, any>;
  cost?: CostData;
}

// Cost Types
export interface CostData {
  amount: number;
  currency: string;
  period: 'daily' | 'weekly' | 'monthly' | 'yearly';
  startDate: string;
  endDate: string;
}

export interface CostBreakdown {
  service: string;
  amount: number;
  currency: string;
  percentage: number;
}

export interface CostTrend {
  date: string;
  amount: number;
  currency: string;
}

// Recommendation Types
export interface Recommendation {
  id: string;
  type: string;
  priority: 'high' | 'medium' | 'low';
  status: 'new' | 'in_progress' | 'applied' | 'dismissed';
  resourceId?: string;
  resourceName?: string;
  resourceType?: string;
  description: string;
  estimatedSavings?: {
    amount: number;
    currency: string;
    period: 'monthly' | 'yearly';
  };
  details: Record<string, any>;
  createdAt: string;
}

// Action Types
export interface Action {
  id: string;
  type: string;
  status: 'pending' | 'in_progress' | 'completed' | 'failed';
  approvalStatus: 'pending' | 'approved' | 'rejected';
  resourceId?: string;
  resourceName?: string;
  resourceType?: string;
  parameters: Record<string, any>;
  recommendationId?: string;
  createdBy?: string;
  createdAt: string;
  scheduledTime?: string;
  completedAt?: string;
  result?: Record<string, any>;
}

// Workflow Types
export interface Workflow {
  id: string;
  name: string;
  description?: string;
  triggerType: 'manual' | 'scheduled' | 'event';
  triggerConfig?: Record<string, any>;
  steps: WorkflowStep[];
  status: 'active' | 'inactive';
  createdAt: string;
  lastExecutionTime?: string;
}

export interface WorkflowStep {
  type: 'action' | 'condition' | 'delay';
  actionId?: string;
  condition?: Record<string, any>;
  durationSeconds?: number;
  trueBranch?: number;
  falseBranch?: number;
}

export interface WorkflowExecution {
  id: string;
  workflowId: string;
  status: 'in_progress' | 'completed' | 'failed';
  startTime: string;
  endTime?: string;
  results: Record<string, any>;
}

// Dashboard Types
export interface DashboardWidget {
  id: string;
  type: 'cost_summary' | 'cost_trend' | 'recommendations' | 'resources' | 'actions';
  title: string;
  size: 'small' | 'medium' | 'large';
  position: {
    x: number;
    y: number;
  };
  config: Record<string, any>;
}

export interface Dashboard {
  id: string;
  name: string;
  widgets: DashboardWidget[];
  isDefault: boolean;
}

// User Types
export interface User {
  id: string;
  name: string;
  email: string;
  role: 'admin' | 'user' | 'viewer';
  preferences: Record<string, any>;
}

// API Response Types
export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
  success: boolean;
}

// Filter Types
export interface ResourceFilter {
  providers?: CloudProvider[];
  regions?: string[];
  types?: string[];
  tags?: Record<string, string>;
  status?: string[];
  search?: string;
}

export interface CostFilter {
  startDate: string;
  endDate: string;
  granularity: 'daily' | 'weekly' | 'monthly';
  groupBy?: 'service' | 'account' | 'region' | 'tag';
}

export interface RecommendationFilter {
  priority?: ('high' | 'medium' | 'low')[];
  status?: ('new' | 'in_progress' | 'applied' | 'dismissed')[];
  types?: string[];
  resourceTypes?: string[];
  search?: string;
}

export interface ActionFilter {
  status?: ('pending' | 'in_progress' | 'completed' | 'failed')[];
  approvalStatus?: ('pending' | 'approved' | 'rejected')[];
  types?: string[];
  resourceTypes?: string[];
  search?: string;
}

// Terraform Types
export interface TerraformTemplate {
  id: string;
  name: string;
  description?: string;
  variables: Record<string, {
    description: string;
    type: string;
    default?: any;
    required: boolean;
  }>;
  content: string;
  createdAt: string;
  updatedAt: string;
}

export interface TerraformDeployment {
  id: string;
  templateId: string;
  status: 'planning' | 'applying' | 'completed' | 'failed';
  variables: Record<string, any>;
  output?: Record<string, any>;
  logs?: string;
  createdAt: string;
  completedAt?: string;
}

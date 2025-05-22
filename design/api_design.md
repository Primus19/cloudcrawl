# Cloud Cost Optimizer - API Design

## Overview

The Cloud Cost Optimizer API is designed as a RESTful service that provides comprehensive access to all platform capabilities. The API follows modern best practices including versioning, consistent error handling, and comprehensive documentation. It serves as the foundation for both the web interface and integration with external systems.

## API Design Principles

1. **RESTful Architecture**: Resource-oriented design with standard HTTP methods
2. **Versioning**: API versioning to ensure backward compatibility
3. **Consistent Response Format**: Standardized JSON response structure
4. **Authentication & Authorization**: OAuth 2.0 with fine-grained permissions
5. **Rate Limiting**: Protection against abuse
6. **Comprehensive Documentation**: OpenAPI/Swagger specification
7. **Idempotency**: Safe retries for non-idempotent operations

## Base URL Structure

```
https://api.cloudcostoptimizer.com/v1/{resource}
```

## Authentication

The API uses OAuth 2.0 for authentication with support for:

- Client credentials flow for service-to-service communication
- Authorization code flow for user-based access
- JWT tokens with configurable expiration

Example Authentication Header:
```
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

## Standard Response Format

### Success Response

```json
{
  "status": "success",
  "data": {
    // Resource-specific data
  },
  "meta": {
    "pagination": {
      "total": 100,
      "per_page": 25,
      "current_page": 1,
      "last_page": 4,
      "next_page_url": "/v1/resources?page=2",
      "prev_page_url": null
    }
  }
}
```

### Error Response

```json
{
  "status": "error",
  "error": {
    "code": "resource_not_found",
    "message": "The requested resource was not found",
    "details": {
      "resource_id": "123e4567-e89b-12d3-a456-426614174000"
    }
  },
  "trace_id": "abcdef123456"
}
```

## API Resources and Endpoints

### 1. Authentication and User Management

#### Users

```
GET    /users                  # List users
POST   /users                  # Create user
GET    /users/{id}             # Get user details
PUT    /users/{id}             # Update user
DELETE /users/{id}             # Delete user
GET    /users/me               # Get current user
```

#### Teams

```
GET    /teams                  # List teams
POST   /teams                  # Create team
GET    /teams/{id}             # Get team details
PUT    /teams/{id}             # Update team
DELETE /teams/{id}             # Delete team
GET    /teams/{id}/members     # List team members
POST   /teams/{id}/members     # Add team member
DELETE /teams/{id}/members/{userId} # Remove team member
```

#### Authentication

```
POST   /auth/login             # User login
POST   /auth/logout            # User logout
POST   /auth/refresh           # Refresh token
POST   /auth/mfa/enable        # Enable MFA
POST   /auth/mfa/disable       # Disable MFA
POST   /auth/mfa/verify        # Verify MFA code
```

### 2. Organization and Account Management

#### Organizations

```
GET    /organizations          # List organizations
POST   /organizations          # Create organization
GET    /organizations/{id}     # Get organization details
PUT    /organizations/{id}     # Update organization
DELETE /organizations/{id}     # Delete organization
```

#### Cloud Accounts

```
GET    /cloud-accounts         # List cloud accounts
POST   /cloud-accounts         # Create cloud account
GET    /cloud-accounts/{id}    # Get cloud account details
PUT    /cloud-accounts/{id}    # Update cloud account
DELETE /cloud-accounts/{id}    # Delete cloud account
POST   /cloud-accounts/{id}/sync # Sync cloud account resources
GET    /cloud-accounts/{id}/status # Get sync status
```

### 3. Resource Management

#### Resources

```
GET    /resources              # List resources
GET    /resources/{id}         # Get resource details
PUT    /resources/{id}/tags    # Update resource tags
GET    /resources/{id}/cost    # Get resource cost history
GET    /resources/{id}/metrics # Get resource metrics
```

#### Resource Groups

```
GET    /resource-groups        # List resource groups
POST   /resource-groups        # Create resource group
GET    /resource-groups/{id}   # Get resource group details
PUT    /resource-groups/{id}   # Update resource group
DELETE /resource-groups/{id}   # Delete resource group
POST   /resource-groups/{id}/resources # Add resources to group
DELETE /resource-groups/{id}/resources/{resourceId} # Remove resource from group
```

### 4. Cost Management

#### Cost Analysis

```
GET    /costs                  # Get aggregated costs
GET    /costs/breakdown        # Get cost breakdown
GET    /costs/trends           # Get cost trends
GET    /costs/anomalies        # Get cost anomalies
```

#### Budgets

```
GET    /budgets                # List budgets
POST   /budgets                # Create budget
GET    /budgets/{id}           # Get budget details
PUT    /budgets/{id}           # Update budget
DELETE /budgets/{id}           # Delete budget
GET    /budgets/{id}/alerts    # List budget alerts
POST   /budgets/{id}/alerts    # Create budget alert
```

### 5. Recommendation and Action Engine

#### Recommendations

```
GET    /recommendations        # List recommendations
GET    /recommendations/{id}   # Get recommendation details
PUT    /recommendations/{id}   # Update recommendation status
GET    /recommendations/summary # Get recommendation summary
```

#### Actions

```
GET    /actions                # List actions
POST   /actions                # Create action
GET    /actions/{id}           # Get action details
PUT    /actions/{id}           # Update action
DELETE /actions/{id}           # Delete action
POST   /actions/{id}/execute   # Execute action
GET    /actions/{id}/status    # Get action execution status
POST   /actions/{id}/cancel    # Cancel action execution
```

#### Workflows

```
GET    /workflows              # List workflows
POST   /workflows              # Create workflow
GET    /workflows/{id}         # Get workflow details
PUT    /workflows/{id}         # Update workflow
DELETE /workflows/{id}         # Delete workflow
POST   /workflows/{id}/execute # Execute workflow
GET    /workflows/{id}/executions # List workflow executions
GET    /workflows/{id}/executions/{executionId} # Get execution details
```

#### Approvals

```
GET    /approvals              # List pending approvals
GET    /approvals/{id}         # Get approval details
POST   /approvals/{id}/approve # Approve action
POST   /approvals/{id}/reject  # Reject action
```

### 6. Notification and Alerting

#### Notifications

```
GET    /notifications          # List notifications
GET    /notifications/{id}     # Get notification details
PUT    /notifications/{id}/read # Mark notification as read
PUT    /notifications/read-all # Mark all notifications as read
```

#### Alert Configurations

```
GET    /alert-configs          # List alert configurations
POST   /alert-configs          # Create alert configuration
GET    /alert-configs/{id}     # Get alert configuration details
PUT    /alert-configs/{id}     # Update alert configuration
DELETE /alert-configs/{id}     # Delete alert configuration
```

### 7. Terraform Integration

#### Terraform States

```
GET    /terraform/states       # List Terraform states
POST   /terraform/states       # Create/update Terraform state
GET    /terraform/states/{id}  # Get Terraform state details
DELETE /terraform/states/{id}  # Delete Terraform state
GET    /terraform/states/{id}/resources # List resources in state
```

#### Terraform Modules

```
GET    /terraform/modules      # List Terraform modules
POST   /terraform/modules      # Create Terraform module
GET    /terraform/modules/{id} # Get Terraform module details
PUT    /terraform/modules/{id} # Update Terraform module
DELETE /terraform/modules/{id} # Delete Terraform module
```

#### Terraform Analysis

```
POST   /terraform/analyze      # Analyze Terraform template
POST   /terraform/optimize     # Optimize Terraform template
```

### 8. Reporting and Analytics

#### Reports

```
GET    /reports                # List reports
POST   /reports                # Create report
GET    /reports/{id}           # Get report details
DELETE /reports/{id}           # Delete report
GET    /reports/{id}/download  # Download report
```

#### Dashboards

```
GET    /dashboards             # List dashboards
POST   /dashboards             # Create dashboard
GET    /dashboards/{id}        # Get dashboard details
PUT    /dashboards/{id}        # Update dashboard
DELETE /dashboards/{id}        # Delete dashboard
```

### 9. System Administration

#### Settings

```
GET    /settings               # Get system settings
PUT    /settings               # Update system settings
```

#### Audit Logs

```
GET    /audit-logs             # List audit logs
GET    /audit-logs/{id}        # Get audit log details
```

## Detailed Endpoint Specifications

### Action Execution API (Key Feature)

#### Create Action

```
POST /actions
```

Request Body:
```json
{
  "action_type": "resize_instance",
  "resource_id": "123e4567-e89b-12d3-a456-426614174000",
  "parameters": {
    "target_instance_type": "t3.medium",
    "schedule": "immediate"
  },
  "description": "Resize underutilized EC2 instance",
  "recommendation_id": "789e4567-e89b-12d3-a456-426614174000"
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "id": "456e4567-e89b-12d3-a456-426614174000",
    "action_type": "resize_instance",
    "resource_id": "123e4567-e89b-12d3-a456-426614174000",
    "parameters": {
      "target_instance_type": "t3.medium",
      "schedule": "immediate"
    },
    "description": "Resize underutilized EC2 instance",
    "recommendation_id": "789e4567-e89b-12d3-a456-426614174000",
    "status": "pending",
    "created_at": "2025-05-21T12:34:56Z",
    "created_by": "user-123",
    "requires_approval": true,
    "approval_status": "pending"
  }
}
```

#### Execute Action

```
POST /actions/{id}/execute
```

Request Body:
```json
{
  "confirmation": true,
  "execution_parameters": {
    "dry_run": false
  }
}
```

Response:
```json
{
  "status": "success",
  "data": {
    "id": "456e4567-e89b-12d3-a456-426614174000",
    "execution_id": "567e4567-e89b-12d3-a456-426614174000",
    "status": "in_progress",
    "started_at": "2025-05-21T12:35:00Z",
    "estimated_completion": "2025-05-21T12:40:00Z"
  }
}
```

#### Get Action Execution Status

```
GET /actions/{id}/status
```

Response:
```json
{
  "status": "success",
  "data": {
    "id": "456e4567-e89b-12d3-a456-426614174000",
    "execution_id": "567e4567-e89b-12d3-a456-426614174000",
    "status": "completed",
    "started_at": "2025-05-21T12:35:00Z",
    "completed_at": "2025-05-21T12:38:23Z",
    "result": {
      "success": true,
      "details": {
        "previous_instance_type": "t3.large",
        "new_instance_type": "t3.medium",
        "estimated_monthly_savings": 25.60,
        "currency": "USD"
      }
    }
  }
}
```

### Recommendation API

#### List Recommendations

```
GET /recommendations?status=open&priority=high&resource_type=ec2_instance
```

Response:
```json
{
  "status": "success",
  "data": [
    {
      "id": "789e4567-e89b-12d3-a456-426614174000",
      "resource_id": "123e4567-e89b-12d3-a456-426614174000",
      "resource_type": "ec2_instance",
      "recommendation_type": "rightsizing",
      "priority": "high",
      "status": "open",
      "estimated_savings": {
        "amount": 25.60,
        "currency": "USD",
        "period": "monthly"
      },
      "details": {
        "current_instance_type": "t3.large",
        "recommended_instance_type": "t3.medium",
        "utilization_metrics": {
          "cpu_average": 15.2,
          "memory_average": 35.7
        }
      },
      "created_at": "2025-05-20T10:15:30Z"
    }
  ],
  "meta": {
    "pagination": {
      "total": 42,
      "per_page": 25,
      "current_page": 1,
      "last_page": 2,
      "next_page_url": "/v1/recommendations?status=open&priority=high&resource_type=ec2_instance&page=2",
      "prev_page_url": null
    }
  }
}
```

## Webhook Integration

The API supports webhook notifications for key events:

```
POST /webhooks
```

Request Body:
```json
{
  "name": "Cost Anomaly Alert",
  "events": ["cost.anomaly.detected", "action.completed"],
  "target_url": "https://example.com/webhook-receiver",
  "secret": "your-webhook-secret",
  "active": true
}
```

## Batch Operations

For efficient bulk operations:

```
POST /batch
```

Request Body:
```json
{
  "operations": [
    {
      "method": "POST",
      "path": "/actions",
      "body": {
        "action_type": "resize_instance",
        "resource_id": "123e4567-e89b-12d3-a456-426614174000",
        "parameters": {
          "target_instance_type": "t3.medium"
        }
      }
    },
    {
      "method": "PUT",
      "path": "/resources/456e4567-e89b-12d3-a456-426614174000/tags",
      "body": {
        "tags": {
          "environment": "production",
          "owner": "team-finance"
        }
      }
    }
  ]
}
```

## API Versioning Strategy

1. **URL-based Versioning**:
   - Major version in URL path: `/v1/resources`
   - Ensures clear separation between incompatible versions

2. **Version Lifecycle**:
   - Minimum 12-month support for deprecated versions
   - Deprecation notices via response headers
   - Version sunset announcements 6 months in advance

## Rate Limiting

Rate limits are applied per API key and communicated via headers:

```
X-RateLimit-Limit: 5000
X-RateLimit-Remaining: 4985
X-RateLimit-Reset: 1622148000
```

## API Documentation

The API is documented using OpenAPI/Swagger:

```
GET /docs
```

Interactive documentation is available at:
```
https://api.cloudcostoptimizer.com/docs
```

## SDK Support

Official SDKs are provided for:
- Python
- JavaScript/TypeScript
- Go
- Java

Example Python SDK usage:

```python
from cloudcostoptimizer import CloudCostOptimizer

client = CloudCostOptimizer(api_key="your-api-key")

# List high-priority recommendations
recommendations = client.recommendations.list(
    status="open",
    priority="high",
    resource_type="ec2_instance"
)

# Execute an action
action = client.actions.execute(
    action_id="456e4567-e89b-12d3-a456-426614174000",
    confirmation=True
)
```

## Security Considerations

1. **API Key Management**:
   - Rotation policies
   - Scope-limited API keys
   - Key expiration

2. **Request Signing**:
   - HMAC request signing for sensitive operations
   - Timestamp validation to prevent replay attacks

3. **Transport Security**:
   - TLS 1.2+ required
   - HSTS headers
   - Certificate pinning for SDKs

4. **Input Validation**:
   - Strict schema validation
   - Protection against injection attacks
   - Request size limits

## Monitoring and Observability

The API includes built-in observability endpoints:

```
GET /health
GET /metrics
```

Response headers include trace IDs for correlation:
```
X-Trace-ID: abcdef123456
```

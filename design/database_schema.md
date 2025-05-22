# Cloud Cost Optimizer - Database Schema Design

## Overview

The database schema for the Cloud Cost Optimizer platform is designed to support multi-cloud cost management, actionable recommendations, and secure automation. The schema uses a combination of relational databases for structured data and time-series databases for metrics and cost data.

## Database Technologies

1. **Relational Database**: PostgreSQL
   - For structured data like users, accounts, resources, and configurations
   - ACID compliance for critical transactions
   - Rich query capabilities for complex reporting

2. **Time-Series Database**: InfluxDB/TimescaleDB
   - For historical cost and metric data
   - Efficient storage and querying of time-based data
   - Aggregation and downsampling capabilities

3. **Object Storage**: S3-compatible storage
   - For reports, backups, and large datasets
   - Cost-effective long-term storage
   - Versioning and lifecycle policies

4. **Cache**: Redis
   - For performance optimization
   - Session management
   - Rate limiting and distributed locking

## Entity Relationship Diagram

```
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Organizations │◄──────┤ Teams         │◄──────┤ Users         │
└───────┬───────┘       └───────────────┘       └───────────────┘
        │                       ▲                       ▲
        │                       │                       │
        ▼                       │                       │
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ CloudAccounts │◄──────┤ ResourceGroups│◄──────┤ Permissions   │
└───────┬───────┘       └───────┬───────┘       └───────────────┘
        │                       │
        │                       │
        ▼                       ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Resources     │◄──────┤ Tags          │       │ CostData      │
└───────┬───────┘       └───────────────┘       └───────┬───────┘
        │                                               │
        │                                               │
        ▼                                               ▼
┌───────────────┐       ┌───────────────┐       ┌───────────────┐
│ Recommendations│──────►│ Actions       │◄──────┤ ActionHistory │
└───────────────┘       └───────┬───────┘       └───────────────┘
                                │
                                │
                                ▼
                        ┌───────────────┐       ┌───────────────┐
                        │ Workflows     │◄──────┤ Approvals     │
                        └───────┬───────┘       └───────────────┘
                                │
                                │
                                ▼
                        ┌───────────────┐       ┌───────────────┐
                        │ Notifications │       │ AuditLogs     │
                        └───────────────┘       └───────────────┘
```

## Table Definitions

### Core Tables

#### Organizations
```sql
CREATE TABLE organizations (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    settings JSONB
);
```

#### Teams
```sql
CREATE TABLE teams (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    settings JSONB,
    UNIQUE(organization_id, name)
);
```

#### Users
```sql
CREATE TABLE users (
    id UUID PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255),
    mfa_enabled BOOLEAN DEFAULT FALSE,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    settings JSONB,
    status VARCHAR(50) DEFAULT 'active'
);
```

#### UserTeams
```sql
CREATE TABLE user_teams (
    user_id UUID NOT NULL REFERENCES users(id),
    team_id UUID NOT NULL REFERENCES teams(id),
    role VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (user_id, team_id)
);
```

#### Permissions
```sql
CREATE TABLE permissions (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    description TEXT,
    resource_type VARCHAR(50) NOT NULL,
    action_type VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### RolePermissions
```sql
CREATE TABLE role_permissions (
    role VARCHAR(50) NOT NULL,
    permission_id UUID NOT NULL REFERENCES permissions(id),
    organization_id UUID NOT NULL REFERENCES organizations(id),
    PRIMARY KEY (role, permission_id, organization_id)
);
```

### Cloud Account Management

#### CloudAccounts
```sql
CREATE TABLE cloud_accounts (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    provider VARCHAR(50) NOT NULL,
    account_id VARCHAR(255) NOT NULL,
    credentials JSONB,
    status VARCHAR(50) DEFAULT 'active',
    last_sync TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    settings JSONB,
    UNIQUE(organization_id, provider, account_id)
);
```

#### CloudAccountTeams
```sql
CREATE TABLE cloud_account_teams (
    cloud_account_id UUID NOT NULL REFERENCES cloud_accounts(id),
    team_id UUID NOT NULL REFERENCES teams(id),
    access_level VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (cloud_account_id, team_id)
);
```

### Resource Management

#### Resources
```sql
CREATE TABLE resources (
    id UUID PRIMARY KEY,
    cloud_account_id UUID NOT NULL REFERENCES cloud_accounts(id),
    resource_id VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100) NOT NULL,
    name VARCHAR(255),
    region VARCHAR(100),
    status VARCHAR(50),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    last_seen TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    properties JSONB,
    UNIQUE(cloud_account_id, resource_id)
);
```

#### ResourceGroups
```sql
CREATE TABLE resource_groups (
    id UUID PRIMARY KEY,
    cloud_account_id UUID NOT NULL REFERENCES cloud_accounts(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(cloud_account_id, name)
);
```

#### ResourceGroupMemberships
```sql
CREATE TABLE resource_group_memberships (
    resource_id UUID NOT NULL REFERENCES resources(id),
    resource_group_id UUID NOT NULL REFERENCES resource_groups(id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (resource_id, resource_group_id)
);
```

#### Tags
```sql
CREATE TABLE tags (
    id UUID PRIMARY KEY,
    resource_id UUID NOT NULL REFERENCES resources(id),
    key VARCHAR(255) NOT NULL,
    value TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(resource_id, key)
);
```

### Cost Management

#### CostData
```sql
-- This would typically be in a time-series database
CREATE TABLE cost_data (
    id UUID PRIMARY KEY,
    cloud_account_id UUID NOT NULL REFERENCES cloud_accounts(id),
    resource_id UUID REFERENCES resources(id),
    timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    amount DECIMAL(20, 6) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    granularity VARCHAR(20) NOT NULL, -- hourly, daily, monthly
    dimensions JSONB,
    INDEX(cloud_account_id, timestamp),
    INDEX(resource_id, timestamp)
);
```

#### Budgets
```sql
CREATE TABLE budgets (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    amount DECIMAL(20, 6) NOT NULL,
    currency VARCHAR(3) NOT NULL,
    period VARCHAR(20) NOT NULL, -- monthly, quarterly, yearly
    start_date DATE NOT NULL,
    end_date DATE,
    filters JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

#### BudgetAlerts
```sql
CREATE TABLE budget_alerts (
    id UUID PRIMARY KEY,
    budget_id UUID NOT NULL REFERENCES budgets(id),
    threshold DECIMAL(5, 2) NOT NULL, -- percentage
    notification_channels JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);
```

### Recommendation and Action Engine

#### Recommendations
```sql
CREATE TABLE recommendations (
    id UUID PRIMARY KEY,
    cloud_account_id UUID NOT NULL REFERENCES cloud_accounts(id),
    resource_id UUID REFERENCES resources(id),
    recommendation_type VARCHAR(100) NOT NULL,
    status VARCHAR(50) DEFAULT 'open',
    priority VARCHAR(20) NOT NULL, -- high, medium, low
    estimated_savings DECIMAL(20, 6),
    currency VARCHAR(3),
    details JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE
);
```

#### Actions
```sql
CREATE TABLE actions (
    id UUID PRIMARY KEY,
    recommendation_id UUID REFERENCES recommendations(id),
    action_type VARCHAR(100) NOT NULL,
    resource_id UUID REFERENCES resources(id),
    status VARCHAR(50) DEFAULT 'pending',
    parameters JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    scheduled_for TIMESTAMP WITH TIME ZONE,
    created_by UUID REFERENCES users(id)
);
```

#### ActionHistory
```sql
CREATE TABLE action_history (
    id UUID PRIMARY KEY,
    action_id UUID NOT NULL REFERENCES actions(id),
    status VARCHAR(50) NOT NULL,
    executed_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    executed_by UUID REFERENCES users(id),
    result JSONB,
    details TEXT
);
```

#### Workflows
```sql
CREATE TABLE workflows (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    trigger_type VARCHAR(50) NOT NULL, -- manual, scheduled, event-based
    definition JSONB NOT NULL,
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_by UUID REFERENCES users(id)
);
```

#### WorkflowExecutions
```sql
CREATE TABLE workflow_executions (
    id UUID PRIMARY KEY,
    workflow_id UUID NOT NULL REFERENCES workflows(id),
    status VARCHAR(50) NOT NULL,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE,
    triggered_by UUID REFERENCES users(id),
    results JSONB
);
```

#### Approvals
```sql
CREATE TABLE approvals (
    id UUID PRIMARY KEY,
    action_id UUID NOT NULL REFERENCES actions(id),
    approver_id UUID NOT NULL REFERENCES users(id),
    status VARCHAR(50) DEFAULT 'pending',
    comments TEXT,
    requested_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    responded_at TIMESTAMP WITH TIME ZONE
);
```

### Notification and Audit

#### Notifications
```sql
CREATE TABLE notifications (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    team_id UUID REFERENCES teams(id),
    title VARCHAR(255) NOT NULL,
    message TEXT NOT NULL,
    type VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'unread',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP WITH TIME ZONE,
    data JSONB
);
```

#### AuditLogs
```sql
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY,
    user_id UUID REFERENCES users(id),
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(100),
    resource_id VARCHAR(255),
    timestamp TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    ip_address VARCHAR(45),
    user_agent TEXT,
    details JSONB
);
```

### Terraform Integration

#### TerraformStates
```sql
CREATE TABLE terraform_states (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    state_file JSONB,
    last_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, name)
);
```

#### TerraformModules
```sql
CREATE TABLE terraform_modules (
    id UUID PRIMARY KEY,
    organization_id UUID NOT NULL REFERENCES organizations(id),
    name VARCHAR(255) NOT NULL,
    description TEXT,
    source_url TEXT,
    version VARCHAR(50),
    variables JSONB,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(organization_id, name, version)
);
```

## Indexes and Performance Considerations

1. **Indexing Strategy**:
   - Index on foreign keys for efficient joins
   - Composite indexes for common query patterns
   - Partial indexes for filtered queries

2. **Partitioning**:
   - Time-based partitioning for cost data
   - Organization-based partitioning for multi-tenant tables

3. **Data Retention**:
   - Automated archiving of historical data
   - Downsampling of time-series data
   - Configurable retention policies

## Data Migration and Evolution

1. **Schema Versioning**:
   - Track schema versions in a dedicated table
   - Use migration scripts for schema changes

2. **Zero-Downtime Migrations**:
   - Backward-compatible schema changes
   - Dual-write during transition periods

3. **Data Backfilling**:
   - Strategies for populating new columns/tables
   - Batch processing for large datasets

## Security Considerations

1. **Data Encryption**:
   - Encryption at rest for all databases
   - Encryption in transit for all connections
   - Column-level encryption for sensitive data

2. **Access Control**:
   - Row-level security policies
   - Column-level permissions
   - Database role separation

3. **Audit and Compliance**:
   - Database activity monitoring
   - Change data capture for audit trails
   - Compliance with data protection regulations

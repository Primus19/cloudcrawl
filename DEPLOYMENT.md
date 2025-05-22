# Cloud Cost Optimizer - Deployment Instructions

## Overview

The Cloud Cost Optimizer is a comprehensive solution for managing and optimizing cloud costs across AWS, Azure, and GCP. This document provides instructions for deploying and configuring the solution.

## System Requirements

- **Operating System**: Linux, macOS, or Windows with Docker support
- **Docker**: Docker Engine 20.10.0 or higher
- **Docker Compose**: version 2.0.0 or higher
- **Memory**: Minimum 4GB RAM
- **Storage**: Minimum 10GB free disk space
- **Network**: Internet connectivity for cloud provider API access

## Quick Start with Docker

The easiest way to deploy the Cloud Cost Optimizer is using Docker Compose:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-org/cloud-cost-optimizer.git
   cd cloud-cost-optimizer
   ```

2. **Configure environment variables**:
   Copy the example environment file and edit it with your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred text editor
   ```

3. **Build and start the containers**:
   ```bash
   docker-compose up -d
   ```

4. **Access the application**:
   Open your browser and navigate to `http://localhost:8080`

## Manual Installation

### Prerequisites

- **Python**: 3.9 or higher
- **Node.js**: 16.0.0 or higher
- **npm**: 8.0.0 or higher
- **Terraform**: 1.0.0 or higher

### Backend Setup

1. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure the application**:
   ```bash
   cp config.example.py config.py
   # Edit config.py with your settings
   ```

4. **Initialize the database**:
   ```bash
   python src/scripts/init_db.py
   ```

5. **Start the backend server**:
   ```bash
   python src/main.py
   ```

### Frontend Setup

1. **Navigate to the UI directory**:
   ```bash
   cd src/ui/dashboard
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Build the frontend**:
   ```bash
   npm run build
   ```

4. **Configure API endpoint** (if not using default):
   Edit `.env.production` to set the correct API endpoint.

## Cloud Provider Configuration

### AWS Configuration

1. **Create an IAM user** with the following permissions:
   - `AmazonEC2ReadOnlyAccess`
   - `AmazonS3ReadOnlyAccess`
   - `AmazonRDSReadOnlyAccess`
   - `AWSCloudFormationReadOnlyAccess`
   - `AWSCostExplorerAccess`

2. **Generate access keys** for the IAM user.

3. **Configure credentials** in the application settings or environment variables:
   ```
   AWS_ACCESS_KEY_ID=your_access_key
   AWS_SECRET_ACCESS_KEY=your_secret_key
   AWS_REGION=your_default_region
   ```

### Azure Configuration

1. **Create an Azure Service Principal** with Reader role:
   ```bash
   az ad sp create-for-rbac --name "CloudCostOptimizer" --role "Reader" --scopes /subscriptions/{subscription-id}
   ```

2. **Configure credentials** in the application settings:
   ```
   AZURE_TENANT_ID=your_tenant_id
   AZURE_CLIENT_ID=your_client_id
   AZURE_CLIENT_SECRET=your_client_secret
   AZURE_SUBSCRIPTION_ID=your_subscription_id
   ```

### GCP Configuration

1. **Create a service account** with the following roles:
   - `roles/compute.viewer`
   - `roles/storage.objectViewer`
   - `roles/cloudsql.viewer`
   - `roles/billing.viewer`

2. **Generate a service account key** (JSON format).

3. **Configure the service account key path**:
   ```
   GOOGLE_APPLICATION_CREDENTIALS=path/to/service-account-key.json
   ```

## Action Execution Permissions

To enable the tool to take actions (modify, delete, scale resources), additional permissions are required:

### AWS Action Permissions
- `AmazonEC2FullAccess`
- `AmazonS3FullAccess`
- `AmazonRDSFullAccess`

### Azure Action Permissions
- `Contributor` role on target resources

### GCP Action Permissions
- `roles/compute.admin`
- `roles/storage.admin`
- `roles/cloudsql.admin`

## Terraform Integration

1. **Install Terraform** (version 1.0.0 or higher).

2. **Configure provider authentication** for each cloud provider as described above.

3. **Set Terraform directories** in the application configuration:
   ```
   TERRAFORM_TEMPLATES_DIR=/path/to/terraform/templates
   TERRAFORM_STATE_DIR=/path/to/terraform/state
   ```

## Security Considerations

1. **API Keys and Secrets**: Store securely using environment variables or a secrets manager.

2. **Network Security**: Deploy behind a reverse proxy with HTTPS enabled.

3. **Authentication**: Configure user authentication using OAuth, OIDC, or LDAP.

4. **Action Approval**: Enable approval workflows for cost-impacting actions.

## Troubleshooting

### Common Issues

1. **Connection errors to cloud providers**:
   - Verify credentials are correct
   - Check network connectivity
   - Ensure IAM permissions are properly configured

2. **Database connection issues**:
   - Verify database credentials
   - Check database server is running
   - Ensure firewall allows connections

3. **Terraform execution failures**:
   - Check Terraform installation
   - Verify provider authentication
   - Review Terraform logs for specific errors

### Logs

- **Backend logs**: Located in `logs/backend.log`
- **Frontend build logs**: Located in `src/ui/dashboard/build-log.txt`
- **Terraform logs**: Located in `terraform/logs/`

## Extending the Solution

The Cloud Cost Optimizer is designed to be extensible:

1. **Adding new cloud providers**:
   - Implement the provider interface in `src/providers/`
   - Register the new provider in `src/providers/__init__.py`

2. **Adding new recommendation types**:
   - Implement the recommendation algorithm in `src/automation/recommendation/`
   - Register in `src/automation/recommendation/__init__.py`

3. **Adding new action types**:
   - Implement the action executor in `src/automation/execution/`
   - Register in `src/automation/execution/__init__.py`

4. **Customizing the UI**:
   - Frontend components are in `src/ui/dashboard/src/components/`
   - Themes can be modified in `src/ui/dashboard/src/lib/theme.ts`

## Support and Resources

- **Documentation**: Full documentation is available in the `docs/` directory
- **Issue Tracker**: Report issues on the project's GitHub repository
- **Community Forum**: Join our community at [forum.cloudcostoptimizer.com](https://forum.cloudcostoptimizer.com)

## License

This project is licensed under the MIT License - see the LICENSE file for details.

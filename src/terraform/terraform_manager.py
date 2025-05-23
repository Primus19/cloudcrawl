"""
Terraform Template Manager for Cloud Cost Optimizer.
Handles template management, deployment, and cost estimation.
"""
import os
import json
import yaml
import subprocess
import tempfile
import shutil
from typing import Dict, Any, Optional, List
import logging
import psycopg2
from psycopg2.extras import RealDictCursor
import uuid

class TerraformManager:
    """
    Manages Terraform templates, deployments, and cost estimation.
    """
    
    def __init__(self, db_connection_string: str, templates_dir: str, state_dir: str):
        """
        Initialize the Terraform Manager.
        
        Args:
            db_connection_string: PostgreSQL connection string
            templates_dir: Directory for storing Terraform templates
            state_dir: Directory for storing Terraform state files
        """
        self.db_connection_string = db_connection_string
        self.templates_dir = templates_dir
        self.state_dir = state_dir
        self.logger = logging.getLogger(__name__)
        
        # Create directories if they don't exist
        os.makedirs(self.templates_dir, exist_ok=True)
        os.makedirs(self.state_dir, exist_ok=True)
    
    def _get_db_connection(self):
        """Get a database connection."""
        return psycopg2.connect(self.db_connection_string)
    
    def create_template(self, name: str, description: str, provider: str, service_type: str, template_content: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new Terraform template.
        
        Args:
            name: Template name
            description: Template description
            provider: Cloud provider (aws, gcp, azure)
            service_type: Service type (ec2, s3, rds, etc.)
            template_content: Terraform template content
            variables: Template variables
            
        Returns:
            Dictionary containing template information
        """
        # Validate template
        validation_result = self._validate_template(template_content, variables)
        if not validation_result['valid']:
            raise ValueError(f"Invalid template: {validation_result['error']}")
        
        # Store template in database
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO terraform_templates 
                    (name, description, provider, service_type, template_content, variables, version)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    RETURNING id, name, description, provider, service_type, variables, version, created_at, updated_at
                    """,
                    (
                        name,
                        description,
                        provider,
                        service_type,
                        template_content,
                        json.dumps(variables),
                        '1.0.0'
                    )
                )
                template = cursor.fetchone()
                conn.commit()
                
                # Convert variables from JSON string to dictionary
                template['variables'] = json.loads(template['variables']) if template['variables'] else {}
                
                return dict(template)
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
        
        # Store template file
        template_dir = os.path.join(self.templates_dir, str(template['id']))
        os.makedirs(template_dir, exist_ok=True)
        
        with open(os.path.join(template_dir, 'main.tf'), 'w') as f:
            f.write(template_content)
        
        # Create variables file
        with open(os.path.join(template_dir, 'variables.tf'), 'w') as f:
            for var_name, var_info in variables.items():
                f.write(f'variable "{var_name}" {{\n')
                f.write(f'  description = "{var_info.get("description", "")}"\n')
                f.write(f'  type        = {var_info.get("type", "string")}\n')
                if 'default' in var_info:
                    default_value = var_info['default']
                    if isinstance(default_value, str):
                        f.write(f'  default     = "{default_value}"\n')
                    else:
                        f.write(f'  default     = {default_value}\n')
                f.write('}\n\n')
    
    def get_templates(self, provider: Optional[str] = None, service_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all templates.
        
        Args:
            provider: Filter by provider (optional)
            service_type: Filter by service type (optional)
            
        Returns:
            List of dictionaries containing template information
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT id, name, description, provider, service_type, variables, version, created_at, updated_at FROM terraform_templates"
                params = []
                
                if provider:
                    query += " WHERE provider = %s"
                    params.append(provider)
                    
                    if service_type:
                        query += " AND service_type = %s"
                        params.append(service_type)
                elif service_type:
                    query += " WHERE service_type = %s"
                    params.append(service_type)
                
                cursor.execute(query, params)
                templates = cursor.fetchall()
                
                # Convert variables from JSON string to dictionary
                for template in templates:
                    template['variables'] = json.loads(template['variables']) if template['variables'] else {}
                
                return [dict(template) for template in templates]
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_template(self, template_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a template by ID.
        
        Args:
            template_id: Template ID
            
        Returns:
            Dictionary containing template information, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    SELECT id, name, description, provider, service_type, template_content, variables, version, created_at, updated_at 
                    FROM terraform_templates 
                    WHERE id = %s
                    """,
                    (template_id,)
                )
                template = cursor.fetchone()
                
                if not template:
                    return None
                
                # Convert variables from JSON string to dictionary
                template['variables'] = json.loads(template['variables']) if template['variables'] else {}
                
                return dict(template)
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def update_template(self, template_id: int, name: Optional[str] = None, description: Optional[str] = None, 
                        template_content: Optional[str] = None, variables: Optional[Dict[str, Any]] = None) -> Optional[Dict[str, Any]]:
        """
        Update a template.
        
        Args:
            template_id: Template ID
            name: New template name (optional)
            description: New template description (optional)
            template_content: New template content (optional)
            variables: New template variables (optional)
            
        Returns:
            Updated template information, or None if not found
        """
        # Get existing template
        template = self.get_template(template_id)
        if not template:
            return None
        
        # Validate template if content or variables are updated
        if template_content or variables:
            content = template_content if template_content is not None else template['template_content']
            vars_dict = variables if variables is not None else template['variables']
            
            validation_result = self._validate_template(content, vars_dict)
            if not validation_result['valid']:
                raise ValueError(f"Invalid template: {validation_result['error']}")
        
        # Update template in database
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "UPDATE terraform_templates SET updated_at = NOW()"
                params = []
                
                if name:
                    query += ", name = %s"
                    params.append(name)
                
                if description:
                    query += ", description = %s"
                    params.append(description)
                
                if template_content:
                    query += ", template_content = %s"
                    params.append(template_content)
                
                if variables:
                    query += ", variables = %s"
                    params.append(json.dumps(variables))
                
                query += " WHERE id = %s RETURNING id, name, description, provider, service_type, variables, version, created_at, updated_at"
                params.append(template_id)
                
                cursor.execute(query, params)
                updated_template = cursor.fetchone()
                conn.commit()
                
                if not updated_template:
                    return None
                
                # Convert variables from JSON string to dictionary
                updated_template['variables'] = json.loads(updated_template['variables']) if updated_template['variables'] else {}
                
                return dict(updated_template)
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
        
        # Update template file if content was updated
        if template_content:
            template_dir = os.path.join(self.templates_dir, str(template_id))
            os.makedirs(template_dir, exist_ok=True)
            
            with open(os.path.join(template_dir, 'main.tf'), 'w') as f:
                f.write(template_content)
        
        # Update variables file if variables were updated
        if variables:
            template_dir = os.path.join(self.templates_dir, str(template_id))
            os.makedirs(template_dir, exist_ok=True)
            
            with open(os.path.join(template_dir, 'variables.tf'), 'w') as f:
                for var_name, var_info in variables.items():
                    f.write(f'variable "{var_name}" {{\n')
                    f.write(f'  description = "{var_info.get("description", "")}"\n')
                    f.write(f'  type        = {var_info.get("type", "string")}\n')
                    if 'default' in var_info:
                        default_value = var_info['default']
                        if isinstance(default_value, str):
                            f.write(f'  default     = "{default_value}"\n')
                        else:
                            f.write(f'  default     = {default_value}\n')
                    f.write('}\n\n')
    
    def delete_template(self, template_id: int) -> bool:
        """
        Delete a template.
        
        Args:
            template_id: Template ID
            
        Returns:
            True if template was deleted, False if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    "DELETE FROM terraform_templates WHERE id = %s",
                    (template_id,)
                )
                conn.commit()
                return cursor.rowcount > 0
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
        
        # Delete template directory
        template_dir = os.path.join(self.templates_dir, str(template_id))
        if os.path.exists(template_dir):
            shutil.rmtree(template_dir)
    
    def estimate_cost(self, template_id: int, variables_values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Estimate the cost of a template.
        
        Args:
            template_id: Template ID
            variables_values: Values for template variables
            
        Returns:
            Dictionary containing cost estimation
        """
        # Get template
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Create temporary directory for Terraform files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create main.tf file
            with open(os.path.join(temp_dir, 'main.tf'), 'w') as f:
                f.write(template['template_content'])
            
            # Create variables.tf file
            with open(os.path.join(temp_dir, 'variables.tf'), 'w') as f:
                for var_name, var_info in template['variables'].items():
                    f.write(f'variable "{var_name}" {{\n')
                    f.write(f'  description = "{var_info.get("description", "")}"\n')
                    f.write(f'  type        = {var_info.get("type", "string")}\n')
                    if 'default' in var_info:
                        default_value = var_info['default']
                        if isinstance(default_value, str):
                            f.write(f'  default     = "{default_value}"\n')
                        else:
                            f.write(f'  default     = {default_value}\n')
                    f.write('}\n\n')
            
            # Create terraform.tfvars file
            with open(os.path.join(temp_dir, 'terraform.tfvars'), 'w') as f:
                for var_name, var_value in variables_values.items():
                    if isinstance(var_value, str):
                        f.write(f'{var_name} = "{var_value}"\n')
                    else:
                        f.write(f'{var_name} = {var_value}\n')
            
            # Initialize Terraform
            subprocess.run(['terraform', 'init'], cwd=temp_dir, check=True, capture_output=True)
            
            # Run cost estimation
            try:
                # Use Terraform plan with cost estimation plugin
                # Note: This is a simplified example. In a real implementation, you would use a cost estimation tool like Infracost
                result = subprocess.run(['terraform', 'plan', '-out=plan.tfplan'], cwd=temp_dir, check=True, capture_output=True)
                
                # Parse cost estimation
                # This is a placeholder for actual cost estimation logic
                cost_estimate = {
                    'monthly_cost': 100.0,  # Placeholder value
                    'currency': 'USD',
                    'resources': [
                        {
                            'name': 'Example Resource',
                            'monthly_cost': 100.0,
                            'currency': 'USD'
                        }
                    ]
                }
                
                return {
                    'success': True,
                    'estimate': cost_estimate
                }
            except subprocess.CalledProcessError as e:
                return {
                    'success': False,
                    'error': e.stderr.decode('utf-8')
                }
    
    def deploy_template(self, template_id: int, account_id: int, variables_values: Dict[str, Any]) -> Dict[str, Any]:
        """
        Deploy a template.
        
        Args:
            template_id: Template ID
            account_id: Account ID
            variables_values: Values for template variables
            
        Returns:
            Dictionary containing deployment information
        """
        # Get template
        template = self.get_template(template_id)
        if not template:
            raise ValueError(f"Template {template_id} not found")
        
        # Create deployment record
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    """
                    INSERT INTO terraform_deployments 
                    (template_id, account_id, status, variables_used)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id
                    """,
                    (
                        template_id,
                        account_id,
                        'planning',
                        json.dumps(variables_values)
                    )
                )
                deployment = cursor.fetchone()
                conn.commit()
                deployment_id = deployment['id']
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
        
        # Create deployment directory
        deployment_dir = os.path.join(self.state_dir, str(deployment_id))
        os.makedirs(deployment_dir, exist_ok=True)
        
        # Create main.tf file
        with open(os.path.join(deployment_dir, 'main.tf'), 'w') as f:
            f.write(template['template_content'])
        
        # Create variables.tf file
        with open(os.path.join(deployment_dir, 'variables.tf'), 'w') as f:
            for var_name, var_info in template['variables'].items():
                f.write(f'variable "{var_name}" {{\n')
                f.write(f'  description = "{var_info.get("description", "")}"\n')
                f.write(f'  type        = {var_info.get("type", "string")}\n')
                if 'default' in var_info:
                    default_value = var_info['default']
                    if isinstance(default_value, str):
                        f.write(f'  default     = "{default_value}"\n')
                    else:
                        f.write(f'  default     = {default_value}\n')
                f.write('}\n\n')
        
        # Create terraform.tfvars file
        with open(os.path.join(deployment_dir, 'terraform.tfvars'), 'w') as f:
            for var_name, var_value in variables_values.items():
                if isinstance(var_value, str):
                    f.write(f'{var_name} = "{var_value}"\n')
                else:
                    f.write(f'{var_name} = {var_value}\n')
        
        # Initialize Terraform
        try:
            subprocess.run(['terraform', 'init'], cwd=deployment_dir, check=True, capture_output=True)
            
            # Update deployment status
            self._update_deployment_status(deployment_id, 'planned')
            
            return {
                'success': True,
                'deployment_id': deployment_id,
                'status': 'planned',
                'message': 'Deployment planned successfully'
            }
        except subprocess.CalledProcessError as e:
            # Update deployment status
            self._update_deployment_status(deployment_id, 'error', e.stderr.decode('utf-8'))
            
            return {
                'success': False,
                'deployment_id': deployment_id,
                'status': 'error',
                'error': e.stderr.decode('utf-8')
            }
    
    def apply_deployment(self, deployment_id: int) -> Dict[str, Any]:
        """
        Apply a deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Dictionary containing deployment information
        """
        # Get deployment
        deployment = self.get_deployment(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        if deployment['status'] not in ['planned', 'error']:
            raise ValueError(f"Deployment {deployment_id} is not in a valid state for applying")
        
        # Apply deployment
        deployment_dir = os.path.join(self.state_dir, str(deployment_id))
        if not os.path.exists(deployment_dir):
            raise ValueError(f"Deployment directory {deployment_dir} not found")
        
        try:
            # Apply Terraform configuration
            result = subprocess.run(['terraform', 'apply', '-auto-approve'], cwd=deployment_dir, check=True, capture_output=True)
            
            # Get output
            output_result = subprocess.run(['terraform', 'output', '-json'], cwd=deployment_dir, check=True, capture_output=True)
            output = json.loads(output_result.stdout.decode('utf-8'))
            
            # Update deployment status
            self._update_deployment_status(deployment_id, 'applied', result.stdout.decode('utf-8'), output)
            
            return {
                'success': True,
                'deployment_id': deployment_id,
                'status': 'applied',
                'message': 'Deployment applied successfully',
                'output': output
            }
        except subprocess.CalledProcessError as e:
            # Update deployment status
            self._update_deployment_status(deployment_id, 'error', e.stderr.decode('utf-8'))
            
            return {
                'success': False,
                'deployment_id': deployment_id,
                'status': 'error',
                'error': e.stderr.decode('utf-8')
            }
    
    def destroy_deployment(self, deployment_id: int) -> Dict[str, Any]:
        """
        Destroy a deployment.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Dictionary containing deployment information
        """
        # Get deployment
        deployment = self.get_deployment(deployment_id)
        if not deployment:
            raise ValueError(f"Deployment {deployment_id} not found")
        
        # Destroy deployment
        deployment_dir = os.path.join(self.state_dir, str(deployment_id))
        if not os.path.exists(deployment_dir):
            raise ValueError(f"Deployment directory {deployment_dir} not found")
        
        try:
            # Destroy Terraform configuration
            result = subprocess.run(['terraform', 'destroy', '-auto-approve'], cwd=deployment_dir, check=True, capture_output=True)
            
            # Update deployment status
            self._update_deployment_status(deployment_id, 'destroyed', result.stdout.decode('utf-8'))
            
            return {
                'success': True,
                'deployment_id': deployment_id,
                'status': 'destroyed',
                'message': 'Deployment destroyed successfully'
            }
        except subprocess.CalledProcessError as e:
            # Update deployment status
            self._update_deployment_status(deployment_id, 'error', e.stderr.decode('utf-8'))
            
            return {
                'success': False,
                'deployment_id': deployment_id,
                'status': 'error',
                'error': e.stderr.decode('utf-8')
            }
    
    def get_deployments(self, account_id: Optional[int] = None, template_id: Optional[int] = None, status: Optional[str] = None) -> List[Dict[str, Any]]:
        """
        Get all deployments.
        
        Args:
            account_id: Filter by account ID (optional)
            template_id: Filter by template ID (optional)
            status: Filter by status (optional)
            
        Returns:
            List of dictionaries containing deployment information
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                query = "SELECT * FROM terraform_deployments"
                params = []
                
                conditions = []
                if account_id:
                    conditions.append("account_id = %s")
                    params.append(account_id)
                
                if template_id:
                    conditions.append("template_id = %s")
                    params.append(template_id)
                
                if status:
                    conditions.append("status = %s")
                    params.append(status)
                
                if conditions:
                    query += " WHERE " + " AND ".join(conditions)
                
                cursor.execute(query, params)
                deployments = cursor.fetchall()
                
                # Convert JSON strings to dictionaries
                for deployment in deployments:
                    deployment['variables_used'] = json.loads(deployment['variables_used']) if deployment['variables_used'] else {}
                    deployment['cost_estimate'] = json.loads(deployment['cost_estimate']) if deployment['cost_estimate'] else {}
                
                return [dict(deployment) for deployment in deployments]
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def get_deployment(self, deployment_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a deployment by ID.
        
        Args:
            deployment_id: Deployment ID
            
        Returns:
            Dictionary containing deployment information, or None if not found
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(
                    "SELECT * FROM terraform_deployments WHERE id = %s",
                    (deployment_id,)
                )
                deployment = cursor.fetchone()
                
                if not deployment:
                    return None
                
                # Convert JSON strings to dictionaries
                deployment['variables_used'] = json.loads(deployment['variables_used']) if deployment['variables_used'] else {}
                deployment['cost_estimate'] = json.loads(deployment['cost_estimate']) if deployment['cost_estimate'] else {}
                
                return dict(deployment)
        except Exception as e:
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def _update_deployment_status(self, deployment_id: int, status: str, output: str = None, state: Dict[str, Any] = None) -> None:
        """
        Update deployment status.
        
        Args:
            deployment_id: Deployment ID
            status: New status
            output: Command output (optional)
            state: Terraform state (optional)
        """
        conn = self._get_db_connection()
        try:
            with conn.cursor() as cursor:
                query = "UPDATE terraform_deployments SET status = %s, updated_at = NOW()"
                params = [status]
                
                if output:
                    query += ", output = %s"
                    params.append(output)
                
                if state:
                    query += ", state_file = %s"
                    params.append(json.dumps(state))
                
                query += " WHERE id = %s"
                params.append(deployment_id)
                
                cursor.execute(query, params)
                conn.commit()
        except Exception as e:
            conn.rollback()
            self.logger.error(f"Database error: {str(e)}")
            raise
        finally:
            conn.close()
    
    def _validate_template(self, template_content: str, variables: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate a Terraform template.
        
        Args:
            template_content: Template content
            variables: Template variables
            
        Returns:
            Dictionary containing validation results
        """
        # Create temporary directory for Terraform files
        with tempfile.TemporaryDirectory() as temp_dir:
            # Create main.tf file
            with open(os.path.join(temp_dir, 'main.tf'), 'w') as f:
                f.write(template_content)
            
            # Create variables.tf file
            with open(os.path.join(temp_dir, 'variables.tf'), 'w') as f:
                for var_name, var_info in variables.items():
                    f.write(f'variable "{var_name}" {{\n')
                    f.write(f'  description = "{var_info.get("description", "")}"\n')
                    f.write(f'  type        = {var_info.get("type", "string")}\n')
                    if 'default' in var_info:
                        default_value = var_info['default']
                        if isinstance(default_value, str):
                            f.write(f'  default     = "{default_value}"\n')
                        else:
                            f.write(f'  default     = {default_value}\n')
                    f.write('}\n\n')
            
            # Initialize Terraform
            try:
                subprocess.run(['terraform', 'init'], cwd=temp_dir, check=True, capture_output=True)
                
                # Validate template
                subprocess.run(['terraform', 'validate'], cwd=temp_dir, check=True, capture_output=True)
                
                return {
                    'valid': True
                }
            except subprocess.CalledProcessError as e:
                return {
                    'valid': False,
                    'error': e.stderr.decode('utf-8')
                }

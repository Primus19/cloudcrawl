"""
Terraform integration service.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import json

from src.core.repositories.base import BaseRepository
from src.core.models.terraform import TerraformState, TerraformModule, TerraformTemplate


class TerraformService:
    """Service for Terraform integration."""
    
    def __init__(self, 
                 terraform_state_repository: BaseRepository[TerraformState],
                 terraform_module_repository: BaseRepository[TerraformModule],
                 terraform_template_repository: BaseRepository[TerraformTemplate]):
        self.terraform_state_repository = terraform_state_repository
        self.terraform_module_repository = terraform_module_repository
        self.terraform_template_repository = terraform_template_repository
    
    # Terraform State Management
    
    def create_or_update_state(self, 
                             organization_id: UUID, 
                             name: str,
                             state_data: Dict[str, Any],
                             version: str) -> TerraformState:
        """Create or update a Terraform state."""
        # Check if state already exists
        existing_states = self.terraform_state_repository.filter_by(
            organization_id=organization_id,
            name=name
        )
        
        if existing_states:
            # Update existing state
            state = existing_states[0]
            state.state_data = state_data
            state.version = version
            return self.terraform_state_repository.update(state)
        else:
            # Create new state
            state = TerraformState(
                organization_id=organization_id,
                name=name,
                state_data=state_data,
                version=version
            )
            return self.terraform_state_repository.create(state)
    
    def get_state(self, state_id: UUID) -> Optional[TerraformState]:
        """Get a Terraform state by ID."""
        return self.terraform_state_repository.get_by_id(state_id)
    
    def get_states_by_organization(self, organization_id: UUID) -> List[TerraformState]:
        """Get all Terraform states for an organization."""
        return self.terraform_state_repository.filter_by(organization_id=organization_id)
    
    def delete_state(self, state_id: UUID) -> bool:
        """Delete a Terraform state by ID."""
        return self.terraform_state_repository.delete(state_id)
    
    def extract_resources_from_state(self, state_id: UUID) -> List[Dict[str, Any]]:
        """Extract resources from a Terraform state."""
        state = self.terraform_state_repository.get_by_id(state_id)
        if not state:
            raise ValueError(f"Terraform state with ID {state_id} not found")
        
        resources = []
        
        # Extract resources from state data
        # This is a simplified implementation that assumes a specific state format
        if 'resources' in state.state_data:
            for resource in state.state_data['resources']:
                resource_type = resource.get('type', '')
                resource_name = resource.get('name', '')
                
                if 'instances' in resource:
                    for instance in resource['instances']:
                        attributes = instance.get('attributes', {})
                        resources.append({
                            'type': resource_type,
                            'name': resource_name,
                            'id': attributes.get('id', ''),
                            'attributes': attributes
                        })
        
        return resources
    
    # Terraform Module Management
    
    def create_module(self, 
                    organization_id: UUID, 
                    name: str,
                    source_type: str,
                    source_url: str,
                    description: str = None,
                    version: str = None,
                    variables: Dict[str, Any] = None) -> TerraformModule:
        """Create a new Terraform module."""
        module = TerraformModule(
            organization_id=organization_id,
            name=name,
            description=description,
            source_type=source_type,
            source_url=source_url,
            version=version,
            variables=variables,
            is_optimized=False
        )
        return self.terraform_module_repository.create(module)
    
    def get_module(self, module_id: UUID) -> Optional[TerraformModule]:
        """Get a Terraform module by ID."""
        return self.terraform_module_repository.get_by_id(module_id)
    
    def get_modules_by_organization(self, organization_id: UUID) -> List[TerraformModule]:
        """Get all Terraform modules for an organization."""
        return self.terraform_module_repository.filter_by(organization_id=organization_id)
    
    def update_module(self, module: TerraformModule) -> TerraformModule:
        """Update a Terraform module."""
        return self.terraform_module_repository.update(module)
    
    def delete_module(self, module_id: UUID) -> bool:
        """Delete a Terraform module by ID."""
        return self.terraform_module_repository.delete(module_id)
    
    # Terraform Template Management
    
    def create_template(self, 
                      organization_id: UUID, 
                      name: str,
                      content: str,
                      description: str = None,
                      variables: Dict[str, Any] = None) -> TerraformTemplate:
        """Create a new Terraform template."""
        template = TerraformTemplate(
            organization_id=organization_id,
            name=name,
            description=description,
            content=content,
            variables=variables,
            optimization_status='not_analyzed'
        )
        return self.terraform_template_repository.create(template)
    
    def get_template(self, template_id: UUID) -> Optional[TerraformTemplate]:
        """Get a Terraform template by ID."""
        return self.terraform_template_repository.get_by_id(template_id)
    
    def get_templates_by_organization(self, organization_id: UUID) -> List[TerraformTemplate]:
        """Get all Terraform templates for an organization."""
        return self.terraform_template_repository.filter_by(organization_id=organization_id)
    
    def update_template(self, template: TerraformTemplate) -> TerraformTemplate:
        """Update a Terraform template."""
        return self.terraform_template_repository.update(template)
    
    def delete_template(self, template_id: UUID) -> bool:
        """Delete a Terraform template by ID."""
        return self.terraform_template_repository.delete(template_id)
    
    def analyze_template_cost(self, template_id: UUID) -> Dict[str, Any]:
        """Analyze the cost of a Terraform template."""
        template = self.terraform_template_repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Terraform template with ID {template_id} not found")
        
        # This would involve parsing the template and estimating costs
        # For now, we'll implement a simplified version
        
        # Parse template to extract resources
        resources = self._parse_template(template.content)
        
        # Estimate costs for each resource
        total_cost = 0
        resource_costs = []
        
        for resource in resources:
            # In a real implementation, this would use pricing APIs or databases
            cost = self._estimate_resource_cost(resource)
            total_cost += cost
            
            resource_costs.append({
                'resource_type': resource['type'],
                'resource_name': resource['name'],
                'monthly_cost': cost
            })
        
        # Update template with estimated cost
        template.estimated_cost = {
            'total_monthly_cost': total_cost,
            'resource_costs': resource_costs,
            'currency': 'USD'
        }
        template.optimization_status = 'analyzed'
        self.terraform_template_repository.update(template)
        
        return template.estimated_cost
    
    def optimize_template(self, template_id: UUID) -> Dict[str, Any]:
        """Optimize a Terraform template for cost efficiency."""
        template = self.terraform_template_repository.get_by_id(template_id)
        if not template:
            raise ValueError(f"Terraform template with ID {template_id} not found")
        
        if template.optimization_status == 'not_analyzed':
            # Analyze first if not already done
            self.analyze_template_cost(template_id)
            template = self.terraform_template_repository.get_by_id(template_id)
        
        # Parse template
        resources = self._parse_template(template.content)
        
        # Generate optimization suggestions
        optimizations = []
        optimized_content = template.content
        
        for resource in resources:
            # In a real implementation, this would use more sophisticated analysis
            optimization = self._generate_resource_optimization(resource)
            if optimization:
                optimizations.append(optimization)
                
                # Apply optimization to content
                if 'replacement' in optimization:
                    optimized_content = optimized_content.replace(
                        optimization['original_block'],
                        optimization['replacement']
                    )
        
        # Calculate savings
        original_cost = template.estimated_cost['total_monthly_cost'] if template.estimated_cost else 0
        optimized_cost = original_cost
        
        for opt in optimizations:
            if 'savings' in opt:
                optimized_cost -= opt['savings']
        
        # Create a new optimized template
        optimized_template = TerraformTemplate(
            organization_id=template.organization_id,
            name=f"{template.name} (Optimized)",
            description=f"Optimized version of {template.name}",
            content=optimized_content,
            variables=template.variables,
            optimization_status='optimized',
            estimated_cost={
                'total_monthly_cost': optimized_cost,
                'original_monthly_cost': original_cost,
                'savings': original_cost - optimized_cost,
                'savings_percentage': ((original_cost - optimized_cost) / original_cost * 100) if original_cost > 0 else 0,
                'currency': 'USD'
            }
        )
        
        optimized_template = self.terraform_template_repository.create(optimized_template)
        
        return {
            'original_template_id': str(template_id),
            'optimized_template_id': str(optimized_template.id),
            'optimizations': optimizations,
            'savings': original_cost - optimized_cost,
            'savings_percentage': ((original_cost - optimized_cost) / original_cost * 100) if original_cost > 0 else 0
        }
    
    # Helper methods
    
    def _parse_template(self, content: str) -> List[Dict[str, Any]]:
        """Parse a Terraform template to extract resources."""
        # This is a simplified implementation
        # In a real implementation, this would use a proper HCL parser
        
        resources = []
        lines = content.split('\n')
        
        i = 0
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for resource blocks
            if line.startswith('resource'):
                parts = line.split('"')
                if len(parts) >= 5:
                    resource_type = parts[1]
                    resource_name = parts[3]
                    
                    # Find the block content
                    block_start = i
                    block_end = i
                    block_content = ""
                    brace_count = 0
                    
                    # Find the matching closing brace
                    for j in range(i, len(lines)):
                        block_content += lines[j] + "\n"
                        
                        for char in lines[j]:
                            if char == '{':
                                brace_count += 1
                            elif char == '}':
                                brace_count -= 1
                        
                        if brace_count == 0 and '{' in lines[j]:
                            # This is a single-line block
                            block_end = j
                            break
                        elif brace_count == 0 and j > i:
                            # We found the closing brace
                            block_end = j
                            break
                    
                    resources.append({
                        'type': resource_type,
                        'name': resource_name,
                        'block_start': block_start,
                        'block_end': block_end,
                        'content': block_content,
                        'attributes': self._extract_attributes(block_content)
                    })
                    
                    i = block_end
            
            i += 1
        
        return resources
    
    def _extract_attributes(self, block_content: str) -> Dict[str, Any]:
        """Extract attributes from a resource block."""
        # This is a simplified implementation
        attributes = {}
        lines = block_content.split('\n')
        
        for line in lines:
            line = line.strip()
            if '=' in line and not line.startswith('#'):
                parts = line.split('=', 1)
                if len(parts) == 2:
                    key = parts[0].strip()
                    value = parts[1].strip()
                    
                    # Remove quotes and trailing comments
                    if value.startswith('"') and '"' in value[1:]:
                        value = value[1:value[1:].index('"')+1]
                    elif value.startswith('"'):
                        value = value[1:]
                    
                    if '#' in value:
                        value = value[:value.index('#')].strip()
                    
                    attributes[key] = value
        
        return attributes
    
    def _estimate_resource_cost(self, resource: Dict[str, Any]) -> float:
        """Estimate the monthly cost of a resource."""
        # This is a simplified implementation with hardcoded costs
        # In a real implementation, this would use pricing APIs
        
        resource_type = resource['type']
        attributes = resource['attributes']
        
        if resource_type == 'aws_instance':
            instance_type = attributes.get('instance_type', 't3.micro')
            
            # Simplified pricing
            pricing = {
                't3.micro': 8.50,
                't3.small': 17.00,
                't3.medium': 34.00,
                't3.large': 68.00,
                't3.xlarge': 136.00,
                't3.2xlarge': 272.00,
                'm5.large': 77.00,
                'm5.xlarge': 154.00,
                'm5.2xlarge': 308.00,
                'm5.4xlarge': 616.00,
                'c5.large': 85.00,
                'c5.xlarge': 170.00,
                'c5.2xlarge': 340.00,
                'r5.large': 126.00,
                'r5.xlarge': 252.00,
                'r5.2xlarge': 504.00
            }
            
            return pricing.get(instance_type, 30.00)  # Default if unknown
            
        elif resource_type == 'aws_db_instance':
            instance_class = attributes.get('instance_class', 'db.t3.micro')
            storage = float(attributes.get('allocated_storage', 20))
            
            # Simplified pricing
            instance_pricing = {
                'db.t3.micro': 12.50,
                'db.t3.small': 25.00,
                'db.t3.medium': 50.00,
                'db.t3.large': 100.00,
                'db.m5.large': 130.00,
                'db.m5.xlarge': 260.00,
                'db.r5.large': 175.00,
                'db.r5.xlarge': 350.00
            }
            
            storage_cost = storage * 0.10  # $0.10 per GB
            instance_cost = instance_pricing.get(instance_class, 50.00)
            
            return storage_cost + instance_cost
            
        elif resource_type == 'aws_s3_bucket':
            # Simplified S3 pricing
            return 5.00  # Assume some baseline storage
            
        elif resource_type == 'azurerm_virtual_machine':
            size = attributes.get('vm_size', 'Standard_B1s')
            
            # Simplified pricing
            pricing = {
                'Standard_B1s': 8.76,
                'Standard_B2s': 35.04,
                'Standard_D2s_v3': 70.08,
                'Standard_D4s_v3': 140.16,
                'Standard_E2s_v3': 87.60,
                'Standard_E4s_v3': 175.20
            }
            
            return pricing.get(size, 40.00)  # Default if unknown
            
        elif resource_type == 'google_compute_instance':
            machine_type = attributes.get('machine_type', 'e2-micro')
            
            # Simplified pricing
            pricing = {
                'e2-micro': 7.60,
                'e2-small': 15.20,
                'e2-medium': 30.40,
                'n1-standard-1': 25.00,
                'n1-standard-2': 50.00,
                'n1-standard-4': 100.00,
                'n1-standard-8': 200.00
            }
            
            return pricing.get(machine_type, 30.00)  # Default if unknown
            
        else:
            # Default cost for unknown resource types
            return 10.00
    
    def _generate_resource_optimization(self, resource: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Generate optimization suggestions for a resource."""
        resource_type = resource['type']
        attributes = resource['attributes']
        
        if resource_type == 'aws_instance':
            instance_type = attributes.get('instance_type', '')
            
            # Check for oversized instances
            oversized_mappings = {
                't3.xlarge': 't3.large',
                't3.2xlarge': 't3.xlarge',
                'm5.xlarge': 'm5.large',
                'm5.2xlarge': 'm5.xlarge',
                'm5.4xlarge': 'm5.2xlarge',
                'c5.xlarge': 'c5.large',
                'c5.2xlarge': 'c5.xlarge',
                'r5.xlarge': 'r5.large',
                'r5.2xlarge': 'r5.xlarge'
            }
            
            if instance_type in oversized_mappings:
                recommended_type = oversized_mappings[instance_type]
                original_cost = self._estimate_resource_cost(resource)
                
                # Create a copy of the resource with the recommended instance type
                optimized_resource = resource.copy()
                optimized_resource['attributes'] = attributes.copy()
                optimized_resource['attributes']['instance_type'] = recommended_type
                
                optimized_cost = self._estimate_resource_cost(optimized_resource)
                savings = original_cost - optimized_cost
                
                # Generate replacement content
                original_line = f'instance_type = "{instance_type}"'
                replacement_line = f'instance_type = "{recommended_type}"'
                
                return {
                    'resource_type': resource_type,
                    'resource_name': resource['name'],
                    'optimization_type': 'rightsizing',
                    'current_value': instance_type,
                    'recommended_value': recommended_type,
                    'original_cost': original_cost,
                    'optimized_cost': optimized_cost,
                    'savings': savings,
                    'original_block': original_line,
                    'replacement': replacement_line,
                    'justification': f"Instance appears to be oversized. Rightsizing from {instance_type} to {recommended_type} would save ${savings:.2f}/month."
                }
        
        elif resource_type == 'aws_db_instance':
            instance_class = attributes.get('instance_class', '')
            
            # Check for oversized DB instances
            oversized_mappings = {
                'db.t3.large': 'db.t3.medium',
                'db.m5.large': 'db.t3.large',
                'db.m5.xlarge': 'db.m5.large',
                'db.r5.large': 'db.m5.large',
                'db.r5.xlarge': 'db.r5.large'
            }
            
            if instance_class in oversized_mappings:
                recommended_class = oversized_mappings[instance_class]
                original_cost = self._estimate_resource_cost(resource)
                
                # Create a copy of the resource with the recommended instance class
                optimized_resource = resource.copy()
                optimized_resource['attributes'] = attributes.copy()
                optimized_resource['attributes']['instance_class'] = recommended_class
                
                optimized_cost = self._estimate_resource_cost(optimized_resource)
                savings = original_cost - optimized_cost
                
                # Generate replacement content
                original_line = f'instance_class = "{instance_class}"'
                replacement_line = f'instance_class = "{recommended_class}"'
                
                return {
                    'resource_type': resource_type,
                    'resource_name': resource['name'],
                    'optimization_type': 'rightsizing',
                    'current_value': instance_class,
                    'recommended_value': recommended_class,
                    'original_cost': original_cost,
                    'optimized_cost': optimized_cost,
                    'savings': savings,
                    'original_block': original_line,
                    'replacement': replacement_line,
                    'justification': f"Database instance appears to be oversized. Rightsizing from {instance_class} to {recommended_class} would save ${savings:.2f}/month."
                }
        
        return None

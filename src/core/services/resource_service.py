"""
Cloud account and resource management service.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import datetime

from src.core.repositories.base import BaseRepository
from src.core.models.resource import CloudAccount, Resource, ResourceGroup, Tag


class ResourceService:
    """Service for cloud account and resource management."""
    
    def __init__(self, 
                 cloud_account_repository: BaseRepository[CloudAccount],
                 resource_repository: BaseRepository[Resource],
                 resource_group_repository: BaseRepository[ResourceGroup],
                 tag_repository: BaseRepository[Tag]):
        self.cloud_account_repository = cloud_account_repository
        self.resource_repository = resource_repository
        self.resource_group_repository = resource_group_repository
        self.tag_repository = tag_repository
    
    # Cloud Account Management
    
    def create_cloud_account(self, 
                           organization_id: UUID, 
                           name: str, 
                           provider: str, 
                           account_id: str,
                           credentials: Dict[str, Any] = None) -> CloudAccount:
        """Create a new cloud account."""
        # Check if account already exists
        existing_accounts = self.cloud_account_repository.filter_by(
            organization_id=organization_id,
            provider=provider,
            account_id=account_id
        )
        if existing_accounts:
            raise ValueError(f"Cloud account with provider {provider} and ID {account_id} already exists")
        
        # Create new cloud account
        cloud_account = CloudAccount(
            organization_id=organization_id,
            name=name,
            provider=provider,
            account_id=account_id,
            credentials=credentials,
            status='active'
        )
        return self.cloud_account_repository.create(cloud_account)
    
    def get_cloud_account(self, account_id: UUID) -> Optional[CloudAccount]:
        """Get a cloud account by ID."""
        return self.cloud_account_repository.get_by_id(account_id)
    
    def get_cloud_accounts_by_organization(self, organization_id: UUID) -> List[CloudAccount]:
        """Get all cloud accounts for an organization."""
        return self.cloud_account_repository.filter_by(organization_id=organization_id)
    
    def update_cloud_account(self, account: CloudAccount) -> CloudAccount:
        """Update a cloud account."""
        return self.cloud_account_repository.update(account)
    
    def delete_cloud_account(self, account_id: UUID) -> bool:
        """Delete a cloud account by ID."""
        return self.cloud_account_repository.delete(account_id)
    
    def update_cloud_account_sync_status(self, account_id: UUID) -> CloudAccount:
        """Update the last sync timestamp for a cloud account."""
        account = self.get_cloud_account(account_id)
        if not account:
            raise ValueError(f"Cloud account with ID {account_id} not found")
        
        account.last_sync = datetime.datetime.utcnow()
        return self.cloud_account_repository.update(account)
    
    # Resource Management
    
    def create_or_update_resource(self, 
                                cloud_account_id: UUID, 
                                resource_id: str, 
                                resource_type: str,
                                name: str = None,
                                region: str = None,
                                status: str = None,
                                properties: Dict[str, Any] = None) -> Resource:
        """Create or update a cloud resource."""
        # Check if resource already exists
        existing_resources = self.resource_repository.filter_by(
            cloud_account_id=cloud_account_id,
            resource_id=resource_id
        )
        
        if existing_resources:
            # Update existing resource
            resource = existing_resources[0]
            resource.resource_type = resource_type
            resource.name = name or resource.name
            resource.region = region or resource.region
            resource.status = status or resource.status
            resource.properties = properties or resource.properties
            resource.last_seen = datetime.datetime.utcnow()
            return self.resource_repository.update(resource)
        else:
            # Create new resource
            resource = Resource(
                cloud_account_id=cloud_account_id,
                resource_id=resource_id,
                resource_type=resource_type,
                name=name,
                region=region,
                status=status,
                properties=properties,
                last_seen=datetime.datetime.utcnow()
            )
            return self.resource_repository.create(resource)
    
    def get_resource(self, resource_id: UUID) -> Optional[Resource]:
        """Get a resource by ID."""
        return self.resource_repository.get_by_id(resource_id)
    
    def get_resources_by_cloud_account(self, cloud_account_id: UUID) -> List[Resource]:
        """Get all resources for a cloud account."""
        return self.resource_repository.filter_by(cloud_account_id=cloud_account_id)
    
    def get_resources_by_type(self, cloud_account_id: UUID, resource_type: str) -> List[Resource]:
        """Get resources by type for a cloud account."""
        return self.resource_repository.filter_by(
            cloud_account_id=cloud_account_id,
            resource_type=resource_type
        )
    
    def delete_resource(self, resource_id: UUID) -> bool:
        """Delete a resource by ID."""
        return self.resource_repository.delete(resource_id)
    
    # Resource Group Management
    
    def create_resource_group(self, 
                            cloud_account_id: UUID, 
                            name: str, 
                            description: str = None) -> ResourceGroup:
        """Create a new resource group."""
        # Check if group already exists
        existing_groups = self.resource_group_repository.filter_by(
            cloud_account_id=cloud_account_id,
            name=name
        )
        if existing_groups:
            raise ValueError(f"Resource group with name {name} already exists for this cloud account")
        
        # Create new resource group
        resource_group = ResourceGroup(
            cloud_account_id=cloud_account_id,
            name=name,
            description=description
        )
        return self.resource_group_repository.create(resource_group)
    
    def add_resource_to_group(self, resource_id: UUID, group_id: UUID) -> None:
        """Add a resource to a resource group."""
        resource = self.resource_repository.get_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource with ID {resource_id} not found")
        
        group = self.resource_group_repository.get_by_id(group_id)
        if not group:
            raise ValueError(f"Resource group with ID {group_id} not found")
        
        # Check if resource is already in the group
        if group in resource.resource_groups:
            return  # Already in group, no action needed
        
        # Add resource to group
        resource.resource_groups.append(group)
        self.resource_repository.update(resource)
    
    def remove_resource_from_group(self, resource_id: UUID, group_id: UUID) -> None:
        """Remove a resource from a resource group."""
        resource = self.resource_repository.get_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource with ID {resource_id} not found")
        
        group = self.resource_group_repository.get_by_id(group_id)
        if not group:
            raise ValueError(f"Resource group with ID {group_id} not found")
        
        # Check if resource is in the group
        if group not in resource.resource_groups:
            return  # Not in group, no action needed
        
        # Remove resource from group
        resource.resource_groups.remove(group)
        self.resource_repository.update(resource)
    
    # Tag Management
    
    def add_tag_to_resource(self, resource_id: UUID, key: str, value: str = None) -> Tag:
        """Add a tag to a resource."""
        resource = self.resource_repository.get_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource with ID {resource_id} not found")
        
        # Check if tag already exists
        existing_tags = [tag for tag in resource.tags if tag.key == key]
        if existing_tags:
            # Update existing tag
            tag = existing_tags[0]
            tag.value = value
            return self.tag_repository.update(tag)
        else:
            # Create new tag
            tag = Tag(
                resource_id=resource_id,
                key=key,
                value=value
            )
            return self.tag_repository.create(tag)
    
    def remove_tag_from_resource(self, resource_id: UUID, key: str) -> bool:
        """Remove a tag from a resource."""
        resource = self.resource_repository.get_by_id(resource_id)
        if not resource:
            raise ValueError(f"Resource with ID {resource_id} not found")
        
        # Find tag by key
        for tag in resource.tags:
            if tag.key == key:
                return self.tag_repository.delete(tag.id)
        
        return False  # Tag not found
    
    def get_resources_by_tag(self, cloud_account_id: UUID, key: str, value: str = None) -> List[Resource]:
        """Get resources by tag."""
        # This requires a more complex query with joins
        # For simplicity, we'll implement a basic version
        resources = self.get_resources_by_cloud_account(cloud_account_id)
        
        if value is None:
            # Filter by tag key only
            return [r for r in resources if any(t.key == key for t in r.tags)]
        else:
            # Filter by tag key and value
            return [r for r in resources if any(t.key == key and t.value == value for t in r.tags)]

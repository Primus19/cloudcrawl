"""
Cost analysis and budget management service.
"""
from typing import Optional, List, Dict, Any
from uuid import UUID
import datetime
from decimal import Decimal

from src.core.repositories.base import BaseRepository
from src.core.models.cost import CostData, Budget, BudgetAlert


class CostService:
    """Service for cost analysis and budget management."""
    
    def __init__(self, 
                 cost_data_repository: BaseRepository[CostData],
                 budget_repository: BaseRepository[Budget],
                 budget_alert_repository: BaseRepository[BudgetAlert]):
        self.cost_data_repository = cost_data_repository
        self.budget_repository = budget_repository
        self.budget_alert_repository = budget_alert_repository
    
    # Cost Data Management
    
    def record_cost_data(self, 
                       cloud_account_id: UUID, 
                       timestamp: datetime.datetime,
                       amount: Decimal,
                       currency: str,
                       granularity: str,
                       resource_id: UUID = None,
                       dimensions: Dict[str, Any] = None) -> CostData:
        """Record cost data for a cloud account or resource."""
        cost_data = CostData(
            cloud_account_id=cloud_account_id,
            resource_id=resource_id,
            timestamp=timestamp,
            amount=amount,
            currency=currency,
            granularity=granularity,
            dimensions=dimensions
        )
        return self.cost_data_repository.create(cost_data)
    
    def get_cost_data_by_account(self, 
                               cloud_account_id: UUID, 
                               start_date: datetime.datetime,
                               end_date: datetime.datetime,
                               granularity: str = None) -> List[CostData]:
        """Get cost data for a cloud account within a date range."""
        # This requires a more complex query with date filtering
        # For simplicity, we'll implement a basic version
        all_costs = self.cost_data_repository.filter_by(cloud_account_id=cloud_account_id)
        
        # Filter by date range
        filtered_costs = [
            cost for cost in all_costs 
            if start_date <= cost.timestamp <= end_date
        ]
        
        # Filter by granularity if specified
        if granularity:
            filtered_costs = [cost for cost in filtered_costs if cost.granularity == granularity]
        
        return filtered_costs
    
    def get_cost_data_by_resource(self, 
                                resource_id: UUID, 
                                start_date: datetime.datetime,
                                end_date: datetime.datetime,
                                granularity: str = None) -> List[CostData]:
        """Get cost data for a specific resource within a date range."""
        # This requires a more complex query with date filtering
        # For simplicity, we'll implement a basic version
        all_costs = self.cost_data_repository.filter_by(resource_id=resource_id)
        
        # Filter by date range
        filtered_costs = [
            cost for cost in all_costs 
            if start_date <= cost.timestamp <= end_date
        ]
        
        # Filter by granularity if specified
        if granularity:
            filtered_costs = [cost for cost in filtered_costs if cost.granularity == granularity]
        
        return filtered_costs
    
    def aggregate_costs(self, 
                      cloud_account_id: UUID, 
                      start_date: datetime.datetime,
                      end_date: datetime.datetime,
                      group_by: List[str] = None) -> Dict[str, Any]:
        """Aggregate costs by dimensions."""
        # Get all costs for the account in the date range
        costs = self.get_cost_data_by_account(cloud_account_id, start_date, end_date)
        
        if not group_by:
            # Simple sum if no grouping
            total = sum(cost.amount for cost in costs)
            return {"total": total}
        
        # Group by specified dimensions
        result = {}
        for dimension in group_by:
            dimension_groups = {}
            
            for cost in costs:
                # Skip if dimension not in cost dimensions
                if not cost.dimensions or dimension not in cost.dimensions:
                    continue
                
                dimension_value = str(cost.dimensions[dimension])
                if dimension_value not in dimension_groups:
                    dimension_groups[dimension_value] = Decimal('0')
                
                dimension_groups[dimension_value] += cost.amount
            
            result[dimension] = dimension_groups
        
        return result
    
    # Budget Management
    
    def create_budget(self, 
                    organization_id: UUID, 
                    name: str,
                    amount: Decimal,
                    currency: str,
                    period: str,
                    start_date: datetime.date,
                    end_date: datetime.date = None,
                    filters: Dict[str, Any] = None) -> Budget:
        """Create a new budget."""
        budget = Budget(
            organization_id=organization_id,
            name=name,
            amount=amount,
            currency=currency,
            period=period,
            start_date=start_date,
            end_date=end_date,
            filters=filters
        )
        return self.budget_repository.create(budget)
    
    def get_budget(self, budget_id: UUID) -> Optional[Budget]:
        """Get a budget by ID."""
        return self.budget_repository.get_by_id(budget_id)
    
    def get_budgets_by_organization(self, organization_id: UUID) -> List[Budget]:
        """Get all budgets for an organization."""
        return self.budget_repository.filter_by(organization_id=organization_id)
    
    def update_budget(self, budget: Budget) -> Budget:
        """Update a budget."""
        return self.budget_repository.update(budget)
    
    def delete_budget(self, budget_id: UUID) -> bool:
        """Delete a budget by ID."""
        return self.budget_repository.delete(budget_id)
    
    def create_budget_alert(self, 
                          budget_id: UUID, 
                          threshold: Decimal,
                          notification_channels: Dict[str, Any]) -> BudgetAlert:
        """Create a new budget alert."""
        budget = self.budget_repository.get_by_id(budget_id)
        if not budget:
            raise ValueError(f"Budget with ID {budget_id} not found")
        
        alert = BudgetAlert(
            budget_id=budget_id,
            threshold=threshold,
            notification_channels=notification_channels
        )
        return self.budget_alert_repository.create(alert)
    
    def check_budget_status(self, budget_id: UUID) -> Dict[str, Any]:
        """Check the current status of a budget."""
        budget = self.budget_repository.get_by_id(budget_id)
        if not budget:
            raise ValueError(f"Budget with ID {budget_id} not found")
        
        # Determine current period based on budget period
        today = datetime.date.today()
        if budget.period == 'monthly':
            period_start = datetime.date(today.year, today.month, 1)
            if today.month == 12:
                period_end = datetime.date(today.year + 1, 1, 1) - datetime.timedelta(days=1)
            else:
                period_end = datetime.date(today.year, today.month + 1, 1) - datetime.timedelta(days=1)
        elif budget.period == 'quarterly':
            quarter = (today.month - 1) // 3 + 1
            period_start = datetime.date(today.year, (quarter - 1) * 3 + 1, 1)
            if quarter == 4:
                period_end = datetime.date(today.year + 1, 1, 1) - datetime.timedelta(days=1)
            else:
                period_end = datetime.date(today.year, quarter * 3 + 1, 1) - datetime.timedelta(days=1)
        elif budget.period == 'yearly':
            period_start = datetime.date(today.year, 1, 1)
            period_end = datetime.date(today.year, 12, 31)
        else:
            raise ValueError(f"Unsupported budget period: {budget.period}")
        
        # Apply budget filters to get relevant costs
        # This is a simplified implementation
        filters = budget.filters or {}
        cloud_account_ids = filters.get('cloud_account_ids', [])
        
        # Calculate current spend
        current_spend = Decimal('0')
        for cloud_account_id in cloud_account_ids:
            costs = self.get_cost_data_by_account(
                UUID(cloud_account_id),
                datetime.datetime.combine(period_start, datetime.time.min),
                datetime.datetime.combine(period_end, datetime.time.max)
            )
            for cost in costs:
                if cost.currency == budget.currency:
                    current_spend += cost.amount
        
        # Calculate percentage of budget used
        percentage_used = (current_spend / budget.amount) * 100 if budget.amount > 0 else 0
        
        # Check if any alerts are triggered
        alerts_triggered = []
        for alert in budget.alerts:
            if percentage_used >= alert.threshold:
                alerts_triggered.append({
                    'alert_id': str(alert.id),
                    'threshold': float(alert.threshold),
                    'notification_channels': alert.notification_channels
                })
        
        return {
            'budget_id': str(budget.id),
            'name': budget.name,
            'period_start': period_start.isoformat(),
            'period_end': period_end.isoformat(),
            'amount': float(budget.amount),
            'currency': budget.currency,
            'current_spend': float(current_spend),
            'percentage_used': float(percentage_used),
            'alerts_triggered': alerts_triggered
        }

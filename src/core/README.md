# Cloud Cost Optimizer - Core Module

The Core module provides the fundamental domain models, services, and repositories for the Cloud Cost Optimizer platform. This module is designed to be cloud-provider agnostic, with all provider-specific logic isolated in the providers module.

## Structure

### `/models`
Domain models representing the core entities in the system:
- Users and Organizations
- Cloud Accounts and Resources
- Cost Data and Budgets
- Recommendations and Actions

### `/services`
Business logic and service layer:
- Authentication and Authorization
- Resource Management
- Cost Analysis
- Recommendation Generation

### `/repositories`
Data access layer:
- Database Interactions
- Caching
- External API Clients

## Design Principles

1. **Provider Agnosticism**: Core functionality should be independent of specific cloud providers
2. **Clean Architecture**: Separation of concerns with clear boundaries between layers
3. **Domain-Driven Design**: Models reflect the business domain and encapsulate business rules
4. **Dependency Injection**: Services receive their dependencies through constructor injection
5. **Repository Pattern**: Data access is abstracted behind repository interfaces

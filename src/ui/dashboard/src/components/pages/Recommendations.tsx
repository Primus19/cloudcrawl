import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Card, 
  CardContent, 
  CardHeader, 
  Grid, 
  Divider, 
  Button, 
  Chip, 
  Table, 
  TableBody, 
  TableCell, 
  TableContainer, 
  TableHead, 
  TableRow, 
  Paper,
  TextField,
  MenuItem,
  FormControl,
  InputLabel,
  Select,
  CircularProgress,
  IconButton,
  Tooltip,
  useTheme
} from '@mui/material';
import { 
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Info as InfoIcon
} from '@mui/icons-material';
import { Recommendation, RecommendationFilter } from '../../lib/types';

// Mock data - would be replaced with API calls in production
const mockRecommendations: Recommendation[] = [
  { 
    id: '1', 
    type: 'resize_resource', 
    priority: 'high', 
    status: 'new',
    resourceId: 'i-1234567890abcdef0',
    resourceName: 'prod-api-server-1',
    resourceType: 'ec2_instance',
    description: 'Downsize EC2 instance from m5.xlarge to m5.large',
    estimatedSavings: { amount: 120, currency: 'USD', period: 'monthly' },
    details: {
      currentType: 'm5.xlarge',
      recommendedType: 'm5.large',
      cpuUtilization: '15%',
      memoryUtilization: '30%'
    },
    createdAt: '2025-05-15T10:30:00Z'
  },
  { 
    id: '2', 
    type: 'idle_resource', 
    priority: 'medium', 
    status: 'new',
    resourceId: 'rds-1234567890abcdef0',
    resourceName: 'dev-database-1',
    resourceType: 'rds_instance',
    description: 'Stop idle RDS instance in dev environment',
    estimatedSavings: { amount: 80, currency: 'USD', period: 'monthly' },
    details: {
      lastActivity: '30 days ago',
      connectionCount: '0',
      environment: 'development'
    },
    createdAt: '2025-05-16T14:20:00Z'
  },
  { 
    id: '3', 
    type: 'purchase_reservation', 
    priority: 'medium', 
    status: 'new',
    resourceName: 'Multiple resources',
    description: 'Purchase reserved instances for stable workloads',
    estimatedSavings: { amount: 450, currency: 'USD', period: 'monthly' },
    details: {
      eligibleInstances: 12,
      recommendedTerm: '1 year',
      paymentOption: 'partial upfront'
    },
    createdAt: '2025-05-17T09:15:00Z'
  },
  { 
    id: '4', 
    type: 'delete_resource', 
    priority: 'high', 
    status: 'new',
    resourceId: 'vol-1234567890abcdef0',
    resourceName: 'unused-volume-1',
    resourceType: 'ebs_volume',
    description: 'Delete unattached EBS volume',
    estimatedSavings: { amount: 15, currency: 'USD', period: 'monthly' },
    details: {
      size: '100 GB',
      type: 'gp2',
      lastAttached: '90 days ago'
    },
    createdAt: '2025-05-18T11:45:00Z'
  },
  { 
    id: '5', 
    type: 'optimize_storage', 
    priority: 'low', 
    status: 'new',
    resourceId: 's3-bucket-logs',
    resourceName: 's3-bucket-logs',
    resourceType: 's3_bucket',
    description: 'Configure lifecycle policy for log bucket',
    estimatedSavings: { amount: 25, currency: 'USD', period: 'monthly' },
    details: {
      currentSize: '500 GB',
      oldObjects: '400 GB older than 90 days',
      recommendedAction: 'Move to Glacier after 90 days'
    },
    createdAt: '2025-05-19T16:30:00Z'
  },
  { 
    id: '6', 
    type: 'resize_resource', 
    priority: 'high', 
    status: 'in_progress',
    resourceId: 'i-0987654321fedcba0',
    resourceName: 'prod-worker-1',
    resourceType: 'ec2_instance',
    description: 'Downsize EC2 instance from c5.2xlarge to c5.xlarge',
    estimatedSavings: { amount: 140, currency: 'USD', period: 'monthly' },
    details: {
      currentType: 'c5.2xlarge',
      recommendedType: 'c5.xlarge',
      cpuUtilization: '20%',
      memoryUtilization: '35%'
    },
    createdAt: '2025-05-20T08:10:00Z'
  },
  { 
    id: '7', 
    type: 'missing_tags', 
    priority: 'low', 
    status: 'new',
    resourceId: 'i-abcdef1234567890',
    resourceName: 'test-server-1',
    resourceType: 'ec2_instance',
    description: 'Add required cost allocation tags',
    details: {
      missingTags: ['CostCenter', 'Project', 'Owner'],
      suggestedValues: {
        CostCenter: 'IT-123',
        Project: 'Unknown',
        Owner: 'Unknown'
      }
    },
    createdAt: '2025-05-21T10:05:00Z'
  },
];

const Recommendations: React.FC = () => {
  const theme = useTheme();
  const [recommendations, setRecommendations] = useState<Recommendation[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<RecommendationFilter>({
    priority: [],
    status: [],
    types: [],
  });
  const [showFilters, setShowFilters] = useState(false);

  useEffect(() => {
    // Simulate API call
    const timer = setTimeout(() => {
      setRecommendations(mockRecommendations);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleFilterChange = (field: keyof RecommendationFilter, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const applyFilters = () => {
    setLoading(true);
    
    // Simulate API call with filters
    setTimeout(() => {
      let filtered = [...mockRecommendations];
      
      if (filters.priority && filters.priority.length > 0) {
        filtered = filtered.filter(rec => filters.priority?.includes(rec.priority));
      }
      
      if (filters.status && filters.status.length > 0) {
        filtered = filtered.filter(rec => filters.status?.includes(rec.status));
      }
      
      if (filters.types && filters.types.length > 0) {
        filtered = filtered.filter(rec => filters.types?.includes(rec.type));
      }
      
      if (filters.search) {
        const search = filters.search.toLowerCase();
        filtered = filtered.filter(rec => 
          rec.description.toLowerCase().includes(search) || 
          rec.resourceName?.toLowerCase().includes(search)
        );
      }
      
      setRecommendations(filtered);
      setLoading(false);
    }, 500);
  };

  const resetFilters = () => {
    setFilters({
      priority: [],
      status: [],
      types: [],
      search: ''
    });
    
    // Reload all recommendations
    setLoading(true);
    setTimeout(() => {
      setRecommendations(mockRecommendations);
      setLoading(false);
    }, 500);
  };

  const handleCreateAction = (recommendationId: string) => {
    console.log(`Creating action for recommendation ${recommendationId}`);
    // In a real app, this would call the API to create an action
    
    // Update the recommendation status
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === recommendationId 
          ? { ...rec, status: 'in_progress' as const } 
          : rec
      )
    );
  };

  const handleDismiss = (recommendationId: string) => {
    console.log(`Dismissing recommendation ${recommendationId}`);
    // In a real app, this would call the API to dismiss the recommendation
    
    // Update the recommendation status
    setRecommendations(prev => 
      prev.map(rec => 
        rec.id === recommendationId 
          ? { ...rec, status: 'dismissed' as const } 
          : rec
      )
    );
  };

  const getPriorityIcon = (priority: string) => {
    switch (priority) {
      case 'high':
        return <ErrorIcon fontSize="small" sx={{ color: theme.palette.error.main }} />;
      case 'medium':
        return <WarningIcon fontSize="small" sx={{ color: theme.palette.warning.main }} />;
      case 'low':
        return <InfoIcon fontSize="small" sx={{ color: theme.palette.info.main }} />;
      default:
        return null;
    }
  };

  const getStatusChip = (status: string) => {
    switch (status) {
      case 'new':
        return <Chip size="small" label="New" color="info" />;
      case 'in_progress':
        return <Chip size="small" label="In Progress" color="warning" />;
      case 'applied':
        return <Chip size="small" label="Applied" color="success" />;
      case 'dismissed':
        return <Chip size="small" label="Dismissed" color="default" />;
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const totalSavings = recommendations.reduce(
    (sum, rec) => sum + (rec.estimatedSavings?.amount || 0), 
    0
  );

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Cost Optimization Recommendations
        </Typography>
        <Box>
          <Button 
            variant="outlined" 
            startIcon={<FilterIcon />} 
            onClick={() => setShowFilters(!showFilters)}
            sx={{ mr: 1 }}
          >
            Filters
          </Button>
          <Button 
            variant="outlined" 
            startIcon={<RefreshIcon />} 
            onClick={() => {
              setLoading(true);
              setTimeout(() => {
                setRecommendations(mockRecommendations);
                setLoading(false);
              }, 500);
            }}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 3 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Total Recommendations
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {recommendations.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Potential Monthly Savings
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                ${totalSavings.toLocaleString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                High Priority
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {recommendations.filter(r => r.priority === 'high').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Applied Recommendations
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {recommendations.filter(r => r.status === 'applied').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      {showFilters && (
        <Card sx={{ mb: 3 }}>
          <CardHeader title="Filters" />
          <Divider />
          <CardContent>
            <Grid container spacing={2}>
              <Grid item xs={12} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="priority-label">Priority</InputLabel>
                  <Select
                    labelId="priority-label"
                    multiple
                    value={filters.priority || []}
                    onChange={(e) => handleFilterChange('priority', e.target.value)}
                    label="Priority"
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
                    <MenuItem value="high">High</MenuItem>
                    <MenuItem value="medium">Medium</MenuItem>
                    <MenuItem value="low">Low</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="status-label">Status</InputLabel>
                  <Select
                    labelId="status-label"
                    multiple
                    value={filters.status || []}
                    onChange={(e) => handleFilterChange('status', e.target.value)}
                    label="Status"
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
                    <MenuItem value="new">New</MenuItem>
                    <MenuItem value="in_progress">In Progress</MenuItem>
                    <MenuItem value="applied">Applied</MenuItem>
                    <MenuItem value="dismissed">Dismissed</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="type-label">Type</InputLabel>
                  <Select
                    labelId="type-label"
                    multiple
                    value={filters.types || []}
                    onChange={(e) => handleFilterChange('types', e.target.value)}
                    label="Type"
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
                    <MenuItem value="resize_resource">Resize Resource</MenuItem>
                    <MenuItem value="idle_resource">Idle Resource</MenuItem>
                    <MenuItem value="delete_resource">Delete Resource</MenuItem>
                    <MenuItem value="purchase_reservation">Purchase Reservation</MenuItem>
                    <MenuItem value="optimize_storage">Optimize Storage</MenuItem>
                    <MenuItem value="missing_tags">Missing Tags</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <TextField
                  fullWidth
                  size="small"
                  label="Search"
                  value={filters.search || ''}
                  onChange={(e) => handleFilterChange('search', e.target.value)}
                />
              </Grid>
            </Grid>
            
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
              <Button onClick={resetFilters} sx={{ mr: 1 }}>
                Reset
              </Button>
              <Button variant="contained" onClick={applyFilters}>
                Apply Filters
              </Button>
            </Box>
          </CardContent>
        </Card>
      )}

      {/* Recommendations Table */}
      <Card>
        <CardHeader title="Recommendations" />
        <Divider />
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
            <CircularProgress />
          </Box>
        ) : (
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Priority</TableCell>
                  <TableCell>Description</TableCell>
                  <TableCell>Resource</TableCell>
                  <TableCell>Estimated Savings</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {recommendations.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={7} align="center">
                      No recommendations found
                    </TableCell>
                  </TableRow>
                ) : (
                  recommendations.map((recommendation) => (
                    <TableRow key={recommendation.id}>
                      <TableCell>
                        <Box sx={{ display: 'flex', alignItems: 'center' }}>
                          {getPriorityIcon(recommendation.priority)}
                          <Typography variant="body2" sx={{ ml: 1, textTransform: 'capitalize' }}>
                            {recommendation.priority}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>{recommendation.description}</TableCell>
                      <TableCell>{recommendation.resourceName}</TableCell>
                      <TableCell>
                        {recommendation.estimatedSavings ? (
                          <Typography variant="body2" color="success.main">
                            ${recommendation.estimatedSavings.amount}/{recommendation.estimatedSavings.period}
                          </Typography>
                        ) : (
                          'N/A'
                        )}
                      </TableCell>
                      <TableCell>{getStatusChip(recommendation.status)}</TableCell>
                      <TableCell>{formatDate(recommendation.createdAt)}</TableCell>
                      <TableCell align="right">
                        {recommendation.status === 'new' && (
                          <>
                            <Button 
                              size="small" 
                              variant="contained" 
                              color="primary"
                              onClick={() => handleCreateAction(recommendation.id)}
                              sx={{ mr: 1 }}
                            >
                              Apply
                            </Button>
                            <Button 
                              size="small" 
                              variant="outlined"
                              onClick={() => handleDismiss(recommendation.id)}
                            >
                              Dismiss
                            </Button>
                          </>
                        )}
                        {recommendation.status === 'in_progress' && (
                          <Button 
                            size="small" 
                            variant="outlined" 
                            color="primary"
                          >
                            View Action
                          </Button>
                        )}
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Card>
    </Box>
  );
};

export default Recommendations;

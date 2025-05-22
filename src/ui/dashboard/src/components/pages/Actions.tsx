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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  useTheme
} from '@mui/material';
import { 
  FilterList as FilterIcon,
  Refresh as RefreshIcon,
  PlayArrow as PlayArrowIcon,
  CheckCircle as CheckCircleIcon,
  Error as ErrorIcon,
  Warning as WarningIcon,
  Schedule as ScheduleIcon,
  Info as InfoIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { Action, ActionFilter } from '../../lib/types';

// Mock data - would be replaced with API calls in production
const mockActions: Action[] = [
  { 
    id: '1', 
    type: 'resize_resource', 
    status: 'pending', 
    approvalStatus: 'approved',
    resourceId: 'i-1234567890abcdef0',
    resourceName: 'prod-api-server-1',
    resourceType: 'ec2_instance',
    parameters: {
      instance_type: 'm5.large'
    },
    recommendationId: '1',
    createdBy: 'user1',
    createdAt: '2025-05-20T10:30:00Z'
  },
  { 
    id: '2', 
    type: 'stop_resource', 
    status: 'pending', 
    approvalStatus: 'pending',
    resourceId: 'rds-1234567890abcdef0',
    resourceName: 'dev-database-1',
    resourceType: 'rds_instance',
    parameters: {
      force: true
    },
    recommendationId: '2',
    createdBy: 'user2',
    createdAt: '2025-05-20T14:20:00Z'
  },
  { 
    id: '3', 
    type: 'purchase_reservation', 
    status: 'pending', 
    approvalStatus: 'pending',
    parameters: {
      instance_count: 12,
      instance_type: 'm5.xlarge',
      term: '1 year',
      payment_option: 'partial_upfront'
    },
    createdBy: 'user1',
    createdAt: '2025-05-20T09:15:00Z'
  },
  { 
    id: '4', 
    type: 'delete_resource', 
    status: 'completed', 
    approvalStatus: 'approved',
    resourceId: 'vol-1234567890abcdef0',
    resourceName: 'unused-volume-1',
    resourceType: 'ebs_volume',
    parameters: {},
    recommendationId: '4',
    createdBy: 'user3',
    createdAt: '2025-05-19T11:45:00Z',
    completedAt: '2025-05-19T12:00:00Z',
    result: {
      success: true,
      message: 'Volume deleted successfully'
    }
  },
  { 
    id: '5', 
    type: 'optimize_storage', 
    status: 'failed', 
    approvalStatus: 'approved',
    resourceId: 's3-bucket-logs',
    resourceName: 's3-bucket-logs',
    resourceType: 's3_bucket',
    parameters: {
      lifecycle_configuration: {
        rules: [
          {
            id: 'move-to-glacier',
            status: 'Enabled',
            filter: {
              prefix: 'logs/'
            },
            transitions: [
              {
                days: 90,
                storageClass: 'GLACIER'
              }
            ]
          }
        ]
      }
    },
    recommendationId: '5',
    createdBy: 'user2',
    createdAt: '2025-05-18T16:30:00Z',
    completedAt: '2025-05-18T16:35:00Z',
    result: {
      success: false,
      message: 'Failed to apply lifecycle configuration: Access denied'
    }
  },
  { 
    id: '6', 
    type: 'resize_resource', 
    status: 'in_progress', 
    approvalStatus: 'approved',
    resourceId: 'i-0987654321fedcba0',
    resourceName: 'prod-worker-1',
    resourceType: 'ec2_instance',
    parameters: {
      instance_type: 'c5.xlarge'
    },
    recommendationId: '6',
    createdBy: 'user1',
    createdAt: '2025-05-21T08:10:00Z'
  },
  { 
    id: '7', 
    type: 'add_tags', 
    status: 'pending', 
    approvalStatus: 'rejected',
    resourceId: 'i-abcdef1234567890',
    resourceName: 'test-server-1',
    resourceType: 'ec2_instance',
    parameters: {
      tags: {
        CostCenter: 'IT-123',
        Project: 'Testing',
        Owner: 'DevOps'
      }
    },
    recommendationId: '7',
    createdBy: 'user3',
    createdAt: '2025-05-21T10:05:00Z'
  },
];

const Actions: React.FC = () => {
  const theme = useTheme();
  const [actions, setActions] = useState<Action[]>([]);
  const [loading, setLoading] = useState(true);
  const [filters, setFilters] = useState<ActionFilter>({
    status: [],
    approvalStatus: [],
    types: [],
  });
  const [showFilters, setShowFilters] = useState(false);
  const [selectedAction, setSelectedAction] = useState<Action | null>(null);
  const [detailsOpen, setDetailsOpen] = useState(false);
  const [scheduleOpen, setScheduleOpen] = useState(false);
  const [scheduleDate, setScheduleDate] = useState<string>('');
  const [scheduleTime, setScheduleTime] = useState<string>('');

  useEffect(() => {
    // Simulate API call
    const timer = setTimeout(() => {
      setActions(mockActions);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleFilterChange = (field: keyof ActionFilter, value: any) => {
    setFilters(prev => ({
      ...prev,
      [field]: value
    }));
  };

  const applyFilters = () => {
    setLoading(true);
    
    // Simulate API call with filters
    setTimeout(() => {
      let filtered = [...mockActions];
      
      if (filters.status && filters.status.length > 0) {
        filtered = filtered.filter(action => filters.status?.includes(action.status));
      }
      
      if (filters.approvalStatus && filters.approvalStatus.length > 0) {
        filtered = filtered.filter(action => filters.approvalStatus?.includes(action.approvalStatus));
      }
      
      if (filters.types && filters.types.length > 0) {
        filtered = filtered.filter(action => filters.types?.includes(action.type));
      }
      
      if (filters.search) {
        const search = filters.search.toLowerCase();
        filtered = filtered.filter(action => 
          action.type.toLowerCase().includes(search) || 
          action.resourceName?.toLowerCase().includes(search)
        );
      }
      
      setActions(filtered);
      setLoading(false);
    }, 500);
  };

  const resetFilters = () => {
    setFilters({
      status: [],
      approvalStatus: [],
      types: [],
      search: ''
    });
    
    // Reload all actions
    setLoading(true);
    setTimeout(() => {
      setActions(mockActions);
      setLoading(false);
    }, 500);
  };

  const handleApprove = (actionId: string) => {
    console.log(`Approving action ${actionId}`);
    // In a real app, this would call the API to approve the action
    
    // Update the action approval status
    setActions(prev => 
      prev.map(action => 
        action.id === actionId 
          ? { ...action, approvalStatus: 'approved' as const } 
          : action
      )
    );
  };

  const handleReject = (actionId: string) => {
    console.log(`Rejecting action ${actionId}`);
    // In a real app, this would call the API to reject the action
    
    // Update the action approval status
    setActions(prev => 
      prev.map(action => 
        action.id === actionId 
          ? { ...action, approvalStatus: 'rejected' as const } 
          : action
      )
    );
  };

  const handleExecute = (actionId: string) => {
    console.log(`Executing action ${actionId}`);
    // In a real app, this would call the API to execute the action
    
    // Update the action status
    setActions(prev => 
      prev.map(action => 
        action.id === actionId 
          ? { ...action, status: 'in_progress' as const } 
          : action
      )
    );
  };

  const handleSchedule = (action: Action) => {
    setSelectedAction(action);
    setScheduleOpen(true);
  };

  const handleScheduleSubmit = () => {
    if (!selectedAction || !scheduleDate || !scheduleTime) return;
    
    const scheduledTime = `${scheduleDate}T${scheduleTime}:00Z`;
    console.log(`Scheduling action ${selectedAction.id} for ${scheduledTime}`);
    
    // In a real app, this would call the API to schedule the action
    
    // Update the action with scheduled time
    setActions(prev => 
      prev.map(action => 
        action.id === selectedAction.id 
          ? { ...action, scheduledTime } 
          : action
      )
    );
    
    setScheduleOpen(false);
    setSelectedAction(null);
    setScheduleDate('');
    setScheduleTime('');
  };

  const handleViewDetails = (action: Action) => {
    setSelectedAction(action);
    setDetailsOpen(true);
  };

  const getStatusChip = (status: string) => {
    switch (status) {
      case 'pending':
        return <Chip size="small" label="Pending" color="info" />;
      case 'in_progress':
        return <Chip size="small" label="In Progress" color="warning" />;
      case 'completed':
        return <Chip size="small" label="Completed" color="success" />;
      case 'failed':
        return <Chip size="small" label="Failed" color="error" />;
      default:
        return null;
    }
  };

  const getApprovalStatusChip = (status: string) => {
    switch (status) {
      case 'pending':
        return <Chip size="small" label="Pending Approval" color="info" />;
      case 'approved':
        return <Chip size="small" label="Approved" color="success" />;
      case 'rejected':
        return <Chip size="small" label="Rejected" color="error" />;
      default:
        return null;
    }
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const formatActionType = (type: string) => {
    return type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ');
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Actions
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
                setActions(mockActions);
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
                Total Actions
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {actions.length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Pending Approval
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {actions.filter(a => a.approvalStatus === 'pending').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                In Progress
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {actions.filter(a => a.status === 'in_progress').length}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Completed
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {actions.filter(a => a.status === 'completed').length}
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
                    <MenuItem value="pending">Pending</MenuItem>
                    <MenuItem value="in_progress">In Progress</MenuItem>
                    <MenuItem value="completed">Completed</MenuItem>
                    <MenuItem value="failed">Failed</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
              
              <Grid item xs={12} md={3}>
                <FormControl fullWidth size="small">
                  <InputLabel id="approval-status-label">Approval Status</InputLabel>
                  <Select
                    labelId="approval-status-label"
                    multiple
                    value={filters.approvalStatus || []}
                    onChange={(e) => handleFilterChange('approvalStatus', e.target.value)}
                    label="Approval Status"
                    renderValue={(selected) => (
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                        {(selected as string[]).map((value) => (
                          <Chip key={value} label={value} size="small" />
                        ))}
                      </Box>
                    )}
                  >
                    <MenuItem value="pending">Pending</MenuItem>
                    <MenuItem value="approved">Approved</MenuItem>
                    <MenuItem value="rejected">Rejected</MenuItem>
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
                    <MenuItem value="stop_resource">Stop Resource</MenuItem>
                    <MenuItem value="delete_resource">Delete Resource</MenuItem>
                    <MenuItem value="purchase_reservation">Purchase Reservation</MenuItem>
                    <MenuItem value="optimize_storage">Optimize Storage</MenuItem>
                    <MenuItem value="add_tags">Add Tags</MenuItem>
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

      {/* Actions Table */}
      <Card>
        <CardHeader title="Actions" />
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
                  <TableCell>Type</TableCell>
                  <TableCell>Resource</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Approval</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell align="right">Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {actions.length === 0 ? (
                  <TableRow>
                    <TableCell colSpan={6} align="center">
                      No actions found
                    </TableCell>
                  </TableRow>
                ) : (
                  actions.map((action) => (
                    <TableRow key={action.id}>
                      <TableCell>{formatActionType(action.type)}</TableCell>
                      <TableCell>{action.resourceName || 'N/A'}</TableCell>
                      <TableCell>{getStatusChip(action.status)}</TableCell>
                      <TableCell>{getApprovalStatusChip(action.approvalStatus)}</TableCell>
                      <TableCell>{formatDate(action.createdAt)}</TableCell>
                      <TableCell align="right">
                        <Box sx={{ display: 'flex', justifyContent: 'flex-end' }}>
                          <Tooltip title="View Details">
                            <IconButton 
                              size="small" 
                              onClick={() => handleViewDetails(action)}
                              sx={{ mr: 1 }}
                            >
                              <InfoIcon fontSize="small" />
                            </IconButton>
                          </Tooltip>
                          
                          {action.approvalStatus === 'pending' && (
                            <>
                              <Button 
                                size="small" 
                                variant="contained" 
                                color="success"
                                onClick={() => handleApprove(action.id)}
                                sx={{ mr: 1 }}
                              >
                                Approve
                              </Button>
                              <Button 
                                size="small" 
                                variant="outlined"
                                color="error"
                                onClick={() => handleReject(action.id)}
                                sx={{ mr: 1 }}
                              >
                                Reject
                              </Button>
                            </>
                          )}
                          
                          {action.approvalStatus === 'approved' && action.status === 'pending' && (
                            <>
                              <Tooltip title="Execute Now">
                                <IconButton 
                                  color="primary" 
                                  size="small"
                                  onClick={() => handleExecute(action.id)}
                                  sx={{ mr: 1 }}
                                >
                                  <PlayArrowIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                              <Tooltip title="Schedule">
                                <IconButton 
                                  color="primary" 
                                  size="small"
                                  onClick={() => handleSchedule(action)}
                                >
                                  <ScheduleIcon fontSize="small" />
                                </IconButton>
                              </Tooltip>
                            </>
                          )}
                        </Box>
                      </TableCell>
                    </TableRow>
                  ))
                )}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </Card>

      {/* Action Details Dialog */}
      <Dialog
        open={detailsOpen}
        onClose={() => setDetailsOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Action Details
          <IconButton
            aria-label="close"
            onClick={() => setDetailsOpen(false)}
            sx={{
              position: 'absolute',
              right: 8,
              top: 8,
            }}
          >
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {selectedAction && (
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Action Type
                </Typography>
                <Typography variant="body1">
                  {formatActionType(selectedAction.type)}
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Status
                </Typography>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  {getStatusChip(selectedAction.status)}
                  <Typography variant="body2" sx={{ ml: 1 }}>
                    {getApprovalStatusChip(selectedAction.approvalStatus)}
                  </Typography>
                </Box>
              </Grid>
              
              {selectedAction.resourceName && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Resource Name
                  </Typography>
                  <Typography variant="body1">
                    {selectedAction.resourceName}
                  </Typography>
                </Grid>
              )}
              
              {selectedAction.resourceType && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Resource Type
                  </Typography>
                  <Typography variant="body1">
                    {selectedAction.resourceType}
                  </Typography>
                </Grid>
              )}
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Created By
                </Typography>
                <Typography variant="body1">
                  {selectedAction.createdBy}
                </Typography>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" color="textSecondary">
                  Created At
                </Typography>
                <Typography variant="body1">
                  {formatDate(selectedAction.createdAt)}
                </Typography>
              </Grid>
              
              {selectedAction.completedAt && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Completed At
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(selectedAction.completedAt)}
                  </Typography>
                </Grid>
              )}
              
              {selectedAction.scheduledTime && (
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Scheduled For
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(selectedAction.scheduledTime)}
                  </Typography>
                </Grid>
              )}
              
              <Grid item xs={12}>
                <Typography variant="subtitle2" color="textSecondary">
                  Parameters
                </Typography>
                <Paper variant="outlined" sx={{ p: 2, mt: 1, backgroundColor: theme.palette.background.default }}>
                  <pre style={{ margin: 0, overflow: 'auto' }}>
                    {JSON.stringify(selectedAction.parameters, null, 2)}
                  </pre>
                </Paper>
              </Grid>
              
              {selectedAction.result && (
                <Grid item xs={12}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Result
                  </Typography>
                  <Paper variant="outlined" sx={{ 
                    p: 2, 
                    mt: 1, 
                    backgroundColor: theme.palette.background.default,
                    borderColor: selectedAction.result.success ? theme.palette.success.main : theme.palette.error.main
                  }}>
                    <Typography variant="body2" color={selectedAction.result.success ? 'success.main' : 'error.main'}>
                      {selectedAction.result.message}
                    </Typography>
                    {selectedAction.result.details && (
                      <pre style={{ margin: '10px 0 0 0', overflow: 'auto' }}>
                        {JSON.stringify(selectedAction.result.details, null, 2)}
                      </pre>
                    )}
                  </Paper>
                </Grid>
              )}
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDetailsOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>

      {/* Schedule Dialog */}
      <Dialog
        open={scheduleOpen}
        onClose={() => setScheduleOpen(false)}
      >
        <DialogTitle>Schedule Action</DialogTitle>
        <DialogContent>
          <Typography variant="body2" sx={{ mb: 2 }}>
            Select when to execute this action:
          </Typography>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Date"
                type="date"
                fullWidth
                value={scheduleDate}
                onChange={(e) => setScheduleDate(e.target.value)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                label="Time"
                type="time"
                fullWidth
                value={scheduleTime}
                onChange={(e) => setScheduleTime(e.target.value)}
                InputLabelProps={{
                  shrink: true,
                }}
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setScheduleOpen(false)}>Cancel</Button>
          <Button 
            onClick={handleScheduleSubmit} 
            variant="contained" 
            disabled={!scheduleDate || !scheduleTime}
          >
            Schedule
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Actions;

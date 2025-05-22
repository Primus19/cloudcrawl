import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, CardHeader, Button, Stepper, Step, StepLabel } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

// Sample data - would be replaced with actual API data in production
const workflows = [
  { id: 1, name: 'Daily EC2 Optimization', status: 'Active', lastRun: '2023-05-21', nextRun: '2023-05-22', savings: '$120/month' },
  { id: 2, name: 'Weekly S3 Cleanup', status: 'Active', lastRun: '2023-05-18', nextRun: '2023-05-25', savings: '$45/month' },
  { id: 3, name: 'Monthly RDS Rightsizing', status: 'Inactive', lastRun: '2023-04-30', nextRun: 'N/A', savings: '$0/month' },
  { id: 4, name: 'Idle Resource Detection', status: 'Active', lastRun: '2023-05-20', nextRun: '2023-05-23', savings: '$85/month' },
  { id: 5, name: 'Reserved Instance Planner', status: 'Active', lastRun: '2023-05-01', nextRun: '2023-06-01', savings: '$350/month' },
];

const columns: GridColDef[] = [
  { field: 'name', headerName: 'Workflow Name', width: 200 },
  { field: 'status', headerName: 'Status', width: 120 },
  { field: 'lastRun', headerName: 'Last Run', width: 150 },
  { field: 'nextRun', headerName: 'Next Run', width: 150 },
  { field: 'savings', headerName: 'Estimated Savings', width: 150 },
  {
    field: 'actions',
    headerName: 'Actions',
    width: 200,
    renderCell: () => (
      <Box>
        <Button size="small" variant="outlined" sx={{ mr: 1 }}>Edit</Button>
        <Button size="small" variant="contained">Run Now</Button>
      </Box>
    ),
  },
];

const Workflows: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Automation Workflows
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
            <Button variant="contained" color="primary">
              Create New Workflow
            </Button>
          </Box>
          
          <Paper sx={{ p: 2, mb: 3 }}>
            <DataGrid
              rows={workflows}
              columns={columns}
              pageSize={5}
              rowsPerPageOptions={[5, 10, 25]}
              autoHeight
              disableSelectionOnClick
            />
          </Paper>
        </Grid>
        
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Create Workflow
            </Typography>
            
            <Stepper activeStep={0} sx={{ mb: 4 }}>
              <Step>
                <StepLabel>Select Resources</StepLabel>
              </Step>
              <Step>
                <StepLabel>Define Actions</StepLabel>
              </Step>
              <Step>
                <StepLabel>Set Schedule</StepLabel>
              </Step>
              <Step>
                <StepLabel>Review & Save</StepLabel>
              </Step>
            </Stepper>
            
            <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
              <Button variant="contained" disabled sx={{ mr: 1 }}>
                Back
              </Button>
              <Button variant="contained" color="primary">
                Next
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Workflows;

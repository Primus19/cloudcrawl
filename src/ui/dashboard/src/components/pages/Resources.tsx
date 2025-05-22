import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, CardHeader } from '@mui/material';
import { DataGrid, GridColDef } from '@mui/x-data-grid';

// Sample data - would be replaced with actual API data in production
const resources = [
  { id: 1, name: 'web-server-01', type: 'EC2 Instance', region: 'us-east-1', status: 'Running', cost: '$45.60/month' },
  { id: 2, name: 'app-server-01', type: 'EC2 Instance', region: 'us-east-1', status: 'Running', cost: '$65.30/month' },
  { id: 3, name: 'db-server-01', type: 'RDS Instance', region: 'us-east-1', status: 'Running', cost: '$120.80/month' },
  { id: 4, name: 'storage-bucket-01', type: 'S3 Bucket', region: 'us-east-1', status: 'Active', cost: '$22.40/month' },
  { id: 5, name: 'lambda-function-01', type: 'Lambda Function', region: 'us-east-1', status: 'Active', cost: '$5.20/month' },
  { id: 6, name: 'web-server-02', type: 'EC2 Instance', region: 'us-west-2', status: 'Stopped', cost: '$0.00/month' },
  { id: 7, name: 'app-server-02', type: 'EC2 Instance', region: 'us-west-2', status: 'Running', cost: '$65.30/month' },
  { id: 8, name: 'db-server-02', type: 'RDS Instance', region: 'us-west-2', status: 'Running', cost: '$120.80/month' },
];

const columns: GridColDef[] = [
  { field: 'name', headerName: 'Name', width: 180 },
  { field: 'type', headerName: 'Type', width: 150 },
  { field: 'region', headerName: 'Region', width: 120 },
  { field: 'status', headerName: 'Status', width: 120 },
  { field: 'cost', headerName: 'Monthly Cost', width: 150 },
];

const Resources: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Cloud Resources
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2, height: 'calc(100vh - 200px)' }}>
            <DataGrid
              rows={resources}
              columns={columns}
              pageSize={10}
              rowsPerPageOptions={[10, 25, 50]}
              checkboxSelection
              disableSelectionOnClick
            />
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Resources;

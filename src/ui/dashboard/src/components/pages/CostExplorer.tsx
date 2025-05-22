import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, CardHeader } from '@mui/material';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, LineChart, Line } from 'recharts';

// Sample data - would be replaced with actual API data in production
const costData = [
  { name: 'Jan', AWS: 4000, Azure: 2400, GCP: 1800 },
  { name: 'Feb', AWS: 3000, Azure: 1398, GCP: 2000 },
  { name: 'Mar', AWS: 2000, Azure: 9800, GCP: 2290 },
  { name: 'Apr', AWS: 2780, Azure: 3908, GCP: 2500 },
  { name: 'May', AWS: 1890, Azure: 4800, GCP: 2181 },
  { name: 'Jun', AWS: 2390, Azure: 3800, GCP: 2500 },
];

const serviceData = [
  { name: 'EC2', value: 35 },
  { name: 'S3', value: 20 },
  { name: 'RDS', value: 15 },
  { name: 'Lambda', value: 10 },
  { name: 'Other', value: 20 },
];

const CostExplorer: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Cost Explorer
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Monthly Cloud Costs
            </Typography>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart
                data={costData}
                margin={{
                  top: 5,
                  right: 30,
                  left: 20,
                  bottom: 5,
                }}
              >
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="AWS" fill="#8884d8" />
                <Bar dataKey="Azure" fill="#82ca9d" />
                <Bar dataKey="GCP" fill="#ffc658" />
              </BarChart>
            </ResponsiveContainer>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Cost Breakdown by Service" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart
                  layout="vertical"
                  data={serviceData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis type="number" />
                  <YAxis dataKey="name" type="category" />
                  <Tooltip />
                  <Legend />
                  <Bar dataKey="value" fill="#8884d8" />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader title="Cost Trend" />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart
                  data={costData}
                  margin={{
                    top: 5,
                    right: 30,
                    left: 20,
                    bottom: 5,
                  }}
                >
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="name" />
                  <YAxis />
                  <Tooltip />
                  <Legend />
                  <Line type="monotone" dataKey="AWS" stroke="#8884d8" activeDot={{ r: 8 }} />
                  <Line type="monotone" dataKey="Azure" stroke="#82ca9d" />
                  <Line type="monotone" dataKey="GCP" stroke="#ffc658" />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default CostExplorer;

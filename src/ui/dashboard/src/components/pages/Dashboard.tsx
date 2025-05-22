import React, { useState, useEffect } from 'react';
import { 
  Grid, 
  Paper, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  CardHeader, 
  Button, 
  Chip, 
  Divider,
  CircularProgress,
  useTheme
} from '@mui/material';
import { 
  TrendingUp as TrendingUpIcon, 
  TrendingDown as TrendingDownIcon,
  Warning as WarningIcon,
  CheckCircle as CheckCircleIcon
} from '@mui/icons-material';
import { ResponsiveContainer, LineChart, Line, BarChart, Bar, XAxis, YAxis, Tooltip, Legend, PieChart, Pie, Cell } from 'recharts';

// Mock data - would be replaced with API calls in production
const costTrendData = [
  { date: '2025-05-01', amount: 1200 },
  { date: '2025-05-02', amount: 1300 },
  { date: '2025-05-03', amount: 1400 },
  { date: '2025-05-04', amount: 1350 },
  { date: '2025-05-05', amount: 1500 },
  { date: '2025-05-06', amount: 1450 },
  { date: '2025-05-07', amount: 1400 },
  { date: '2025-05-08', amount: 1350 },
  { date: '2025-05-09', amount: 1300 },
  { date: '2025-05-10', amount: 1250 },
  { date: '2025-05-11', amount: 1200 },
  { date: '2025-05-12', amount: 1150 },
  { date: '2025-05-13', amount: 1100 },
  { date: '2025-05-14', amount: 1050 },
  { date: '2025-05-15', amount: 1000 },
  { date: '2025-05-16', amount: 950 },
  { date: '2025-05-17', amount: 900 },
  { date: '2025-05-18', amount: 850 },
  { date: '2025-05-19', amount: 800 },
  { date: '2025-05-20', amount: 750 },
  { date: '2025-05-21', amount: 700 },
];

const costBreakdownData = [
  { name: 'Compute', value: 45 },
  { name: 'Storage', value: 25 },
  { name: 'Network', value: 15 },
  { name: 'Database', value: 10 },
  { name: 'Other', value: 5 },
];

const recommendationsData = [
  { 
    id: '1', 
    type: 'resize_resource', 
    priority: 'high', 
    resourceName: 'prod-api-server', 
    description: 'Downsize EC2 instance from m5.xlarge to m5.large',
    estimatedSavings: { amount: 120, currency: 'USD', period: 'monthly' }
  },
  { 
    id: '2', 
    type: 'idle_resource', 
    priority: 'medium', 
    resourceName: 'dev-database', 
    description: 'Stop idle RDS instance in dev environment',
    estimatedSavings: { amount: 80, currency: 'USD', period: 'monthly' }
  },
  { 
    id: '3', 
    type: 'purchase_reservation', 
    priority: 'medium', 
    resourceName: 'Multiple resources', 
    description: 'Purchase reserved instances for stable workloads',
    estimatedSavings: { amount: 450, currency: 'USD', period: 'monthly' }
  },
];

const resourcesData = [
  { type: 'EC2 Instances', count: 42, cost: 3200 },
  { type: 'RDS Instances', count: 12, cost: 1800 },
  { type: 'S3 Buckets', count: 25, cost: 950 },
  { type: 'EBS Volumes', count: 65, cost: 750 },
];

const Dashboard: React.FC = () => {
  const theme = useTheme();
  const [loading, setLoading] = useState(true);
  const [totalCost, setTotalCost] = useState(0);
  const [costTrend, setCostTrend] = useState(0);
  const [savingsOpportunity, setSavingsOpportunity] = useState(0);
  const [actionsPending, setActionsPending] = useState(0);

  useEffect(() => {
    // Simulate API loading
    const timer = setTimeout(() => {
      setLoading(false);
      setTotalCost(6700);
      setCostTrend(-12);
      setSavingsOpportunity(650);
      setActionsPending(5);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const COLORS = [
    theme.palette.primary.main,
    theme.palette.secondary.main,
    theme.palette.info.main,
    theme.palette.warning.main,
    theme.palette.error.main,
  ];

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '80vh' }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Typography variant="h4" gutterBottom>
        Cloud Cost Dashboard
      </Typography>
      
      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Monthly Cost
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                ${totalCost.toLocaleString()}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                {costTrend < 0 ? (
                  <>
                    <TrendingDownIcon sx={{ color: theme.palette.success.main, mr: 0.5 }} />
                    <Typography variant="body2" color="success.main">
                      {Math.abs(costTrend)}% decrease
                    </Typography>
                  </>
                ) : (
                  <>
                    <TrendingUpIcon sx={{ color: theme.palette.error.main, mr: 0.5 }} />
                    <Typography variant="body2" color="error.main">
                      {costTrend}% increase
                    </Typography>
                  </>
                )}
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Savings Opportunity
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                ${savingsOpportunity.toLocaleString()}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <Typography variant="body2" color="textSecondary">
                  {Math.round((savingsOpportunity / totalCost) * 100)}% of monthly cost
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Recommendations
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {recommendationsData.length}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <WarningIcon sx={{ color: theme.palette.warning.main, mr: 0.5 }} />
                <Typography variant="body2" color="warning.main">
                  {recommendationsData.filter(r => r.priority === 'high').length} high priority
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Typography variant="subtitle2" color="textSecondary">
                Actions Pending
              </Typography>
              <Typography variant="h4" component="div" sx={{ mt: 1 }}>
                {actionsPending}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <Button size="small" variant="outlined" color="primary">
                  Review
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Charts Row */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={8}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Cost Trend" />
            <Divider />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={costTrendData}>
                  <XAxis 
                    dataKey="date" 
                    tickFormatter={(value) => {
                      const date = new Date(value);
                      return `${date.getMonth() + 1}/${date.getDate()}`;
                    }}
                  />
                  <YAxis />
                  <Tooltip 
                    formatter={(value) => [`$${value}`, 'Cost']}
                    labelFormatter={(label) => {
                      const date = new Date(label);
                      return date.toLocaleDateString();
                    }}
                  />
                  <Legend />
                  <Line 
                    type="monotone" 
                    dataKey="amount" 
                    stroke={theme.palette.primary.main} 
                    name="Daily Cost" 
                    strokeWidth={2}
                    dot={{ r: 1 }}
                    activeDot={{ r: 5 }}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={4}>
          <Card sx={{ height: '100%' }}>
            <CardHeader title="Cost Breakdown" />
            <Divider />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={costBreakdownData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    outerRadius={80}
                    fill="#8884d8"
                    dataKey="value"
                    label={({ name, percent }) => `${name}: ${(percent * 100).toFixed(0)}%`}
                  >
                    {costBreakdownData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip formatter={(value) => [`${value}%`, 'Percentage']} />
                  <Legend />
                </PieChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
      
      {/* Recommendations and Resources */}
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Top Recommendations" 
              action={
                <Button size="small" color="primary">
                  View All
                </Button>
              }
            />
            <Divider />
            <CardContent sx={{ p: 0 }}>
              {recommendationsData.map((recommendation, index) => (
                <Box key={recommendation.id} sx={{ p: 2, borderBottom: index < recommendationsData.length - 1 ? 1 : 0, borderColor: 'divider' }}>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                    <Typography variant="subtitle1">
                      {recommendation.description}
                    </Typography>
                    <Chip 
                      label={recommendation.priority} 
                      size="small" 
                      color={
                        recommendation.priority === 'high' ? 'error' : 
                        recommendation.priority === 'medium' ? 'warning' : 'success'
                      }
                    />
                  </Box>
                  <Typography variant="body2" color="textSecondary" gutterBottom>
                    Resource: {recommendation.resourceName}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mt: 1 }}>
                    <Typography variant="body2" color="success.main">
                      Estimated savings: ${recommendation.estimatedSavings.amount}/month
                    </Typography>
                    <Button size="small" variant="contained" color="primary">
                      Apply
                    </Button>
                  </Box>
                </Box>
              ))}
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardHeader 
              title="Resource Overview" 
              action={
                <Button size="small" color="primary">
                  View All
                </Button>
              }
            />
            <Divider />
            <CardContent>
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={resourcesData}>
                  <XAxis dataKey="type" />
                  <YAxis yAxisId="left" orientation="left" stroke={theme.palette.primary.main} />
                  <YAxis yAxisId="right" orientation="right" stroke={theme.palette.secondary.main} />
                  <Tooltip formatter={(value, name) => [name === 'cost' ? `$${value}` : value, name === 'cost' ? 'Cost' : 'Count']} />
                  <Legend />
                  <Bar yAxisId="left" dataKey="count" name="Count" fill={theme.palette.primary.main} />
                  <Bar yAxisId="right" dataKey="cost" name="Cost ($)" fill={theme.palette.secondary.main} />
                </BarChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Dashboard;

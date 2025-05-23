import React, { useState } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { AppBar, Toolbar, Typography, Container, Box, Tabs, Tab } from "@mui/material";

// Dashboard component
const Dashboard = () => (
  <Box sx={{ p: 3 }}>
    <Typography variant="h4" gutterBottom>Dashboard</Typography>
    <Typography>Welcome to the Cloud Cost Optimizer dashboard.</Typography>
  </Box>
);

// AWS Accounts component
const AWSAccounts = () => (
  <Box sx={{ p: 3 }}>
    <Typography variant="h4" gutterBottom>AWS Accounts</Typography>
    <Typography>Manage your AWS accounts here.</Typography>
  </Box>
);

// AWS Resources component
const AWSResources = () => (
  <Box sx={{ p: 3 }}>
    <Typography variant="h4" gutterBottom>AWS Resources</Typography>
    <Typography>View and manage your AWS resources here.</Typography>
  </Box>
);

// Terraform Templates component
const TerraformTemplates = () => (
  <Box sx={{ p: 3 }}>
    <Typography variant="h4" gutterBottom>Terraform Templates</Typography>
    <Typography>Manage your Terraform templates here.</Typography>
  </Box>
);

// Main App component
function App() {
  const [tabValue, setTabValue] = useState(0);

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Typography variant="h6">Cloud Cost Optimizer</Typography>
        </Toolbar>
      </AppBar>
      <Tabs value={tabValue} onChange={handleTabChange} centered>
        <Tab label="Dashboard" />
        <Tab label="AWS Accounts" />
        <Tab label="AWS Resources" />
        <Tab label="Terraform Templates" />
      </Tabs>
      <Container>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/aws/accounts" element={<AWSAccounts />} />
          <Route path="/aws/resources" element={<AWSResources />} />
          <Route path="/terraform/templates" element={<TerraformTemplates />} />
        </Routes>
      </Container>
    </Router>
  );
}

export default App;

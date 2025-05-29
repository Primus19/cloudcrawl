import React from 'react';
import { Box, Container, Typography } from '@mui/material';
import CloudAccountsList from '../CloudAccounts/CloudAccountsList';

const CloudAccounts: React.FC = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Cloud Accounts
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Manage your cloud provider accounts and view their associated resources and costs.
        </Typography>
        
        <CloudAccountsList />
      </Box>
    </Container>
  );
};

export default CloudAccounts;

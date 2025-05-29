import React from 'react';
import { Box, Container, Typography, Grid, Card, CardContent, Button } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';

const Terraform: React.FC = () => {
  // Mock terraform templates data
  const templates = [
    {
      id: 'aws-vpc',
      name: 'AWS VPC with Subnets',
      description: 'Creates a VPC with public and private subnets across multiple availability zones',
      provider: 'aws',
      category: 'networking'
    },
    {
      id: 'aws-eks',
      name: 'AWS EKS Cluster',
      description: 'Deploys a production-ready Kubernetes cluster with worker nodes and networking',
      provider: 'aws',
      category: 'containers'
    },
    {
      id: 'aws-rds',
      name: 'AWS RDS Database',
      description: 'Sets up a highly available RDS database with backups and monitoring',
      provider: 'aws',
      category: 'database'
    },
    {
      id: 'gcp-gke',
      name: 'GCP GKE Cluster',
      description: 'Creates a Google Kubernetes Engine cluster with auto-scaling node pools',
      provider: 'gcp',
      category: 'containers'
    },
    {
      id: 'azure-aks',
      name: 'Azure Kubernetes Service',
      description: 'Deploys an AKS cluster with virtual network integration',
      provider: 'azure',
      category: 'containers'
    },
    {
      id: 'multi-cloud-network',
      name: 'Multi-Cloud Network',
      description: 'Establishes secure network connectivity between AWS, GCP, and Azure',
      provider: 'multi',
      category: 'networking'
    }
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mt: 4, mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Terraform Templates
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />}>
            Create Custom Template
          </Button>
        </Box>
        
        <Typography variant="body1" color="text.secondary" paragraph>
          Deploy infrastructure as code using pre-configured templates or create your own custom templates.
        </Typography>
        
        <Grid container spacing={3}>
          {templates.map((template) => (
            <Grid item xs={12} md={6} lg={4} key={template.id}>
              <Card 
                sx={{ 
                  height: '100%', 
                  display: 'flex', 
                  flexDirection: 'column',
                  transition: 'transform 0.2s, box-shadow 0.2s',
                  '&:hover': {
                    transform: 'translateY(-4px)',
                    boxShadow: '0 8px 16px rgba(0,0,0,0.2)'
                  }
                }}
              >
                <CardContent sx={{ flexGrow: 1 }}>
                  <Typography variant="h6" component="h2" gutterBottom>
                    {template.name}
                  </Typography>
                  <Box 
                    sx={{ 
                      display: 'flex', 
                      gap: 1, 
                      mb: 2 
                    }}
                  >
                    <Typography 
                      variant="caption" 
                      sx={{ 
                        bgcolor: 'primary.main', 
                        color: 'primary.contrastText',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1
                      }}
                    >
                      {template.provider.toUpperCase()}
                    </Typography>
                    <Typography 
                      variant="caption" 
                      sx={{ 
                        bgcolor: 'secondary.main', 
                        color: 'secondary.contrastText',
                        px: 1,
                        py: 0.5,
                        borderRadius: 1
                      }}
                    >
                      {template.category}
                    </Typography>
                  </Box>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    {template.description}
                  </Typography>
                  <Box sx={{ display: 'flex', justifyContent: 'flex-end', mt: 2 }}>
                    <Button size="small" variant="outlined" sx={{ mr: 1 }}>
                      View
                    </Button>
                    <Button size="small" variant="contained">
                      Deploy
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Box>
    </Container>
  );
};

export default Terraform;

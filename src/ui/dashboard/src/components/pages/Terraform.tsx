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
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Tooltip,
  CircularProgress,
  useTheme
} from '@mui/material';
import { 
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as PlayArrowIcon,
  Code as CodeIcon,
  ContentCopy as ContentCopyIcon,
  Close as CloseIcon
} from '@mui/icons-material';
import { TerraformTemplate, TerraformDeployment } from '../../lib/types';

// Mock data - would be replaced with API calls in production
const mockTemplates: TerraformTemplate[] = [
  {
    id: '1',
    name: 'AWS EC2 Instance',
    description: 'Creates an EC2 instance with specified configuration',
    variables: {
      instance_type: {
        description: 'The instance type to use',
        type: 'string',
        default: 't3.micro',
        required: true
      },
      ami_id: {
        description: 'The AMI ID to use',
        type: 'string',
        default: 'ami-0c55b159cbfafe1f0',
        required: true
      },
      subnet_id: {
        description: 'The subnet ID to launch the instance in',
        type: 'string',
        required: true
      },
      tags: {
        description: 'Tags to apply to the instance',
        type: 'map',
        default: {
          Name: 'example-instance',
          Environment: 'dev'
        },
        required: false
      }
    },
    content: `provider "aws" {
  region = "us-west-2"
}

resource "aws_instance" "example" {
  ami           = var.ami_id
  instance_type = var.instance_type
  subnet_id     = var.subnet_id
  
  tags = var.tags
}

variable "instance_type" {
  description = "The instance type to use"
  type        = string
  default     = "t3.micro"
}

variable "ami_id" {
  description = "The AMI ID to use"
  type        = string
}

variable "subnet_id" {
  description = "The subnet ID to launch the instance in"
  type        = string
}

variable "tags" {
  description = "Tags to apply to the instance"
  type        = map(string)
  default     = {
    Name        = "example-instance"
    Environment = "dev"
  }
}

output "instance_id" {
  description = "The ID of the created instance"
  value       = aws_instance.example.id
}

output "public_ip" {
  description = "The public IP of the created instance"
  value       = aws_instance.example.public_ip
}`,
    createdAt: '2025-05-01T10:00:00Z',
    updatedAt: '2025-05-01T10:00:00Z'
  },
  {
    id: '2',
    name: 'AWS S3 Bucket with Lifecycle Policy',
    description: 'Creates an S3 bucket with lifecycle policy for cost optimization',
    variables: {
      bucket_name: {
        description: 'The name of the S3 bucket',
        type: 'string',
        required: true
      },
      transition_days: {
        description: 'Days after which to transition objects to Glacier',
        type: 'number',
        default: 90,
        required: false
      },
      expiration_days: {
        description: 'Days after which to expire objects',
        type: 'number',
        default: 365,
        required: false
      }
    },
    content: `provider "aws" {
  region = "us-west-2"
}

resource "aws_s3_bucket" "example" {
  bucket = var.bucket_name
  
  lifecycle_rule {
    id      = "archive"
    enabled = true
    
    transition {
      days          = var.transition_days
      storage_class = "GLACIER"
    }
    
    expiration {
      days = var.expiration_days
    }
  }
  
  tags = {
    Name        = var.bucket_name
    Environment = "prod"
    Managed     = "terraform"
  }
}

variable "bucket_name" {
  description = "The name of the S3 bucket"
  type        = string
}

variable "transition_days" {
  description = "Days after which to transition objects to Glacier"
  type        = number
  default     = 90
}

variable "expiration_days" {
  description = "Days after which to expire objects"
  type        = number
  default     = 365
}

output "bucket_id" {
  description = "The ID of the created bucket"
  value       = aws_s3_bucket.example.id
}

output "bucket_arn" {
  description = "The ARN of the created bucket"
  value       = aws_s3_bucket.example.arn
}`,
    createdAt: '2025-05-02T14:30:00Z',
    updatedAt: '2025-05-02T14:30:00Z'
  },
  {
    id: '3',
    name: 'Azure VM with Auto-shutdown',
    description: 'Creates an Azure VM with auto-shutdown schedule for cost optimization',
    variables: {
      vm_name: {
        description: 'The name of the VM',
        type: 'string',
        required: true
      },
      vm_size: {
        description: 'The size of the VM',
        type: 'string',
        default: 'Standard_B1s',
        required: true
      },
      shutdown_time: {
        description: 'The time to shutdown the VM (24h format, UTC)',
        type: 'string',
        default: '1900',
        required: false
      }
    },
    content: `provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "example" {
  name     = "${var.vm_name}-resources"
  location = "West Europe"
}

resource "azurerm_virtual_network" "example" {
  name                = "${var.vm_name}-network"
  address_space       = ["10.0.0.0/16"]
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name
}

resource "azurerm_subnet" "example" {
  name                 = "internal"
  resource_group_name  = azurerm_resource_group.example.name
  virtual_network_name = azurerm_virtual_network.example.name
  address_prefixes     = ["10.0.2.0/24"]
}

resource "azurerm_network_interface" "example" {
  name                = "${var.vm_name}-nic"
  location            = azurerm_resource_group.example.location
  resource_group_name = azurerm_resource_group.example.name

  ip_configuration {
    name                          = "internal"
    subnet_id                     = azurerm_subnet.example.id
    private_ip_address_allocation = "Dynamic"
  }
}

resource "azurerm_linux_virtual_machine" "example" {
  name                = var.vm_name
  resource_group_name = azurerm_resource_group.example.name
  location            = azurerm_resource_group.example.location
  size                = var.vm_size
  admin_username      = "adminuser"
  network_interface_ids = [
    azurerm_network_interface.example.id,
  ]

  admin_ssh_key {
    username   = "adminuser"
    public_key = file("~/.ssh/id_rsa.pub")
  }

  os_disk {
    caching              = "ReadWrite"
    storage_account_type = "Standard_LRS"
  }

  source_image_reference {
    publisher = "Canonical"
    offer     = "UbuntuServer"
    sku       = "18.04-LTS"
    version   = "latest"
  }
}

resource "azurerm_dev_test_global_vm_shutdown_schedule" "example" {
  virtual_machine_id = azurerm_linux_virtual_machine.example.id
  location           = azurerm_resource_group.example.location
  enabled            = true

  daily_recurrence_time = var.shutdown_time
  timezone              = "UTC"

  notification_settings {
    enabled = false
  }
}

variable "vm_name" {
  description = "The name of the VM"
  type        = string
}

variable "vm_size" {
  description = "The size of the VM"
  type        = string
  default     = "Standard_B1s"
}

variable "shutdown_time" {
  description = "The time to shutdown the VM (24h format, UTC)"
  type        = string
  default     = "1900"
}

output "vm_id" {
  description = "The ID of the created VM"
  value       = azurerm_linux_virtual_machine.example.id
}`,
    createdAt: '2025-05-03T09:15:00Z',
    updatedAt: '2025-05-03T09:15:00Z'
  }
];

const mockDeployments: TerraformDeployment[] = [
  {
    id: '1',
    templateId: '1',
    status: 'completed',
    variables: {
      instance_type: 't3.micro',
      ami_id: 'ami-0c55b159cbfafe1f0',
      subnet_id: 'subnet-12345678',
      tags: {
        Name: 'prod-api-server',
        Environment: 'production',
        CostCenter: 'IT-123'
      }
    },
    output: {
      instance_id: 'i-1234567890abcdef0',
      public_ip: '54.123.45.67'
    },
    logs: 'Terraform initialized...\nApplying changes...\nApply complete! Resources: 1 added, 0 changed, 0 destroyed.',
    createdAt: '2025-05-15T10:30:00Z',
    completedAt: '2025-05-15T10:32:00Z'
  },
  {
    id: '2',
    templateId: '2',
    status: 'completed',
    variables: {
      bucket_name: 'cost-optimizer-logs',
      transition_days: 30,
      expiration_days: 180
    },
    output: {
      bucket_id: 'cost-optimizer-logs',
      bucket_arn: 'arn:aws:s3:::cost-optimizer-logs'
    },
    logs: 'Terraform initialized...\nApplying changes...\nApply complete! Resources: 1 added, 0 changed, 0 destroyed.',
    createdAt: '2025-05-16T14:20:00Z',
    completedAt: '2025-05-16T14:21:00Z'
  },
  {
    id: '3',
    templateId: '3',
    status: 'failed',
    variables: {
      vm_name: 'dev-server',
      vm_size: 'Standard_B2s',
      shutdown_time: '2000'
    },
    logs: 'Terraform initialized...\nApplying changes...\nError: Error creating Linux Virtual Machine: compute.VirtualMachinesClient#CreateOrUpdate: Failure sending request: StatusCode=400 -- Original Error: Code="InvalidParameter" Message="The value of parameter linuxConfiguration.ssh.publicKeys.keyData is invalid."',
    createdAt: '2025-05-17T09:15:00Z',
    completedAt: '2025-05-17T09:16:00Z'
  },
  {
    id: '4',
    templateId: '1',
    status: 'planning',
    variables: {
      instance_type: 't3.small',
      ami_id: 'ami-0c55b159cbfafe1f0',
      subnet_id: 'subnet-87654321',
      tags: {
        Name: 'dev-worker',
        Environment: 'development',
        CostCenter: 'IT-456'
      }
    },
    logs: 'Terraform initialized...\nPlanning...',
    createdAt: '2025-05-21T08:10:00Z'
  }
];

const Terraform: React.FC = () => {
  const theme = useTheme();
  const [templates, setTemplates] = useState<TerraformTemplate[]>([]);
  const [deployments, setDeployments] = useState<TerraformDeployment[]>([]);
  const [loading, setLoading] = useState(true);
  const [selectedTemplate, setSelectedTemplate] = useState<TerraformTemplate | null>(null);
  const [selectedDeployment, setSelectedDeployment] = useState<TerraformDeployment | null>(null);
  const [templateDialogOpen, setTemplateDialogOpen] = useState(false);
  const [deployDialogOpen, setDeployDialogOpen] = useState(false);
  const [deploymentDialogOpen, setDeploymentDialogOpen] = useState(false);
  const [deploymentVariables, setDeploymentVariables] = useState<Record<string, any>>({});
  const [activeTab, setActiveTab] = useState<'templates' | 'deployments'>('templates');

  useEffect(() => {
    // Simulate API call
    const timer = setTimeout(() => {
      setTemplates(mockTemplates);
      setDeployments(mockDeployments);
      setLoading(false);
    }, 1000);

    return () => clearTimeout(timer);
  }, []);

  const handleTemplateSelect = (template: TerraformTemplate) => {
    setSelectedTemplate(template);
    setTemplateDialogOpen(true);
  };

  const handleDeploymentSelect = (deployment: TerraformDeployment) => {
    setSelectedDeployment(deployment);
    setDeploymentDialogOpen(true);
  };

  const handleDeployTemplate = (template: TerraformTemplate) => {
    setSelectedTemplate(template);
    
    // Initialize variables with default values
    const initialVariables: Record<string, any> = {};
    Object.entries(template.variables).forEach(([key, variable]) => {
      initialVariables[key] = variable.default !== undefined ? variable.default : '';
    });
    
    setDeploymentVariables(initialVariables);
    setDeployDialogOpen(true);
  };

  const handleDeploySubmit = () => {
    if (!selectedTemplate) return;
    
    console.log(`Deploying template ${selectedTemplate.id} with variables:`, deploymentVariables);
    
    // In a real app, this would call the API to deploy the template
    
    // Simulate deployment creation
    const newDeployment: TerraformDeployment = {
      id: `new-${Date.now()}`,
      templateId: selectedTemplate.id,
      status: 'planning',
      variables: deploymentVariables,
      logs: 'Terraform initialized...\nPlanning...',
      createdAt: new Date().toISOString()
    };
    
    setDeployments([newDeployment, ...deployments]);
    setDeployDialogOpen(false);
    setActiveTab('deployments');
  };

  const handleVariableChange = (key: string, value: any) => {
    setDeploymentVariables(prev => ({
      ...prev,
      [key]: value
    }));
  };

  const formatDate = (dateString: string) => {
    const date = new Date(dateString);
    return date.toLocaleDateString() + ' ' + date.toLocaleTimeString();
  };

  const getStatusChip = (status: string) => {
    switch (status) {
      case 'planning':
        return <Chip size="small" label="Planning" color="info" />;
      case 'applying':
        return <Chip size="small" label="Applying" color="warning" />;
      case 'completed':
        return <Chip size="small" label="Completed" color="success" />;
      case 'failed':
        return <Chip size="small" label="Failed" color="error" />;
      default:
        return null;
    }
  };

  return (
    <Box sx={{ flexGrow: 1 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Terraform Management
        </Typography>
        <Box>
          <Button 
            variant={activeTab === 'templates' ? 'contained' : 'outlined'} 
            onClick={() => setActiveTab('templates')}
            sx={{ mr: 1 }}
          >
            Templates
          </Button>
          <Button 
            variant={activeTab === 'deployments' ? 'contained' : 'outlined'} 
            onClick={() => setActiveTab('deployments')}
          >
            Deployments
          </Button>
        </Box>
      </Box>

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : (
        <>
          {/* Templates Tab */}
          {activeTab === 'templates' && (
            <>
              <Box sx={{ display: 'flex', justifyContent: 'flex-end', mb: 2 }}>
                <Button 
                  variant="contained" 
                  startIcon={<AddIcon />}
                  // In a real app, this would open a dialog to create a new template
                >
                  New Template
                </Button>
              </Box>
              
              <Grid container spacing={3}>
                {templates.map((template) => (
                  <Grid item xs={12} md={6} lg={4} key={template.id}>
                    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
                      <CardHeader 
                        title={template.name}
                        action={
                          <IconButton aria-label="edit">
                            <EditIcon />
                          </IconButton>
                        }
                      />
                      <Divider />
                      <CardContent sx={{ flexGrow: 1 }}>
                        <Typography variant="body2" color="text.secondary" gutterBottom>
                          {template.description}
                        </Typography>
                        <Typography variant="caption" color="text.secondary" display="block" sx={{ mt: 2 }}>
                          Last updated: {formatDate(template.updatedAt)}
                        </Typography>
                      </CardContent>
                      <Divider />
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', p: 1 }}>
                        <Button 
                          size="small" 
                          startIcon={<CodeIcon />}
                          onClick={() => handleTemplateSelect(template)}
                        >
                          View
                        </Button>
                        <Button 
                          size="small" 
                          variant="contained" 
                          color="primary"
                          onClick={() => handleDeployTemplate(template)}
                        >
                          Deploy
                        </Button>
                      </Box>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </>
          )}
          
          {/* Deployments Tab */}
          {activeTab === 'deployments' && (
            <Card>
              <CardHeader title="Deployments" />
              <Divider />
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Template</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Created</TableCell>
                      <TableCell>Completed</TableCell>
                      <TableCell align="right">Actions</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {deployments.length === 0 ? (
                      <TableRow>
                        <TableCell colSpan={5} align="center">
                          No deployments found
                        </TableCell>
                      </TableRow>
                    ) : (
                      deployments.map((deployment) => {
                        const template = templates.find(t => t.id === deployment.templateId);
                        return (
                          <TableRow key={deployment.id}>
                            <TableCell>{template?.name || deployment.templateId}</TableCell>
                            <TableCell>{getStatusChip(deployment.status)}</TableCell>
                            <TableCell>{formatDate(deployment.createdAt)}</TableCell>
                            <TableCell>
                              {deployment.completedAt ? formatDate(deployment.completedAt) : '-'}
                            </TableCell>
                            <TableCell align="right">
                              <Button 
                                size="small" 
                                onClick={() => handleDeploymentSelect(deployment)}
                              >
                                Details
                              </Button>
                            </TableCell>
                          </TableRow>
                        );
                      })
                    )}
                  </TableBody>
                </Table>
              </TableContainer>
            </Card>
          )}
        </>
      )}

      {/* Template Details Dialog */}
      <Dialog
        open={templateDialogOpen}
        onClose={() => setTemplateDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {selectedTemplate?.name}
          <IconButton
            aria-label="close"
            onClick={() => setTemplateDialogOpen(false)}
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
          {selectedTemplate && (
            <>
              <Typography variant="subtitle1" gutterBottom>
                Description
              </Typography>
              <Typography variant="body2" paragraph>
                {selectedTemplate.description}
              </Typography>
              
              <Typography variant="subtitle1" gutterBottom>
                Variables
              </Typography>
              <TableContainer component={Paper} variant="outlined" sx={{ mb: 3 }}>
                <Table size="small">
                  <TableHead>
                    <TableRow>
                      <TableCell>Name</TableCell>
                      <TableCell>Description</TableCell>
                      <TableCell>Type</TableCell>
                      <TableCell>Default</TableCell>
                      <TableCell>Required</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {Object.entries(selectedTemplate.variables).map(([key, variable]) => (
                      <TableRow key={key}>
                        <TableCell>{key}</TableCell>
                        <TableCell>{variable.description}</TableCell>
                        <TableCell>{variable.type}</TableCell>
                        <TableCell>
                          {variable.default !== undefined ? 
                            (typeof variable.default === 'object' ? 
                              JSON.stringify(variable.default) : 
                              String(variable.default)
                            ) : 
                            '-'
                          }
                        </TableCell>
                        <TableCell>{variable.required ? 'Yes' : 'No'}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
              
              <Typography variant="subtitle1" gutterBottom>
                Terraform Configuration
              </Typography>
              <Box sx={{ position: 'relative' }}>
                <Paper 
                  variant="outlined" 
                  sx={{ 
                    p: 2, 
                    backgroundColor: theme.palette.background.default,
                    maxHeight: '400px',
                    overflow: 'auto'
                  }}
                >
                  <pre style={{ margin: 0, fontFamily: 'monospace' }}>
                    {selectedTemplate.content}
                  </pre>
                </Paper>
                <Tooltip title="Copy to clipboard">
                  <IconButton 
                    sx={{ position: 'absolute', top: 8, right: 8 }}
                    onClick={() => {
                      navigator.clipboard.writeText(selectedTemplate.content);
                    }}
                  >
                    <ContentCopyIcon />
                  </IconButton>
                </Tooltip>
              </Box>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTemplateDialogOpen(false)}>Close</Button>
          <Button 
            variant="contained" 
            color="primary"
            onClick={() => {
              setTemplateDialogOpen(false);
              if (selectedTemplate) {
                handleDeployTemplate(selectedTemplate);
              }
            }}
          >
            Deploy
          </Button>
        </DialogActions>
      </Dialog>

      {/* Deploy Template Dialog */}
      <Dialog
        open={deployDialogOpen}
        onClose={() => setDeployDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Deploy Template: {selectedTemplate?.name}
          <IconButton
            aria-label="close"
            onClick={() => setDeployDialogOpen(false)}
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
          {selectedTemplate && (
            <>
              <Typography variant="subtitle1" gutterBottom>
                Configure Variables
              </Typography>
              <Grid container spacing={2}>
                {Object.entries(selectedTemplate.variables).map(([key, variable]) => (
                  <Grid item xs={12} md={6} key={key}>
                    <TextField
                      fullWidth
                      label={`${key}${variable.required ? ' *' : ''}`}
                      helperText={variable.description}
                      value={
                        typeof deploymentVariables[key] === 'object' 
                          ? JSON.stringify(deploymentVariables[key]) 
                          : deploymentVariables[key] || ''
                      }
                      onChange={(e) => handleVariableChange(key, e.target.value)}
                      required={variable.required}
                      error={variable.required && !deploymentVariables[key]}
                    />
                  </Grid>
                ))}
              </Grid>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeployDialogOpen(false)}>Cancel</Button>
          <Button 
            variant="contained" 
            color="primary"
            onClick={handleDeploySubmit}
            disabled={!selectedTemplate || Object.entries(selectedTemplate.variables)
              .some(([key, variable]) => variable.required && !deploymentVariables[key])}
          >
            Deploy
          </Button>
        </DialogActions>
      </Dialog>

      {/* Deployment Details Dialog */}
      <Dialog
        open={deploymentDialogOpen}
        onClose={() => setDeploymentDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Deployment Details
          <IconButton
            aria-label="close"
            onClick={() => setDeploymentDialogOpen(false)}
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
          {selectedDeployment && (
            <>
              <Grid container spacing={2}>
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Template
                  </Typography>
                  <Typography variant="body1">
                    {templates.find(t => t.id === selectedDeployment.templateId)?.name || selectedDeployment.templateId}
                  </Typography>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Status
                  </Typography>
                  <Box>
                    {getStatusChip(selectedDeployment.status)}
                  </Box>
                </Grid>
                
                <Grid item xs={12} md={6}>
                  <Typography variant="subtitle2" color="textSecondary">
                    Created At
                  </Typography>
                  <Typography variant="body1">
                    {formatDate(selectedDeployment.createdAt)}
                  </Typography>
                </Grid>
                
                {selectedDeployment.completedAt && (
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" color="textSecondary">
                      Completed At
                    </Typography>
                    <Typography variant="body1">
                      {formatDate(selectedDeployment.completedAt)}
                    </Typography>
                  </Grid>
                )}
              </Grid>
              
              <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                Variables
              </Typography>
              <Paper variant="outlined" sx={{ p: 2, backgroundColor: theme.palette.background.default }}>
                <pre style={{ margin: 0, overflow: 'auto' }}>
                  {JSON.stringify(selectedDeployment.variables, null, 2)}
                </pre>
              </Paper>
              
              {selectedDeployment.output && (
                <>
                  <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                    Output
                  </Typography>
                  <Paper variant="outlined" sx={{ p: 2, backgroundColor: theme.palette.background.default }}>
                    <pre style={{ margin: 0, overflow: 'auto' }}>
                      {JSON.stringify(selectedDeployment.output, null, 2)}
                    </pre>
                  </Paper>
                </>
              )}
              
              <Typography variant="subtitle1" sx={{ mt: 3, mb: 1 }}>
                Logs
              </Typography>
              <Paper 
                variant="outlined" 
                sx={{ 
                  p: 2, 
                  backgroundColor: theme.palette.background.default,
                  maxHeight: '200px',
                  overflow: 'auto'
                }}
              >
                <pre style={{ margin: 0, fontFamily: 'monospace', whiteSpace: 'pre-wrap' }}>
                  {selectedDeployment.logs}
                </pre>
              </Paper>
            </>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeploymentDialogOpen(false)}>Close</Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default Terraform;

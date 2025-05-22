import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Paper, 
  Grid, 
  Card, 
  CardContent, 
  Button, 
  TextField, 
  Divider, 
  Tabs, 
  Tab, 
  Alert,
  CircularProgress,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem
} from '@mui/material';
import { Add as AddIcon, Delete as DeleteIcon, Edit as EditIcon } from '@mui/icons-material';
import { getCloudAccounts, createCloudAccount, updateCloudAccount, deleteCloudAccount } from '../../lib/cloud-accounts-api';
import { CloudAccount } from '../../lib/types';

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel(props: TabPanelProps) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`cloud-account-tabpanel-${index}`}
      aria-labelledby={`cloud-account-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

const CloudAccounts: React.FC = () => {
  const [tabValue, setTabValue] = useState(0);
  const [accounts, setAccounts] = useState<CloudAccount[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [openDialog, setOpenDialog] = useState(false);
  const [editingAccount, setEditingAccount] = useState<CloudAccount | null>(null);
  
  // Form state
  const [accountName, setAccountName] = useState('');
  const [accountProvider, setAccountProvider] = useState<'aws' | 'azure' | 'gcp'>('aws');
  const [awsAccessKey, setAwsAccessKey] = useState('');
  const [awsSecretKey, setAwsSecretKey] = useState('');
  const [gcpCredentials, setGcpCredentials] = useState('');
  const [azureTenantId, setAzureTenantId] = useState('');
  const [azureClientId, setAzureClientId] = useState('');
  const [azureClientSecret, setAzureClientSecret] = useState('');
  const [formError, setFormError] = useState<string | null>(null);

  useEffect(() => {
    fetchAccounts();
  }, []);

  const fetchAccounts = async () => {
    setLoading(true);
    try {
      const response = await getCloudAccounts();
      if (response.success && response.data) {
        setAccounts(response.data);
      } else {
        setError(response.error || 'Failed to fetch cloud accounts');
      }
    } catch (err) {
      setError('An error occurred while fetching cloud accounts');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleTabChange = (event: React.SyntheticEvent, newValue: number) => {
    setTabValue(newValue);
  };

  const handleOpenDialog = (account?: CloudAccount) => {
    if (account) {
      setEditingAccount(account);
      setAccountName(account.name);
      setAccountProvider(account.provider);
      // In a real app, you wouldn't pre-fill credentials for security reasons
    } else {
      setEditingAccount(null);
      resetForm();
    }
    setOpenDialog(true);
  };

  const handleCloseDialog = () => {
    setOpenDialog(false);
    resetForm();
  };

  const resetForm = () => {
    setAccountName('');
    setAccountProvider('aws');
    setAwsAccessKey('');
    setAwsSecretKey('');
    setGcpCredentials('');
    setAzureTenantId('');
    setAzureClientId('');
    setAzureClientSecret('');
    setFormError(null);
  };

  const validateForm = () => {
    if (!accountName.trim()) {
      setFormError('Account name is required');
      return false;
    }

    if (accountProvider === 'aws') {
      if (!awsAccessKey.trim() || !awsSecretKey.trim()) {
        setFormError('AWS Access Key and Secret Key are required');
        return false;
      }
    } else if (accountProvider === 'gcp') {
      if (!gcpCredentials.trim()) {
        setFormError('GCP Service Account JSON is required');
        return false;
      }
      try {
        JSON.parse(gcpCredentials);
      } catch (e) {
        setFormError('GCP Service Account JSON is not valid JSON');
        return false;
      }
    } else if (accountProvider === 'azure') {
      if (!azureTenantId.trim() || !azureClientId.trim() || !azureClientSecret.trim()) {
        setFormError('Azure Tenant ID, Client ID, and Client Secret are required');
        return false;
      }
    }

    setFormError(null);
    return true;
  };

  const handleSubmit = async () => {
    if (!validateForm()) return;

    setLoading(true);
    try {
      let credentials: any = {};
      
      if (accountProvider === 'aws') {
        credentials = {
          accessKey: awsAccessKey,
          secretKey: awsSecretKey
        };
      } else if (accountProvider === 'gcp') {
        credentials = {
          serviceAccountJson: gcpCredentials
        };
      } else if (accountProvider === 'azure') {
        credentials = {
          tenantId: azureTenantId,
          clientId: azureClientId,
          clientSecret: azureClientSecret
        };
      }

      const accountData = {
        name: accountName,
        provider: accountProvider,
        credentials
      };

      let response;
      if (editingAccount) {
        response = await updateCloudAccount(editingAccount.id, accountData);
      } else {
        response = await createCloudAccount(accountData);
      }

      if (response.success) {
        handleCloseDialog();
        fetchAccounts();
      } else {
        setFormError(response.error || 'Failed to save cloud account');
      }
    } catch (err) {
      setFormError('An error occurred while saving the cloud account');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteAccount = async (accountId: string) => {
    if (!window.confirm('Are you sure you want to delete this cloud account?')) {
      return;
    }

    setLoading(true);
    try {
      const response = await deleteCloudAccount(accountId);
      if (response.success) {
        fetchAccounts();
      } else {
        setError(response.error || 'Failed to delete cloud account');
      }
    } catch (err) {
      setError('An error occurred while deleting the cloud account');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const renderAccountForm = () => {
    return (
      <Box>
        {formError && (
          <Alert severity="error" sx={{ mb: 2 }}>
            {formError}
          </Alert>
        )}
        
        <TextField
          fullWidth
          label="Account Name"
          value={accountName}
          onChange={(e) => setAccountName(e.target.value)}
          margin="normal"
          required
        />
        
        <FormControl fullWidth margin="normal" required>
          <InputLabel>Cloud Provider</InputLabel>
          <Select
            value={accountProvider}
            onChange={(e) => setAccountProvider(e.target.value as 'aws' | 'azure' | 'gcp')}
            label="Cloud Provider"
          >
            <MenuItem value="aws">AWS</MenuItem>
            <MenuItem value="gcp">Google Cloud Platform</MenuItem>
            <MenuItem value="azure">Microsoft Azure</MenuItem>
          </Select>
        </FormControl>
        
        {accountProvider === 'aws' && (
          <>
            <TextField
              fullWidth
              label="AWS Access Key"
              value={awsAccessKey}
              onChange={(e) => setAwsAccessKey(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="AWS Secret Key"
              value={awsSecretKey}
              onChange={(e) => setAwsSecretKey(e.target.value)}
              margin="normal"
              type="password"
              required
            />
          </>
        )}
        
        {accountProvider === 'gcp' && (
          <TextField
            fullWidth
            label="GCP Service Account JSON"
            value={gcpCredentials}
            onChange={(e) => setGcpCredentials(e.target.value)}
            margin="normal"
            multiline
            rows={4}
            required
          />
        )}
        
        {accountProvider === 'azure' && (
          <>
            <TextField
              fullWidth
              label="Azure Tenant ID"
              value={azureTenantId}
              onChange={(e) => setAzureTenantId(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Azure Client ID"
              value={azureClientId}
              onChange={(e) => setAzureClientId(e.target.value)}
              margin="normal"
              required
            />
            <TextField
              fullWidth
              label="Azure Client Secret"
              value={azureClientSecret}
              onChange={(e) => setAzureClientSecret(e.target.value)}
              margin="normal"
              type="password"
              required
            />
          </>
        )}
      </Box>
    );
  };

  const renderAccountsList = (provider: 'aws' | 'azure' | 'gcp') => {
    const filteredAccounts = accounts.filter(account => account.provider === provider);
    
    if (filteredAccounts.length === 0) {
      return (
        <Box sx={{ textAlign: 'center', py: 4 }}>
          <Typography variant="body1" color="text.secondary">
            No {provider.toUpperCase()} accounts configured
          </Typography>
          <Button 
            variant="contained" 
            startIcon={<AddIcon />}
            onClick={() => {
              setAccountProvider(provider);
              handleOpenDialog();
            }}
            sx={{ mt: 2 }}
          >
            Add {provider.toUpperCase()} Account
          </Button>
        </Box>
      );
    }
    
    return (
      <Grid container spacing={3}>
        {filteredAccounts.map(account => (
          <Grid item xs={12} md={6} lg={4} key={account.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="h6">{account.name}</Typography>
                  <Box>
                    <IconButton size="small" onClick={() => handleOpenDialog(account)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton size="small" onClick={() => handleDeleteAccount(account.id)}>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
                
                <Typography variant="body2" color="text.secondary">
                  Status: <span style={{ color: account.status === 'active' ? 'green' : account.status === 'error' ? 'red' : 'orange' }}>
                    {account.status.charAt(0).toUpperCase() + account.status.slice(1)}
                  </span>
                </Typography>
                
                {account.lastSyncTime && (
                  <Typography variant="body2" color="text.secondary">
                    Last synced: {new Date(account.lastSyncTime).toLocaleString()}
                  </Typography>
                )}
              </CardContent>
            </Card>
          </Grid>
        ))}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 2 }}>
            <Button 
              variant="contained" 
              startIcon={<AddIcon />}
              onClick={() => {
                setAccountProvider(provider);
                handleOpenDialog();
              }}
            >
              Add Another {provider.toUpperCase()} Account
            </Button>
          </Box>
        </Grid>
      </Grid>
    );
  };

  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Cloud Accounts
      </Typography>
      
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
          <Button onClick={fetchAccounts} size="small" sx={{ ml: 2 }}>
            Retry
          </Button>
        </Alert>
      )}
      
      <Paper sx={{ width: '100%' }}>
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs 
            value={tabValue} 
            onChange={handleTabChange} 
            aria-label="cloud provider tabs"
            variant="fullWidth"
          >
            <Tab label="AWS" id="cloud-account-tab-0" aria-controls="cloud-account-tabpanel-0" />
            <Tab label="Google Cloud" id="cloud-account-tab-1" aria-controls="cloud-account-tabpanel-1" />
            <Tab label="Azure" id="cloud-account-tab-2" aria-controls="cloud-account-tabpanel-2" />
          </Tabs>
        </Box>
        
        {loading && accounts.length === 0 ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', p: 4 }}>
            <CircularProgress />
          </Box>
        ) : (
          <>
            <TabPanel value={tabValue} index={0}>
              {renderAccountsList('aws')}
            </TabPanel>
            <TabPanel value={tabValue} index={1}>
              {renderAccountsList('gcp')}
            </TabPanel>
            <TabPanel value={tabValue} index={2}>
              {renderAccountsList('azure')}
            </TabPanel>
          </>
        )}
      </Paper>
      
      <Dialog open={openDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
        <DialogTitle>
          {editingAccount ? 'Edit Cloud Account' : 'Add Cloud Account'}
        </DialogTitle>
        <DialogContent>
          {renderAccountForm()}
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseDialog}>Cancel</Button>
          <Button 
            onClick={handleSubmit} 
            variant="contained" 
            disabled={loading}
          >
            {loading ? <CircularProgress size={24} /> : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default CloudAccounts;

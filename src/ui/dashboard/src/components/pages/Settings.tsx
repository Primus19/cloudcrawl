import React from 'react';
import { Box, Typography, Paper, Grid, Card, CardContent, CardHeader, TextField, Button, Switch, FormControlLabel, Divider } from '@mui/material';

const Settings: React.FC = () => {
  return (
    <Box sx={{ p: 3 }}>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Account Settings
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            <Box sx={{ mb: 3 }}>
              <TextField
                fullWidth
                label="Email Address"
                defaultValue="admin@example.com"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Username"
                defaultValue="admin"
                margin="normal"
              />
              <Button variant="contained" color="primary" sx={{ mt: 2 }}>
                Update Account
              </Button>
            </Box>
            
            <Typography variant="h6" gutterBottom sx={{ mt: 4 }}>
              Password
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            <Box>
              <TextField
                fullWidth
                label="Current Password"
                type="password"
                margin="normal"
              />
              <TextField
                fullWidth
                label="New Password"
                type="password"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Confirm New Password"
                type="password"
                margin="normal"
              />
              <Button variant="contained" color="primary" sx={{ mt: 2 }}>
                Change Password
              </Button>
            </Box>
          </Paper>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Notification Settings
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Email Notifications"
            />
            <Typography variant="body2" color="textSecondary" sx={{ ml: 4, mb: 2 }}>
              Receive email notifications for cost alerts and recommendations
            </Typography>
            
            <FormControlLabel
              control={<Switch defaultChecked />}
              label="Weekly Cost Reports"
            />
            <Typography variant="body2" color="textSecondary" sx={{ ml: 4, mb: 2 }}>
              Receive weekly cost summary reports
            </Typography>
            
            <FormControlLabel
              control={<Switch />}
              label="SMS Notifications"
            />
            <Typography variant="body2" color="textSecondary" sx={{ ml: 4, mb: 2 }}>
              Receive SMS alerts for critical cost events
            </Typography>
            
            <TextField
              fullWidth
              label="Alert Threshold (%)"
              type="number"
              defaultValue="10"
              margin="normal"
              helperText="Send alerts when costs exceed budget by this percentage"
            />
            
            <Button variant="contained" color="primary" sx={{ mt: 2 }}>
              Save Notification Settings
            </Button>
          </Paper>
          
          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              API Keys
            </Typography>
            <Divider sx={{ mb: 3 }} />
            
            <TextField
              fullWidth
              label="API Key"
              value="••••••••••••••••••••••••••••••"
              InputProps={{
                readOnly: true,
              }}
              margin="normal"
            />
            
            <Box sx={{ display: 'flex', mt: 2 }}>
              <Button variant="outlined" sx={{ mr: 1 }}>
                Regenerate Key
              </Button>
              <Button variant="contained">
                Copy Key
              </Button>
            </Box>
          </Paper>
        </Grid>
      </Grid>
    </Box>
  );
};

export default Settings;

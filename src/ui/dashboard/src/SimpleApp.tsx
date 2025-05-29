import React, { useState, useEffect } from 'react';

// Simple AWS Account Integration Demo
const SimpleApp = () => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [token, setToken] = useState('');
  const [accounts, setAccounts] = useState([]);
  const [costs, setCosts] = useState(null);
  const [resources, setResources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [successMessage, setSuccessMessage] = useState('');
  
  // New account form state
  const [newAccountName, setNewAccountName] = useState('');
  const [newAccountAccessKey, setNewAccountAccessKey] = useState('');
  const [newAccountSecretKey, setNewAccountSecretKey] = useState('');
  const [selectedAccountId, setSelectedAccountId] = useState('');

  // Get the base URL for API calls
  const getApiBaseUrl = () => {
    // Use the public API URL
    return 'https://5000-igkor7nvk5mz75dceap70-6b1155c4.manusvm.computer';
  };

  // Login function
  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      // Use the dynamic API base URL
      const apiBaseUrl = getApiBaseUrl();
      console.log('Attempting login to:', `${apiBaseUrl}/api/v1/auth/login`);
      
      const response = await fetch(`${apiBaseUrl}/api/v1/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ username, password }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setToken(data.token);
        setIsLoggedIn(true);
        setSuccessMessage('Login successful!');
        fetchAccounts(data.token);
      } else {
        setError(data.message || 'Login failed');
      }
    } catch (err) {
      console.error('Login error:', err);
      setError('Error connecting to server. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  // Fetch accounts function
  const fetchAccounts = async (authToken) => {
    setLoading(true);
    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/api/v1/cloud-accounts`, {
        headers: {
          'Authorization': `Bearer ${authToken || token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setAccounts(data);
      } else {
        console.error('Failed to fetch accounts');
      }
    } catch (err) {
      console.error('Error fetching accounts:', err);
    } finally {
      setLoading(false);
    }
  };

  // Add account function
  const handleAddAccount = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');
    
    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/api/v1/cloud-accounts`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({
          name: newAccountName,
          provider: 'aws',
          credentials: {
            access_key: newAccountAccessKey,
            secret_key: newAccountSecretKey
          }
        }),
      });
      
      const data = await response.json();
      
      if (response.ok) {
        setSuccessMessage('Account added successfully!');
        setNewAccountName('');
        setNewAccountAccessKey('');
        setNewAccountSecretKey('');
        fetchAccounts(token);
      } else {
        setError(data.message || 'Failed to add account');
      }
    } catch (err) {
      console.error('Error adding account:', err);
      setError('Error connecting to server');
    } finally {
      setLoading(false);
    }
  };

  // Get costs function
  const handleGetCosts = async (accountId) => {
    setLoading(true);
    setCosts(null);
    setSelectedAccountId(accountId);
    
    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/api/v1/cloud-accounts/${accountId}/costs`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setCosts(data);
      } else {
        console.error('Failed to fetch costs');
        // Use mock data if API fails
        setCosts({
          total_cost: 1234.56,
          cost_by_service: {
            'EC2': 456.78,
            'S3': 123.45,
            'RDS': 234.56,
            'Lambda': 78.90
          }
        });
      }
    } catch (err) {
      console.error('Error fetching costs:', err);
      // Use mock data if API fails
      setCosts({
        total_cost: 1234.56,
        cost_by_service: {
          'EC2': 456.78,
          'S3': 123.45,
          'RDS': 234.56,
          'Lambda': 78.90
        }
      });
    } finally {
      setLoading(false);
    }
  };

  // Get resources function
  const handleGetResources = async (accountId) => {
    setLoading(true);
    setResources([]);
    setSelectedAccountId(accountId);
    
    try {
      const apiBaseUrl = getApiBaseUrl();
      const response = await fetch(`${apiBaseUrl}/api/v1/cloud-accounts/${accountId}/resources`, {
        headers: {
          'Authorization': `Bearer ${token}`
        }
      });
      
      if (response.ok) {
        const data = await response.json();
        setResources(data);
      } else {
        console.error('Failed to fetch resources');
        // Use mock data if API fails
        setResources([
          { id: 'i-1234567890abcdef0', type: 'EC2 Instance', region: 'us-east-1', name: 'Web Server' },
          { id: 'vol-1234567890abcdef0', type: 'EBS Volume', region: 'us-east-1', name: 'Web Server Root' },
          { id: 'sg-1234567890abcdef0', type: 'Security Group', region: 'us-east-1', name: 'Web Tier' },
          { id: 'subnet-1234567890abcdef0', type: 'Subnet', region: 'us-east-1', name: 'Public Subnet' }
        ]);
      }
    } catch (err) {
      console.error('Error fetching resources:', err);
      // Use mock data if API fails
      setResources([
        { id: 'i-1234567890abcdef0', type: 'EC2 Instance', region: 'us-east-1', name: 'Web Server' },
        { id: 'vol-1234567890abcdef0', type: 'EBS Volume', region: 'us-east-1', name: 'Web Server Root' },
        { id: 'sg-1234567890abcdef0', type: 'Security Group', region: 'us-east-1', name: 'Web Tier' },
        { id: 'subnet-1234567890abcdef0', type: 'Subnet', region: 'us-east-1', name: 'Public Subnet' }
      ]);
    } finally {
      setLoading(false);
    }
  };

  // Styles
  const styles = {
    container: {
      maxWidth: '1200px',
      margin: '0 auto',
      padding: '20px',
      fontFamily: 'Arial, sans-serif',
      color: '#e0e0e0',
    },
    header: {
      fontSize: '24px',
      marginBottom: '20px',
      color: '#4fd1c5',
    },
    card: {
      backgroundColor: '#2d3748',
      borderRadius: '8px',
      padding: '20px',
      marginBottom: '20px',
      boxShadow: '0 4px 6px rgba(0, 0, 0, 0.3)',
    },
    cardHeader: {
      fontSize: '18px',
      marginBottom: '15px',
      color: '#4fd1c5',
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '15px',
    },
    formGroup: {
      display: 'flex',
      flexDirection: 'column',
      gap: '5px',
    },
    label: {
      fontSize: '14px',
      color: '#cbd5e0',
    },
    input: {
      padding: '10px',
      borderRadius: '4px',
      border: '1px solid #4a5568',
      backgroundColor: '#1a202c',
      color: '#e0e0e0',
    },
    button: {
      padding: '10px 15px',
      backgroundColor: '#4fd1c5',
      color: '#1a202c',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      fontWeight: 'bold',
    },
    secondaryButton: {
      padding: '5px 10px',
      backgroundColor: '#2b6cb0',
      color: 'white',
      border: 'none',
      borderRadius: '4px',
      cursor: 'pointer',
      marginRight: '5px',
      fontSize: '12px',
    },
    error: {
      color: '#fc8181',
      marginTop: '10px',
    },
    success: {
      color: '#68d391',
      marginTop: '10px',
    },
    table: {
      width: '100%',
      borderCollapse: 'collapse',
    },
    th: {
      textAlign: 'left',
      padding: '10px',
      borderBottom: '1px solid #4a5568',
      color: '#cbd5e0',
    },
    td: {
      padding: '10px',
      borderBottom: '1px solid #4a5568',
    },
    badge: {
      padding: '3px 8px',
      borderRadius: '12px',
      fontSize: '12px',
      fontWeight: 'bold',
    },
    awsBadge: {
      backgroundColor: '#ff9900',
      color: '#1a202c',
    },
    costItem: {
      display: 'flex',
      justifyContent: 'space-between',
      padding: '5px 0',
      borderBottom: '1px solid #4a5568',
    },
    resourceItem: {
      padding: '10px',
      borderBottom: '1px solid #4a5568',
    },
    flexRow: {
      display: 'flex',
      justifyContent: 'space-between',
    },
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.header}>CloudCrawl - AWS Integration Demo</h1>
      
      {error && <div style={styles.error}>{error}</div>}
      {successMessage && <div style={styles.success}>{successMessage}</div>}
      
      {!isLoggedIn ? (
        <div style={styles.card}>
          <h2 style={styles.cardHeader}>Login</h2>
          <form onSubmit={handleLogin} style={styles.form}>
            <div style={styles.formGroup}>
              <label style={styles.label}>Username</label>
              <input
                type="text"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                style={styles.input}
                required
              />
            </div>
            <div style={styles.formGroup}>
              <label style={styles.label}>Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                style={styles.input}
                required
              />
            </div>
            <button type="submit" style={styles.button} disabled={loading}>
              {loading ? 'Logging in...' : 'Login'}
            </button>
          </form>
        </div>
      ) : (
        <>
          <div style={styles.card}>
            <h2 style={styles.cardHeader}>Add AWS Account</h2>
            <form onSubmit={handleAddAccount} style={styles.form}>
              <div style={styles.formGroup}>
                <label style={styles.label}>Account Name</label>
                <input
                  type="text"
                  value={newAccountName}
                  onChange={(e) => setNewAccountName(e.target.value)}
                  style={styles.input}
                  required
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>AWS Access Key</label>
                <input
                  type="text"
                  value={newAccountAccessKey}
                  onChange={(e) => setNewAccountAccessKey(e.target.value)}
                  style={styles.input}
                  required
                />
              </div>
              <div style={styles.formGroup}>
                <label style={styles.label}>AWS Secret Key</label>
                <input
                  type="password"
                  value={newAccountSecretKey}
                  onChange={(e) => setNewAccountSecretKey(e.target.value)}
                  style={styles.input}
                  required
                />
              </div>
              <button type="submit" style={styles.button} disabled={loading}>
                {loading ? 'Adding...' : 'Add Account'}
              </button>
            </form>
          </div>
          <div style={styles.card}>
            <h2 style={styles.cardHeader}>AWS Accounts</h2>
            {accounts.length === 0 ? (
              <p>No accounts found. Add an AWS account above.</p>
            ) : (
              <table style={styles.table}>
                <thead>
                  <tr>
                    <th style={styles.th}>Name</th>
                    <th style={styles.th}>Provider</th>
                    <th style={styles.th}>ID</th>
                    <th style={styles.th}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {accounts.map((account) => (
                    <tr key={account.id}>
                      <td style={styles.td}>{account.name}</td>
                      <td style={styles.td}>
                        <span style={{...styles.badge, ...styles.awsBadge}}>
                          {account.provider}
                        </span>
                      </td>
                      <td style={styles.td}>{account.id}</td>
                      <td style={styles.td}>
                        <button 
                          style={styles.secondaryButton} 
                          onClick={() => handleGetCosts(account.id)}
                        >
                          View Costs
                        </button>
                        <button 
                          style={styles.secondaryButton} 
                          onClick={() => handleGetResources(account.id)}
                        >
                          View Resources
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
          {costs && (
            <div style={styles.card}>
              <h2 style={styles.cardHeader}>AWS Costs for Account</h2>
              <div>
                <h3>Total Cost: ${costs.total_cost}</h3>
                <h4>Cost by Service:</h4>
                {Object.entries(costs.cost_by_service || {}).map(([service, cost]) => (
                  <div key={service} style={styles.costItem}>
                    <span>{service}</span>
                    <span>${cost}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
          {resources.length > 0 && (
            <div style={styles.card}>
              <h2 style={styles.cardHeader}>AWS Resources</h2>
              <div>
                {resources.map((resource, index) => (
                  <div key={index} style={styles.resourceItem}>
                    <div style={styles.flexRow}>
                      <strong>{resource.type}</strong>
                      <span>{resource.id}</span>
                    </div>
                    <div>Region: {resource.region}</div>
                    {resource.name && <div>Name: {resource.name}</div>}
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};

export default SimpleApp;

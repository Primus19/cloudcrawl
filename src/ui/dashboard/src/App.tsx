import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, CssBaseline } from '@mui/material';
import theme from './lib/theme';

// Layout components
import Layout from './components/layout/Layout';

// Page components
import Dashboard from './components/pages/Dashboard';
import CostExplorer from './components/pages/CostExplorer';
import Resources from './components/pages/Resources';
import Recommendations from './components/pages/Recommendations';
import Actions from './components/pages/Actions';
import Workflows from './components/pages/Workflows';
import Terraform from './components/pages/Terraform';
import Settings from './components/pages/Settings';
import CloudAccounts from './components/pages/CloudAccounts';
import NotFound from './components/pages/NotFound';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route index element={<Dashboard />} />
            <Route path="costs" element={<CostExplorer />} />
            <Route path="resources" element={<Resources />} />
            <Route path="recommendations" element={<Recommendations />} />
            <Route path="actions" element={<Actions />} />
            <Route path="workflows" element={<Workflows />} />
            <Route path="terraform" element={<Terraform />} />
            <Route path="cloud-accounts" element={<CloudAccounts />} />
            <Route path="settings" element={<Settings />} />
            <Route path="*" element={<NotFound />} />
          </Route>
        </Routes>
      </Router>
    </ThemeProvider>
  );
}

export default App;

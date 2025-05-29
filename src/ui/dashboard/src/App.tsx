/**
 * App Component
 * Main application component with routing
 */

import React from 'react';
import { ChakraProvider, Box, Flex } from '@chakra-ui/react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { theme } from './lib/theme';
import Sidebar from './components/layout/Sidebar';
import Header from './components/layout/Header';
import Dashboard from './pages/Dashboard';
import CostExplorer from './pages/CostExplorer';
import Resources from './pages/Resources';
import Recommendations from './pages/Recommendations';
import Actions from './pages/Actions';
import Workflows from './pages/Workflows';
import CloudAccountsPage from './pages/CloudAccountsPage';
import TerraformPage from './pages/TerraformPage';
import Settings from './pages/Settings';
import Login from './pages/Login';
import { AuthProvider, useAuth } from './contexts/AuthContext';

const AppContent = () => {
  const { isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Login />;
  }

  return (
    <Flex h="100vh">
      <Sidebar />
      <Box flex="1" bg="gray.900" overflowY="auto">
        <Header />
        <Box as="main" p={4}>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/cost-explorer" element={<CostExplorer />} />
            <Route path="/resources" element={<Resources />} />
            <Route path="/recommendations" element={<Recommendations />} />
            <Route path="/actions" element={<Actions />} />
            <Route path="/workflows" element={<Workflows />} />
            <Route path="/cloud-accounts" element={<CloudAccountsPage />} />
            <Route path="/terraform" element={<TerraformPage />} />
            <Route path="/settings" element={<Settings />} />
          </Routes>
        </Box>
      </Box>
    </Flex>
  );
};

const App = () => {
  return (
    <ChakraProvider theme={theme}>
      <Router>
        <AuthProvider>
          <AppContent />
        </AuthProvider>
      </Router>
    </ChakraProvider>
  );
};

export default App;

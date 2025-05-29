/**
 * Settings Page
 * Application settings and configuration
 */

import React from 'react';
import {
  Box,
  Container,
  Heading,
  Text,
  Tabs,
  TabList,
  TabPanels,
  Tab,
  TabPanel,
  FormControl,
  FormLabel,
  Input,
  Switch,
  Button,
  VStack,
  HStack,
  Divider,
  Card,
  CardBody,
  CardHeader,
  Select
} from '@chakra-ui/react';

const Settings: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Settings</Heading>
          <Text color="gray.300">
            Configure application preferences and account settings
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>General</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Account</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Notifications</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>API Keys</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">General Settings</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={6} align="stretch">
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="dark-mode" mb="0" color="white">
                        Dark Mode
                      </FormLabel>
                      <Switch id="dark-mode" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="auto-refresh" mb="0" color="white">
                        Auto-refresh Data
                      </FormLabel>
                      <Switch id="auto-refresh" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Default Currency</FormLabel>
                      <Select 
                        defaultValue="usd" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      >
                        <option value="usd">USD ($)</option>
                        <option value="eur">EUR (€)</option>
                        <option value="gbp">GBP (£)</option>
                        <option value="jpy">JPY (¥)</option>
                      </Select>
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Data Refresh Interval</FormLabel>
                      <Select 
                        defaultValue="30" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      >
                        <option value="15">Every 15 minutes</option>
                        <option value="30">Every 30 minutes</option>
                        <option value="60">Every hour</option>
                        <option value="360">Every 6 hours</option>
                        <option value="720">Every 12 hours</option>
                        <option value="1440">Every 24 hours</option>
                      </Select>
                    </FormControl>
                    
                    <Button colorScheme="cyan" alignSelf="flex-end">
                      Save Changes
                    </Button>
                  </VStack>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Account Settings</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={6} align="stretch">
                    <FormControl>
                      <FormLabel color="white">Full Name</FormLabel>
                      <Input 
                        defaultValue="Admin User" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Email Address</FormLabel>
                      <Input 
                        defaultValue="admin@example.com" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Username</FormLabel>
                      <Input 
                        defaultValue="admin" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                        isReadOnly
                      />
                    </FormControl>
                    
                    <Divider borderColor="gray.600" />
                    
                    <Heading size="sm" color="white">Change Password</Heading>
                    
                    <FormControl>
                      <FormLabel color="white">Current Password</FormLabel>
                      <Input 
                        type="password" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">New Password</FormLabel>
                      <Input 
                        type="password" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Confirm New Password</FormLabel>
                      <Input 
                        type="password" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <Button colorScheme="cyan" alignSelf="flex-end">
                      Update Account
                    </Button>
                  </VStack>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Notification Settings</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={6} align="stretch">
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="email-alerts" mb="0" color="white">
                        Email Alerts
                      </FormLabel>
                      <Switch id="email-alerts" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="cost-alerts" mb="0" color="white">
                        Cost Threshold Alerts
                      </FormLabel>
                      <Switch id="cost-alerts" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="security-alerts" mb="0" color="white">
                        Security Alerts
                      </FormLabel>
                      <Switch id="security-alerts" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl display="flex" alignItems="center" justifyContent="space-between">
                      <FormLabel htmlFor="resource-alerts" mb="0" color="white">
                        Resource Usage Alerts
                      </FormLabel>
                      <Switch id="resource-alerts" colorScheme="cyan" defaultChecked />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Alert Email Address</FormLabel>
                      <Input 
                        defaultValue="admin@example.com" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <Button colorScheme="cyan" alignSelf="flex-end">
                      Save Notification Settings
                    </Button>
                  </VStack>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">API Keys</Heading>
                </CardHeader>
                <CardBody>
                  <VStack spacing={6} align="stretch">
                    <Text color="gray.300">
                      Generate API keys to access CloudCrawl programmatically. API keys provide full access to your account, so keep them secure.
                    </Text>
                    
                    <FormControl>
                      <FormLabel color="white">API Key Name</FormLabel>
                      <Input 
                        placeholder="Enter a name for your API key" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      />
                    </FormControl>
                    
                    <FormControl>
                      <FormLabel color="white">Expiration</FormLabel>
                      <Select 
                        defaultValue="30" 
                        bg="gray.700" 
                        borderColor="gray.600"
                        color="white"
                        _hover={{ borderColor: "cyan.400" }}
                      >
                        <option value="7">7 days</option>
                        <option value="30">30 days</option>
                        <option value="90">90 days</option>
                        <option value="365">1 year</option>
                        <option value="0">Never</option>
                      </Select>
                    </FormControl>
                    
                    <Button colorScheme="cyan">
                      Generate New API Key
                    </Button>
                    
                    <Divider borderColor="gray.600" />
                    
                    <Heading size="sm" color="white">Your API Keys</Heading>
                    
                    <Text color="gray.300">
                      No API keys found. Generate a new key to get started.
                    </Text>
                  </VStack>
                </CardBody>
              </Card>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
};

export default Settings;

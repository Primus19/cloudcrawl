/**
 * Cloud Accounts List Component
 * Displays a list of cloud provider accounts
 */

import React, { useState, useEffect } from 'react';
import {
  Box,
  Button,
  Heading,
  Text,
  VStack,
  HStack,
  Badge,
  Spinner,
  useToast,
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
  CardFooter,
  Divider,
  IconButton,
  Flex,
  Tooltip
} from '@chakra-ui/react';
import { DeleteIcon, ViewIcon, RepeatIcon } from '@chakra-ui/icons';
import { FaAws, FaMicrosoft, FaGoogle } from 'react-icons/fa';
import { getAllCloudAccounts, deleteCloudAccount, getCloudAccountCosts } from '../../services/cloudAccounts';
import { getAWSResources } from '../../services/awsResources';

interface CloudAccountsListProps {
  refreshTrigger: number;
  onViewAccount?: (account: any) => void;
}

const CloudAccountsList: React.FC<CloudAccountsListProps> = ({ refreshTrigger, onViewAccount }) => {
  const [accounts, setAccounts] = useState<any>({});
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [costs, setCosts] = useState<Record<string, any>>({});
  const [loadingCosts, setLoadingCosts] = useState<Record<string, boolean>>({});
  const [resources, setResources] = useState<Record<string, any>>({});
  const [loadingResources, setLoadingResources] = useState<Record<string, boolean>>({});
  
  const toast = useToast();

  // Fetch accounts on component mount and when refreshTrigger changes
  useEffect(() => {
    fetchAccounts();
  }, [refreshTrigger]);

  const fetchAccounts = async () => {
    setLoading(true);
    setError('');
    
    try {
      const data = await getAllCloudAccounts();
      setAccounts(data);
      
      // Initialize cost loading state for each account
      const initialLoadingState: Record<string, boolean> = {};
      Object.keys(data).forEach(provider => {
        data[provider].forEach((account: any) => {
          initialLoadingState[`${provider}-${account.id}`] = false;
        });
      });
      
      setLoadingCosts(initialLoadingState);
      setLoadingResources({...initialLoadingState});
      
    } catch (err: any) {
      console.error('Error fetching cloud accounts:', err);
      setError(err.message || 'An error occurred while fetching accounts');
      
      toast({
        title: 'Error',
        description: err.message || 'An error occurred while fetching accounts',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (provider: string, accountId: string, accountName: string) => {
    if (!window.confirm(`Are you sure you want to delete ${accountName}?`)) {
      return;
    }
    
    try {
      await deleteCloudAccount(provider, accountId);
      
      toast({
        title: 'Account deleted',
        description: `${provider.toUpperCase()} account "${accountName}" has been deleted.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      
      // Refresh accounts
      fetchAccounts();
    } catch (err: any) {
      console.error('Error deleting cloud account:', err);
      
      toast({
        title: 'Error',
        description: err.message || 'An error occurred while deleting the account',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  const fetchCosts = async (provider: string, accountId: string) => {
    const key = `${provider}-${accountId}`;
    setLoadingCosts(prev => ({ ...prev, [key]: true }));
    
    try {
      const costData = await getCloudAccountCosts(provider, accountId);
      setCosts(prev => ({ ...prev, [key]: costData }));
    } catch (err: any) {
      console.error(`Error fetching costs for ${provider} account ${accountId}:`, err);
      
      toast({
        title: 'Error',
        description: `Failed to fetch cost data: ${err.message || 'Unknown error'}`,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoadingCosts(prev => ({ ...prev, [key]: false }));
    }
  };

  const fetchResources = async (provider: string, accountId: string) => {
    if (provider !== 'aws') return; // Only implemented for AWS currently
    
    const key = `${provider}-${accountId}`;
    setLoadingResources(prev => ({ ...prev, [key]: true }));
    
    try {
      const resourceData = await getAWSResources(accountId);
      setResources(prev => ({ ...prev, [key]: resourceData }));
    } catch (err: any) {
      console.error(`Error fetching resources for ${provider} account ${accountId}:`, err);
      
      toast({
        title: 'Error',
        description: `Failed to fetch resource data: ${err.message || 'Unknown error'}`,
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setLoadingResources(prev => ({ ...prev, [key]: false }));
    }
  };

  const getProviderIcon = (provider: string) => {
    switch (provider) {
      case 'aws':
        return <FaAws size="24px" color="#FF9900" />;
      case 'azure':
        return <FaMicrosoft size="24px" color="#0078D4" />;
      case 'gcp':
        return <FaGoogle size="24px" color="#4285F4" />;
      default:
        return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'active':
        return 'green';
      case 'inactive':
        return 'red';
      case 'pending':
        return 'yellow';
      default:
        return 'gray';
    }
  };

  if (loading) {
    return (
      <Box textAlign="center" py={10}>
        <Spinner size="xl" color="cyan.400" />
        <Text mt={4} color="gray.300">Loading cloud accounts...</Text>
      </Box>
    );
  }

  if (error) {
    return (
      <Box textAlign="center" py={10} color="red.400">
        <Text>Error: {error}</Text>
        <Button mt={4} onClick={fetchAccounts} colorScheme="cyan">
          Retry
        </Button>
      </Box>
    );
  }

  const hasAccounts = Object.keys(accounts).some(provider => accounts[provider]?.length > 0);

  if (!hasAccounts) {
    return (
      <Box textAlign="center" py={10} bg="gray.800" borderRadius="md" p={6}>
        <Text color="gray.300">No cloud accounts found. Add your first account to get started.</Text>
      </Box>
    );
  }

  return (
    <VStack spacing={6} align="stretch">
      {Object.keys(accounts).map(provider => (
        accounts[provider]?.length > 0 && (
          <Box key={provider}>
            <Heading size="md" mb={4} color="cyan.400" display="flex" alignItems="center">
              {getProviderIcon(provider)}
              <Text ml={2}>{provider.toUpperCase()} Accounts</Text>
            </Heading>
            
            <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
              {accounts[provider].map((account: any) => {
                const accountKey = `${provider}-${account.id}`;
                const accountCosts = costs[accountKey];
                const accountResources = resources[accountKey];
                
                return (
                  <Card 
                    key={account.id} 
                    bg="gray.800" 
                    borderColor="gray.700" 
                    borderWidth="1px"
                    _hover={{ 
                      borderColor: "cyan.400",
                      transform: "translateY(-2px)",
                      transition: "all 0.2s ease-in-out"
                    }}
                    transition="all 0.2s ease-in-out"
                  >
                    <CardHeader>
                      <Flex justify="space-between" align="center">
                        <Heading size="sm" color="white">{account.name}</Heading>
                        <Badge colorScheme={getStatusColor(account.status)}>
                          {account.status}
                        </Badge>
                      </Flex>
                    </CardHeader>
                    
                    <CardBody>
                      <VStack align="start" spacing={2}>
                        {provider === 'aws' && (
                          <>
                            <Text color="gray.300">Account ID: {account.account_id}</Text>
                            <Text color="gray.300">Regions: {account.regions?.join(', ')}</Text>
                          </>
                        )}
                        
                        {provider === 'azure' && (
                          <Text color="gray.300">Subscription ID: {account.subscription_id}</Text>
                        )}
                        
                        {provider === 'gcp' && (
                          <Text color="gray.300">Project ID: {account.project_id}</Text>
                        )}
                        
                        <Divider my={2} borderColor="gray.600" />
                        
                        {/* Cost Information */}
                        <Box w="100%">
                          <Flex justify="space-between" align="center" mb={2}>
                            <Text color="gray.300">Cost Data:</Text>
                            <Tooltip label="Refresh Cost Data">
                              <IconButton
                                aria-label="Refresh costs"
                                icon={<RepeatIcon />}
                                size="sm"
                                colorScheme="cyan"
                                isLoading={loadingCosts[accountKey]}
                                onClick={() => fetchCosts(provider, account.id)}
                              />
                            </Tooltip>
                          </Flex>
                          
                          {accountCosts ? (
                            <VStack align="start" spacing={1}>
                              <Text color="white" fontWeight="bold">
                                Total: ${accountCosts.total_cost?.toFixed(2)} {accountCosts.currency}
                              </Text>
                              <Text color="gray.400" fontSize="sm">
                                Period: {accountCosts.time_period?.start} to {accountCosts.time_period?.end}
                              </Text>
                              {accountCosts.services && accountCosts.services.length > 0 && (
                                <Box mt={2} w="100%">
                                  <Text color="gray.300" fontSize="sm">Top Services:</Text>
                                  {accountCosts.services.slice(0, 3).map((service: any, idx: number) => (
                                    <Flex key={idx} justify="space-between" fontSize="sm">
                                      <Text color="gray.400">{service.name}</Text>
                                      <Text color="cyan.300">${service.cost.toFixed(2)}</Text>
                                    </Flex>
                                  ))}
                                </Box>
                              )}
                            </VStack>
                          ) : (
                            <Text color="gray.400" fontSize="sm">
                              {loadingCosts[accountKey] ? 'Loading cost data...' : 'Click refresh to load cost data'}
                            </Text>
                          )}
                        </Box>
                        
                        {/* Resource Information for AWS */}
                        {provider === 'aws' && (
                          <Box w="100%" mt={2}>
                            <Flex justify="space-between" align="center" mb={2}>
                              <Text color="gray.300">Resources:</Text>
                              <Tooltip label="Fetch Resources">
                                <IconButton
                                  aria-label="Fetch resources"
                                  icon={<RepeatIcon />}
                                  size="sm"
                                  colorScheme="cyan"
                                  isLoading={loadingResources[accountKey]}
                                  onClick={() => fetchResources(provider, account.id)}
                                />
                              </Tooltip>
                            </Flex>
                            
                            {accountResources ? (
                              <VStack align="start" spacing={1}>
                                <Flex justify="space-between" w="100%" fontSize="sm">
                                  <Text color="gray.400">EC2 Instances:</Text>
                                  <Text color="cyan.300">{accountResources.ec2_instances?.length || 0}</Text>
                                </Flex>
                                <Flex justify="space-between" w="100%" fontSize="sm">
                                  <Text color="gray.400">S3 Buckets:</Text>
                                  <Text color="cyan.300">{accountResources.s3_buckets?.length || 0}</Text>
                                </Flex>
                                <Flex justify="space-between" w="100%" fontSize="sm">
                                  <Text color="gray.400">RDS Instances:</Text>
                                  <Text color="cyan.300">{accountResources.rds_instances?.length || 0}</Text>
                                </Flex>
                              </VStack>
                            ) : (
                              <Text color="gray.400" fontSize="sm">
                                {loadingResources[accountKey] ? 'Loading resources...' : 'Click refresh to load resources'}
                              </Text>
                            )}
                          </Box>
                        )}
                      </VStack>
                    </CardBody>
                    
                    <CardFooter>
                      <HStack spacing={2} justify="space-between" w="100%">
                        <Button
                          leftIcon={<ViewIcon />}
                          colorScheme="cyan"
                          size="sm"
                          variant="outline"
                          onClick={() => onViewAccount && onViewAccount(account)}
                        >
                          View Details
                        </Button>
                        
                        <IconButton
                          aria-label="Delete account"
                          icon={<DeleteIcon />}
                          colorScheme="red"
                          size="sm"
                          variant="ghost"
                          onClick={() => handleDelete(provider, account.id, account.name)}
                        />
                      </HStack>
                    </CardFooter>
                  </Card>
                );
              })}
            </SimpleGrid>
          </Box>
        )
      ))}
    </VStack>
  );
};

export default CloudAccountsList;

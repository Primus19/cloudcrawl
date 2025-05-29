/**
 * Cloud Account Form Component
 * Form for adding and editing cloud provider accounts
 */

import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  Select,
  Stack,
  Heading,
  Text,
  useToast,
  VStack,
  HStack,
  Checkbox,
  CheckboxGroup,
  Divider,
  Card,
  CardBody,
  CardHeader,
  IconButton
} from '@chakra-ui/react';
import { AddIcon, CloseIcon } from '@chakra-ui/icons';
import { addAWSAccount, addAzureAccount, addGCPAccount } from '../../services/cloudAccounts';

// AWS Regions
const AWS_REGIONS = [
  'us-east-1',
  'us-east-2',
  'us-west-1',
  'us-west-2',
  'ca-central-1',
  'eu-west-1',
  'eu-west-2',
  'eu-west-3',
  'eu-central-1',
  'ap-northeast-1',
  'ap-northeast-2',
  'ap-southeast-1',
  'ap-southeast-2',
  'ap-south-1',
  'sa-east-1'
];

interface CloudAccountFormProps {
  onSuccess: () => void;
}

const CloudAccountForm: React.FC<CloudAccountFormProps> = ({ onSuccess }) => {
  const [provider, setProvider] = useState('aws');
  const [name, setName] = useState('');
  const [accountId, setAccountId] = useState('');
  const [accessKey, setAccessKey] = useState('');
  const [secretKey, setSecretKey] = useState('');
  const [regions, setRegions] = useState<string[]>(['us-east-1']);
  const [subscriptionId, setSubscriptionId] = useState('');
  const [tenantId, setTenantId] = useState('');
  const [projectId, setProjectId] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');
  
  const toast = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);
    setError('');
    
    try {
      if (provider === 'aws') {
        if (!name || !accountId || !accessKey || !secretKey || regions.length === 0) {
          throw new Error('Please fill in all required fields');
        }
        
        await addAWSAccount({
          name,
          account_id: accountId,
          access_key: accessKey,
          secret_key: secretKey,
          regions
        });
      } else if (provider === 'azure') {
        if (!name || !subscriptionId || !tenantId) {
          throw new Error('Please fill in all required fields');
        }
        
        await addAzureAccount({
          name,
          subscription_id: subscriptionId,
          tenant_id: tenantId
        });
      } else if (provider === 'gcp') {
        if (!name || !projectId) {
          throw new Error('Please fill in all required fields');
        }
        
        await addGCPAccount({
          name,
          project_id: projectId
        });
      }
      
      toast({
        title: 'Account added',
        description: `${provider.toUpperCase()} account "${name}" has been added successfully.`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
      
      // Reset form
      setName('');
      setAccountId('');
      setAccessKey('');
      setSecretKey('');
      setRegions(['us-east-1']);
      setSubscriptionId('');
      setTenantId('');
      setProjectId('');
      
      // Notify parent component
      onSuccess();
    } catch (err: any) {
      console.error('Error adding cloud account:', err);
      setError(err.message || 'An error occurred while adding the account');
      
      toast({
        title: 'Error',
        description: err.message || 'An error occurred while adding the account',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleRegionChange = (region: string) => {
    if (regions.includes(region)) {
      setRegions(regions.filter(r => r !== region));
    } else {
      setRegions([...regions, region]);
    }
  };

  return (
    <Card variant="elevated" bg="gray.800" borderColor="gray.700" borderWidth="1px">
      <CardHeader>
        <Heading size="md" color="cyan.400">Add Cloud Account</Heading>
      </CardHeader>
      <CardBody>
        <Box as="form" onSubmit={handleSubmit}>
          <VStack spacing={4} align="stretch">
            <FormControl isRequired>
              <FormLabel>Cloud Provider</FormLabel>
              <Select 
                value={provider} 
                onChange={(e) => setProvider(e.target.value)}
                bg="gray.700"
                borderColor="gray.600"
                _hover={{ borderColor: "cyan.400" }}
                color="white"
              >
                <option value="aws">AWS</option>
                <option value="azure">Azure</option>
                <option value="gcp">Google Cloud</option>
              </Select>
            </FormControl>
            
            <FormControl isRequired>
              <FormLabel>Account Name</FormLabel>
              <Input 
                value={name} 
                onChange={(e) => setName(e.target.value)} 
                placeholder="e.g., Production AWS Account"
                bg="gray.700"
                borderColor="gray.600"
                _hover={{ borderColor: "cyan.400" }}
                color="white"
              />
            </FormControl>
            
            {provider === 'aws' && (
              <>
                <FormControl isRequired>
                  <FormLabel>AWS Account ID</FormLabel>
                  <Input 
                    value={accountId} 
                    onChange={(e) => setAccountId(e.target.value)} 
                    placeholder="e.g., 123456789012"
                    bg="gray.700"
                    borderColor="gray.600"
                    _hover={{ borderColor: "cyan.400" }}
                    color="white"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Access Key</FormLabel>
                  <Input 
                    value={accessKey} 
                    onChange={(e) => setAccessKey(e.target.value)} 
                    placeholder="e.g., AKIAIOSFODNN7EXAMPLE"
                    bg="gray.700"
                    borderColor="gray.600"
                    _hover={{ borderColor: "cyan.400" }}
                    color="white"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Secret Key</FormLabel>
                  <Input 
                    type="password" 
                    value={secretKey} 
                    onChange={(e) => setSecretKey(e.target.value)} 
                    placeholder="Your AWS Secret Key"
                    bg="gray.700"
                    borderColor="gray.600"
                    _hover={{ borderColor: "cyan.400" }}
                    color="white"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Regions</FormLabel>
                  <Box 
                    maxH="200px" 
                    overflowY="auto" 
                    p={2} 
                    borderWidth="1px" 
                    borderRadius="md"
                    borderColor="gray.600"
                    bg="gray.700"
                  >
                    <CheckboxGroup colorScheme="cyan" defaultValue={regions}>
                      <VStack align="start" spacing={2}>
                        {AWS_REGIONS.map((region) => (
                          <Checkbox 
                            key={region} 
                            value={region} 
                            isChecked={regions.includes(region)}
                            onChange={() => handleRegionChange(region)}
                            color="white"
                          >
                            {region}
                          </Checkbox>
                        ))}
                      </VStack>
                    </CheckboxGroup>
                  </Box>
                </FormControl>
              </>
            )}
            
            {provider === 'azure' && (
              <>
                <FormControl isRequired>
                  <FormLabel>Subscription ID</FormLabel>
                  <Input 
                    value={subscriptionId} 
                    onChange={(e) => setSubscriptionId(e.target.value)} 
                    placeholder="e.g., aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
                    bg="gray.700"
                    borderColor="gray.600"
                    _hover={{ borderColor: "cyan.400" }}
                    color="white"
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel>Tenant ID</FormLabel>
                  <Input 
                    value={tenantId} 
                    onChange={(e) => setTenantId(e.target.value)} 
                    placeholder="e.g., aaaaaaaa-bbbb-cccc-dddd-eeeeeeeeeeee"
                    bg="gray.700"
                    borderColor="gray.600"
                    _hover={{ borderColor: "cyan.400" }}
                    color="white"
                  />
                </FormControl>
              </>
            )}
            
            {provider === 'gcp' && (
              <FormControl isRequired>
                <FormLabel>Project ID</FormLabel>
                <Input 
                  value={projectId} 
                  onChange={(e) => setProjectId(e.target.value)} 
                  placeholder="e.g., my-gcp-project-123"
                  bg="gray.700"
                  borderColor="gray.600"
                  _hover={{ borderColor: "cyan.400" }}
                  color="white"
                />
              </FormControl>
            )}
            
            {error && (
              <Text color="red.400" fontSize="sm">
                {error}
              </Text>
            )}
            
            <Button 
              type="submit" 
              colorScheme="cyan" 
              isLoading={isLoading}
              leftIcon={<AddIcon />}
              _hover={{ bg: "cyan.500" }}
            >
              Add Account
            </Button>
          </VStack>
        </Box>
      </CardBody>
    </Card>
  );
};

export default CloudAccountForm;

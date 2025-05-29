/**
 * Terraform Page
 * Displays and manages Terraform configurations
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
  SimpleGrid,
  Card,
  CardBody,
  CardHeader,
  Divider,
  VStack,
  HStack,
  Badge,
  Icon,
  Flex,
  Button,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Code,
  useColorModeValue
} from '@chakra-ui/react';
import { FiCode, FiPlay, FiDownload, FiPlus, FiGitPull } from 'react-icons/fi';

const TerraformPage: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Terraform Management</Heading>
          <Text color="gray.300">
            Generate, manage, and deploy infrastructure as code
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Flex justify="flex-end">
          <HStack spacing={3}>
            <Button colorScheme="cyan" leftIcon={<FiPlus />}>
              New Configuration
            </Button>
            <Button colorScheme="cyan" variant="outline" leftIcon={<FiGitPull />}>
              Import Existing
            </Button>
          </HStack>
        </Flex>
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Configurations</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Deployments</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Templates</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <HStack>
                    <Icon as={FiCode} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Terraform Configurations</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Name</Th>
                          <Th color="gray.400">Resources</Th>
                          <Th color="gray.400">Provider</Th>
                          <Th color="gray.400">Last Modified</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">production-vpc</Td>
                          <Td color="white">15</Td>
                          <Td color="white">AWS</Td>
                          <Td color="gray.300">2025-05-25</Td>
                          <Td><Badge colorScheme="green">Applied</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan">Edit</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                              <Button size="xs" colorScheme="green" leftIcon={<FiPlay />}>Apply</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">dev-environment</Td>
                          <Td color="white">23</Td>
                          <Td color="white">AWS</Td>
                          <Td color="gray.300">2025-05-27</Td>
                          <Td><Badge colorScheme="yellow">Modified</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan">Edit</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                              <Button size="xs" colorScheme="green" leftIcon={<FiPlay />}>Apply</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">database-cluster</Td>
                          <Td color="white">8</Td>
                          <Td color="white">AWS</Td>
                          <Td color="gray.300">2025-05-20</Td>
                          <Td><Badge colorScheme="green">Applied</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan">Edit</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                              <Button size="xs" colorScheme="green" leftIcon={<FiPlay />}>Apply</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">azure-resources</Td>
                          <Td color="white">12</Td>
                          <Td color="white">Azure</Td>
                          <Td color="gray.300">2025-05-15</Td>
                          <Td><Badge colorScheme="red">Drift Detected</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan">Edit</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                              <Button size="xs" colorScheme="green" leftIcon={<FiPlay />}>Apply</Button>
                            </HStack>
                          </Td>
                        </Tr>
                      </Tbody>
                    </Table>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <HStack>
                    <Icon as={FiPlay} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Deployment History</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Configuration</Th>
                          <Th color="gray.400">Version</Th>
                          <Th color="gray.400">Deployed By</Th>
                          <Th color="gray.400">Timestamp</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">dev-environment</Td>
                          <Td color="white">v1.3.0</Td>
                          <Td color="white">admin</Td>
                          <Td color="gray.300">2025-05-27 14:32</Td>
                          <Td><Badge colorScheme="green">Success</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Logs</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Rollback</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">production-vpc</Td>
                          <Td color="white">v2.1.0</Td>
                          <Td color="white">admin</Td>
                          <Td color="gray.300">2025-05-25 09:15</Td>
                          <Td><Badge colorScheme="green">Success</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Logs</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Rollback</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">database-cluster</Td>
                          <Td color="white">v1.0.2</Td>
                          <Td color="white">admin</Td>
                          <Td color="gray.300">2025-05-20 11:45</Td>
                          <Td><Badge colorScheme="green">Success</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Logs</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Rollback</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">dev-environment</Td>
                          <Td color="white">v1.2.0</Td>
                          <Td color="white">admin</Td>
                          <Td color="gray.300">2025-05-18 16:20</Td>
                          <Td><Badge colorScheme="red">Failed</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Logs</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Rollback</Button>
                            </HStack>
                          </Td>
                        </Tr>
                      </Tbody>
                    </Table>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">AWS VPC</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Complete VPC setup with public and private subnets, NAT gateways, and security groups.
                      </Text>
                      <HStack>
                        <Badge colorScheme="orange">AWS</Badge>
                        <Badge colorScheme="blue">Networking</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  version = "3.14.0"
  
  name = "main-vpc"
  cidr = "10.0.0.0/16"
  
  azs = ["us-east-1a", "us-east-1b"]
  # ...more config
}`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
                
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">EKS Cluster</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Production-ready Kubernetes cluster with node groups and IAM roles.
                      </Text>
                      <HStack>
                        <Badge colorScheme="orange">AWS</Badge>
                        <Badge colorScheme="purple">Containers</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`module "eks" {
  source = "terraform-aws-modules/eks/aws"
  version = "18.20.0"
  
  cluster_name = "main-cluster"
  cluster_version = "1.23"
  
  vpc_id = module.vpc.vpc_id
  # ...more config
}`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
                
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">RDS Database</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Secure PostgreSQL database with backups, encryption, and monitoring.
                      </Text>
                      <HStack>
                        <Badge colorScheme="orange">AWS</Badge>
                        <Badge colorScheme="green">Database</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`module "db" {
  source = "terraform-aws-modules/rds/aws"
  version = "4.2.0"
  
  identifier = "main-db"
  engine = "postgres"
  engine_version = "14.3"
  
  # ...more config
}`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
                
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">Azure Virtual Network</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Complete Azure networking setup with subnets, NSGs, and routing.
                      </Text>
                      <HStack>
                        <Badge colorScheme="blue">Azure</Badge>
                        <Badge colorScheme="blue">Networking</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`module "vnet" {
  source = "Azure/vnet/azurerm"
  version = "3.0.0"
  
  resource_group_name = "main-rg"
  vnet_name = "main-vnet"
  address_space = ["10.0.0.0/16"]
  
  # ...more config
}`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
                
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">GCP Kubernetes Engine</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Production-ready GKE cluster with node pools and IAM configuration.
                      </Text>
                      <HStack>
                        <Badge colorScheme="green">GCP</Badge>
                        <Badge colorScheme="purple">Containers</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`module "gke" {
  source = "terraform-google-modules/kubernetes-engine/google"
  version = "23.0.0"
  
  project_id = "my-project"
  name = "main-cluster"
  region = "us-central1"
  
  # ...more config
}`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
                
                <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                  <CardHeader>
                    <Heading size="md" color="white">Multi-Cloud Setup</Heading>
                  </CardHeader>
                  <CardBody>
                    <VStack align="start" spacing={3}>
                      <Text color="gray.300" fontSize="sm">
                        Complete infrastructure setup across AWS, Azure, and GCP with networking and security.
                      </Text>
                      <HStack>
                        <Badge colorScheme="orange">AWS</Badge>
                        <Badge colorScheme="blue">Azure</Badge>
                        <Badge colorScheme="green">GCP</Badge>
                      </HStack>
                      <Box 
                        bg="gray.800" 
                        p={3} 
                        borderRadius="md" 
                        w="100%" 
                        maxH="100px" 
                        overflow="auto"
                      >
                        <Code 
                          display="block" 
                          whiteSpace="pre" 
                          children={`# AWS Provider
provider "aws" {
  region = "us-east-1"
}

# Azure Provider
provider "azurerm" {
  features {}
}

# GCP Provider
provider "google" {
  project = "my-project"
  region = "us-central1"
}

# ...more config`}
                          bg="transparent"
                          color="cyan.300"
                        />
                      </Box>
                      <Button 
                        colorScheme="cyan" 
                        leftIcon={<FiDownload />}
                        alignSelf="flex-end"
                      >
                        Use Template
                      </Button>
                    </VStack>
                  </CardBody>
                </Card>
              </SimpleGrid>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
};

export default TerraformPage;

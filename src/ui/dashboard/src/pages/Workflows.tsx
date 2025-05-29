/**
 * Workflows Page
 * Displays automated workflows and pipelines
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
  Progress
} from '@chakra-ui/react';
import { FiActivity, FiPlay, FiPause, FiEdit } from 'react-icons/fi';

const Workflows: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Workflows</Heading>
          <Text color="gray.300">
            Manage automated workflows and pipelines
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Flex justify="flex-end">
          <Button colorScheme="cyan" leftIcon={<FiEdit />}>
            Create Workflow
          </Button>
        </Flex>
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Active Workflows</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Completed Workflows</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Templates</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <HStack>
                    <Icon as={FiActivity} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Active Workflows</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Workflow Name</Th>
                          <Th color="gray.400">Type</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Progress</Th>
                          <Th color="gray.400">Started</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">Monthly Cost Optimization</Td>
                          <Td color="white">Cost Management</Td>
                          <Td><Badge colorScheme="green">Running</Badge></Td>
                          <Td>
                            <Progress value={75} size="sm" colorScheme="cyan" />
                          </Td>
                          <Td color="gray.300">2025-05-28 09:15</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="red" leftIcon={<FiPause />}>Pause</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Security Compliance Check</Td>
                          <Td color="white">Security</Td>
                          <Td><Badge colorScheme="green">Running</Badge></Td>
                          <Td>
                            <Progress value={45} size="sm" colorScheme="cyan" />
                          </Td>
                          <Td color="gray.300">2025-05-29 00:00</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="red" leftIcon={<FiPause />}>Pause</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Resource Tagging Audit</Td>
                          <Td color="white">Governance</Td>
                          <Td><Badge colorScheme="yellow">Paused</Badge></Td>
                          <Td>
                            <Progress value={30} size="sm" colorScheme="yellow" />
                          </Td>
                          <Td color="gray.300">2025-05-27 14:30</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="green" leftIcon={<FiPlay />}>Resume</Button>
                              <Button size="xs" colorScheme="cyan" variant="outline">View</Button>
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
                    <Icon as={FiActivity} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Completed Workflows</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Workflow Name</Th>
                          <Th color="gray.400">Type</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Duration</Th>
                          <Th color="gray.400">Completed</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">Weekly Resource Cleanup</Td>
                          <Td color="white">Maintenance</Td>
                          <Td><Badge colorScheme="green">Completed</Badge></Td>
                          <Td color="white">45 minutes</Td>
                          <Td color="gray.300">2025-05-26 03:15</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Results</Button>
                              <Button size="xs" colorScheme="green">Run Again</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">IAM Access Review</Td>
                          <Td color="white">Security</Td>
                          <Td><Badge colorScheme="green">Completed</Badge></Td>
                          <Td color="white">1 hour 12 minutes</Td>
                          <Td color="gray.300">2025-05-25 15:30</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="cyan" variant="outline">View Results</Button>
                              <Button size="xs" colorScheme="green">Run Again</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Cost Anomaly Detection</Td>
                          <Td color="white">Cost Management</Td>
                          <Td><Badge colorScheme="red">Failed</Badge></Td>
                          <Td color="white">8 minutes</Td>
                          <Td color="gray.300">2025-05-24 09:45</Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="red" variant="outline">View Error</Button>
                              <Button size="xs" colorScheme="green">Retry</Button>
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
                    <Icon as={FiActivity} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Workflow Templates</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} spacing={4}>
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Cost Optimization</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Identifies cost-saving opportunities and implements approved recommendations.
                          </Text>
                          <HStack>
                            <Badge colorScheme="green">Cost</Badge>
                            <Badge colorScheme="blue">Automated</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Use Template
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                    
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Security Compliance</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Scans resources for security vulnerabilities and compliance issues.
                          </Text>
                          <HStack>
                            <Badge colorScheme="red">Security</Badge>
                            <Badge colorScheme="blue">Automated</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Use Template
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                    
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Resource Cleanup</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Identifies and removes unused resources to reduce costs.
                          </Text>
                          <HStack>
                            <Badge colorScheme="green">Cost</Badge>
                            <Badge colorScheme="purple">Maintenance</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Use Template
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                    
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Tagging Compliance</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Enforces tagging policies across all cloud resources.
                          </Text>
                          <HStack>
                            <Badge colorScheme="orange">Governance</Badge>
                            <Badge colorScheme="blue">Automated</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Use Template
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                    
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Backup Verification</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Verifies that all critical resources have proper backups.
                          </Text>
                          <HStack>
                            <Badge colorScheme="red">Security</Badge>
                            <Badge colorScheme="yellow">DR</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Use Template
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                    
                    <Card bg="gray.700" borderColor="gray.600" borderWidth="1px">
                      <CardBody>
                        <VStack align="start" spacing={3}>
                          <Heading size="sm" color="white">Custom Workflow</Heading>
                          <Text color="gray.300" fontSize="sm">
                            Create a custom workflow from scratch with your own steps.
                          </Text>
                          <HStack>
                            <Badge colorScheme="gray">Custom</Badge>
                          </HStack>
                          <Button size="sm" colorScheme="cyan" alignSelf="flex-end">
                            Create Custom
                          </Button>
                        </VStack>
                      </CardBody>
                    </Card>
                  </SimpleGrid>
                </CardBody>
              </Card>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
};

export default Workflows;

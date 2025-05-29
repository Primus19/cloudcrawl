/**
 * Actions Page
 * Displays automated actions and tasks
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
  Td
} from '@chakra-ui/react';
import { FiActivity, FiClock, FiCheckCircle, FiAlertCircle } from 'react-icons/fi';

const Actions: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Actions</Heading>
          <Text color="gray.300">
            View and manage automated actions and tasks
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Pending Actions</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Completed Actions</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Scheduled Tasks</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <HStack>
                    <Icon as={FiActivity} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Pending Actions</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Action</Th>
                          <Th color="gray.400">Resource</Th>
                          <Th color="gray.400">Type</Th>
                          <Th color="gray.400">Estimated Savings</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">Resize EC2 Instance</Td>
                          <Td color="white">i-0123456789abcdef0</Td>
                          <Td color="white">Cost Optimization</Td>
                          <Td color="cyan.300">$45/month</Td>
                          <Td><Badge colorScheme="yellow">Pending Approval</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="green">Approve</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Reject</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Delete Unused EBS Volume</Td>
                          <Td color="white">vol-0123456789abcdef1</Td>
                          <Td color="white">Cost Optimization</Td>
                          <Td color="cyan.300">$12/month</Td>
                          <Td><Badge colorScheme="yellow">Pending Approval</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="green">Approve</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Reject</Button>
                            </HStack>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Update Security Group</Td>
                          <Td color="white">sg-0123456789abcdef2</Td>
                          <Td color="white">Security</Td>
                          <Td color="cyan.300">N/A</Td>
                          <Td><Badge colorScheme="yellow">Pending Approval</Badge></Td>
                          <Td>
                            <HStack spacing={2}>
                              <Button size="xs" colorScheme="green">Approve</Button>
                              <Button size="xs" colorScheme="red" variant="outline">Reject</Button>
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
                    <Icon as={FiCheckCircle} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Completed Actions</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Action</Th>
                          <Th color="gray.400">Resource</Th>
                          <Th color="gray.400">Type</Th>
                          <Th color="gray.400">Savings</Th>
                          <Th color="gray.400">Status</Th>
                          <Th color="gray.400">Completed</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">Resize RDS Instance</Td>
                          <Td color="white">db-prod-replica</Td>
                          <Td color="white">Cost Optimization</Td>
                          <Td color="cyan.300">$78/month</Td>
                          <Td><Badge colorScheme="green">Completed</Badge></Td>
                          <Td color="gray.300">2025-05-28</Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Enable S3 Bucket Encryption</Td>
                          <Td color="white">app-backups-prod</Td>
                          <Td color="white">Security</Td>
                          <Td color="cyan.300">N/A</Td>
                          <Td><Badge colorScheme="green">Completed</Badge></Td>
                          <Td color="gray.300">2025-05-27</Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Purchase Reserved Instances</Td>
                          <Td color="white">Multiple</Td>
                          <Td color="white">Cost Optimization</Td>
                          <Td color="cyan.300">$1,245/month</Td>
                          <Td><Badge colorScheme="green">Completed</Badge></Td>
                          <Td color="gray.300">2025-05-25</Td>
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
                    <Icon as={FiClock} color="cyan.400" boxSize={5} />
                    <Heading size="md" color="white">Scheduled Tasks</Heading>
                  </HStack>
                </CardHeader>
                <CardBody>
                  <Box overflowX="auto">
                    <Table variant="simple" size="sm">
                      <Thead>
                        <Tr>
                          <Th color="gray.400">Task</Th>
                          <Th color="gray.400">Description</Th>
                          <Th color="gray.400">Type</Th>
                          <Th color="gray.400">Schedule</Th>
                          <Th color="gray.400">Next Run</Th>
                          <Th color="gray.400">Actions</Th>
                        </Tr>
                      </Thead>
                      <Tbody>
                        <Tr>
                          <Td color="white">Cost Report Generation</Td>
                          <Td color="white">Generate monthly cost reports</Td>
                          <Td color="white">Reporting</Td>
                          <Td color="white">Monthly</Td>
                          <Td color="gray.300">2025-06-01</Td>
                          <Td>
                            <Button size="xs" colorScheme="cyan">Run Now</Button>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Resource Cleanup</Td>
                          <Td color="white">Identify and flag unused resources</Td>
                          <Td color="white">Maintenance</Td>
                          <Td color="white">Weekly</Td>
                          <Td color="gray.300">2025-06-02</Td>
                          <Td>
                            <Button size="xs" colorScheme="cyan">Run Now</Button>
                          </Td>
                        </Tr>
                        <Tr>
                          <Td color="white">Security Scan</Td>
                          <Td color="white">Scan for security vulnerabilities</Td>
                          <Td color="white">Security</Td>
                          <Td color="white">Daily</Td>
                          <Td color="gray.300">2025-05-30</Td>
                          <Td>
                            <Button size="xs" colorScheme="cyan">Run Now</Button>
                          </Td>
                        </Tr>
                      </Tbody>
                    </Table>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
};

export default Actions;

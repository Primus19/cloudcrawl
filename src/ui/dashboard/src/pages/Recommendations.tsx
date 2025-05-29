/**
 * Recommendations Page
 * Displays cost optimization and security recommendations
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
  Progress
} from '@chakra-ui/react';
import { FiDollarSign, FiShield, FiZap, FiCheck } from 'react-icons/fi';

const Recommendations: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Recommendations</Heading>
          <Text color="gray.300">
            Cost optimization and security recommendations for your cloud resources
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Cost Optimization</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Security</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Performance</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <SimpleGrid columns={{ base: 1, lg: 1 }} spacing={6}>
                {/* Cost Optimization Recommendations */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiDollarSign} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">Cost Optimization Recommendations</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Rightsizing EC2 Instances</Text>
                          </HStack>
                          <Badge colorScheme="green">$1,245/mo</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          8 instances are oversized based on CPU/memory utilization. Consider downsizing to save costs.
                        </Text>
                        <Progress value={75} colorScheme="cyan" size="sm" mb={3} />
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Estimated savings: $1,245/month</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Unused EBS Volumes</Text>
                          </HStack>
                          <Badge colorScheme="green">$450/mo</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          12 unattached volumes detected across all regions. Consider deleting them to save costs.
                        </Text>
                        <Progress value={60} colorScheme="cyan" size="sm" mb={3} />
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Estimated savings: $450/month</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Reserved Instance Coverage</Text>
                          </HStack>
                          <Badge colorScheme="green">$3,200/mo</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          Increase RI coverage from 45% to 75% for optimal savings. Consider purchasing RIs for stable workloads.
                        </Text>
                        <Progress value={45} colorScheme="cyan" size="sm" mb={3} />
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Estimated savings: $3,200/month</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Idle Load Balancers</Text>
                          </HStack>
                          <Badge colorScheme="green">$180/mo</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          3 load balancers with minimal traffic detected. Consider removing them if not needed.
                        </Text>
                        <Progress value={30} colorScheme="cyan" size="sm" mb={3} />
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Estimated savings: $180/month</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                    </VStack>
                  </CardBody>
                </Card>
              </SimpleGrid>
            </TabPanel>
            
            <TabPanel p={0}>
              <SimpleGrid columns={{ base: 1, lg: 1 }} spacing={6}>
                {/* Security Recommendations */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiShield} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">Security Recommendations</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Public S3 Buckets</Text>
                          </HStack>
                          <Badge colorScheme="red">High Risk</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          3 buckets with public read access detected. Restrict access to prevent data exposure.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 3 S3 buckets</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Security Groups</Text>
                          </HStack>
                          <Badge colorScheme="orange">Medium Risk</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          5 security groups with overly permissive rules (0.0.0.0/0). Restrict to specific IP ranges.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 5 security groups</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">IAM Access Keys</Text>
                          </HStack>
                          <Badge colorScheme="yellow">Low Risk</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          2 access keys older than 90 days need rotation. Rotate regularly to enhance security.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 2 IAM users</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">Unencrypted EBS Volumes</Text>
                          </HStack>
                          <Badge colorScheme="orange">Medium Risk</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          8 EBS volumes are not encrypted. Enable encryption to protect sensitive data.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 8 EBS volumes</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                    </VStack>
                  </CardBody>
                </Card>
              </SimpleGrid>
            </TabPanel>
            
            <TabPanel p={0}>
              <SimpleGrid columns={{ base: 1, lg: 1 }} spacing={6}>
                {/* Performance Recommendations */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiZap} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">Performance Recommendations</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <VStack spacing={4} align="stretch">
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">RDS Performance Insights</Text>
                          </HStack>
                          <Badge colorScheme="blue">Performance</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          Enable Performance Insights on 2 RDS instances to monitor and optimize database performance.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 2 RDS instances</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">EC2 Instance Types</Text>
                          </HStack>
                          <Badge colorScheme="blue">Performance</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          3 instances could benefit from newer generation instance types with better performance.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 3 EC2 instances</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
                      
                      <Box p={4} bg="gray.700" borderRadius="md">
                        <Flex justify="space-between" align="center" mb={2}>
                          <HStack>
                            <Text fontWeight="medium" color="white">EBS Volume Types</Text>
                          </HStack>
                          <Badge colorScheme="blue">Performance</Badge>
                        </Flex>
                        <Text color="gray.300" fontSize="sm" mb={3}>
                          5 volumes could benefit from upgrading from gp2 to gp3 for better performance and cost.
                        </Text>
                        <Flex justify="space-between">
                          <Text color="gray.400" fontSize="sm">Affected resources: 5 EBS volumes</Text>
                          <Button size="sm" colorScheme="cyan">View Details</Button>
                        </Flex>
                      </Box>
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

export default Recommendations;

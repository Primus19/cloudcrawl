/**
 * Dashboard Page
 * Main dashboard with overview of cloud resources and costs
 */

import React from 'react';
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Text,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow,
  Card,
  CardBody,
  CardHeader,
  Flex,
  Icon,
  Divider,
  VStack,
  HStack,
  Progress,
  Badge
} from '@chakra-ui/react';
import { FiDollarSign, FiServer, FiDatabase, FiCloud, FiAlertTriangle } from 'react-icons/fi';

const Dashboard: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Dashboard</Heading>
          <Text color="gray.300">
            Overview of your cloud resources, costs, and optimization opportunities
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        {/* Cost Summary Cards */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Flex align="center">
                <Box p={2} bg="cyan.900" borderRadius="md" mr={4}>
                  <Icon as={FiDollarSign} color="cyan.400" boxSize={6} />
                </Box>
                <Stat>
                  <StatLabel color="gray.400">Monthly Cost</StatLabel>
                  <StatNumber color="white">$12,456</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    8.2% from last month
                  </StatHelpText>
                </Stat>
              </Flex>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Flex align="center">
                <Box p={2} bg="cyan.900" borderRadius="md" mr={4}>
                  <Icon as={FiServer} color="cyan.400" boxSize={6} />
                </Box>
                <Stat>
                  <StatLabel color="gray.400">EC2 Instances</StatLabel>
                  <StatNumber color="white">42</StatNumber>
                  <StatHelpText>
                    <StatArrow type="decrease" />
                    3 terminated today
                  </StatHelpText>
                </Stat>
              </Flex>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Flex align="center">
                <Box p={2} bg="cyan.900" borderRadius="md" mr={4}>
                  <Icon as={FiDatabase} color="cyan.400" boxSize={6} />
                </Box>
                <Stat>
                  <StatLabel color="gray.400">Storage (TB)</StatLabel>
                  <StatNumber color="white">156.4</StatNumber>
                  <StatHelpText>
                    <StatArrow type="increase" />
                    12.3% from last month
                  </StatHelpText>
                </Stat>
              </Flex>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Flex align="center">
                <Box p={2} bg="cyan.900" borderRadius="md" mr={4}>
                  <Icon as={FiCloud} color="cyan.400" boxSize={6} />
                </Box>
                <Stat>
                  <StatLabel color="gray.400">Cloud Accounts</StatLabel>
                  <StatNumber color="white">3</StatNumber>
                  <StatHelpText>
                    AWS, Azure, GCP
                  </StatHelpText>
                </Stat>
              </Flex>
            </CardBody>
          </Card>
        </SimpleGrid>
        
        {/* Recommendations and Alerts */}
        <SimpleGrid columns={{ base: 1, lg: 2 }} spacing={6}>
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardHeader>
              <Heading size="md" color="cyan.400">Cost Optimization Recommendations</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiServer} color="cyan.400" />
                      <Text fontWeight="medium" color="white">Rightsizing EC2 Instances</Text>
                    </HStack>
                    <Badge colorScheme="green">$1,245/mo</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    8 instances are oversized based on CPU/memory utilization
                  </Text>
                  <Progress value={75} colorScheme="cyan" size="sm" mt={2} />
                </Box>
                
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiDatabase} color="cyan.400" />
                      <Text fontWeight="medium" color="white">Unused EBS Volumes</Text>
                    </HStack>
                    <Badge colorScheme="green">$450/mo</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    12 unattached volumes detected across all regions
                  </Text>
                  <Progress value={60} colorScheme="cyan" size="sm" mt={2} />
                </Box>
                
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiCloud} color="cyan.400" />
                      <Text fontWeight="medium" color="white">Reserved Instance Coverage</Text>
                    </HStack>
                    <Badge colorScheme="green">$3,200/mo</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    Increase RI coverage from 45% to 75% for optimal savings
                  </Text>
                  <Progress value={45} colorScheme="cyan" size="sm" mt={2} />
                </Box>
              </VStack>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardHeader>
              <Heading size="md" color="cyan.400">Security Alerts</Heading>
            </CardHeader>
            <CardBody>
              <VStack spacing={4} align="stretch">
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiAlertTriangle} color="red.400" />
                      <Text fontWeight="medium" color="white">Public S3 Buckets</Text>
                    </HStack>
                    <Badge colorScheme="red">High</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    3 buckets with public read access detected
                  </Text>
                </Box>
                
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiAlertTriangle} color="orange.400" />
                      <Text fontWeight="medium" color="white">Security Groups</Text>
                    </HStack>
                    <Badge colorScheme="orange">Medium</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    5 security groups with overly permissive rules (0.0.0.0/0)
                  </Text>
                </Box>
                
                <Box p={4} bg="gray.700" borderRadius="md">
                  <Flex justify="space-between" align="center" mb={2}>
                    <HStack>
                      <Icon as={FiAlertTriangle} color="yellow.400" />
                      <Text fontWeight="medium" color="white">IAM Access Keys</Text>
                    </HStack>
                    <Badge colorScheme="yellow">Low</Badge>
                  </Flex>
                  <Text color="gray.300" fontSize="sm">
                    2 access keys older than 90 days need rotation
                  </Text>
                </Box>
              </VStack>
            </CardBody>
          </Card>
        </SimpleGrid>
      </VStack>
    </Container>
  );
};

export default Dashboard;

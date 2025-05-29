/**
 * Resources Page
 * Displays cloud resources across all accounts
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
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td
} from '@chakra-ui/react';
import { FiServer, FiDatabase, FiHardDrive, FiGlobe } from 'react-icons/fi';

const Resources: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Cloud Resources</Heading>
          <Text color="gray.300">
            View and manage resources across all your cloud providers
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>AWS</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Azure</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>GCP</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <VStack spacing={6} align="stretch">
                {/* EC2 Instances */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiServer} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">EC2 Instances</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <Box overflowX="auto">
                      <Table variant="simple" size="sm">
                        <Thead>
                          <Tr>
                            <Th color="gray.400">Instance ID</Th>
                            <Th color="gray.400">Name</Th>
                            <Th color="gray.400">Type</Th>
                            <Th color="gray.400">State</Th>
                            <Th color="gray.400">Region</Th>
                          </Tr>
                        </Thead>
                        <Tbody>
                          <Tr>
                            <Td color="white">i-0123456789abcdef0</Td>
                            <Td color="white">web-server-prod-1</Td>
                            <Td color="white">t3.large</Td>
                            <Td><Badge colorScheme="green">running</Badge></Td>
                            <Td color="white">us-east-1</Td>
                          </Tr>
                          <Tr>
                            <Td color="white">i-0123456789abcdef1</Td>
                            <Td color="white">web-server-prod-2</Td>
                            <Td color="white">t3.large</Td>
                            <Td><Badge colorScheme="green">running</Badge></Td>
                            <Td color="white">us-east-1</Td>
                          </Tr>
                          <Tr>
                            <Td color="white">i-0123456789abcdef2</Td>
                            <Td color="white">db-server-prod-1</Td>
                            <Td color="white">r5.xlarge</Td>
                            <Td><Badge colorScheme="green">running</Badge></Td>
                            <Td color="white">us-east-1</Td>
                          </Tr>
                          <Tr>
                            <Td color="white">i-0123456789abcdef3</Td>
                            <Td color="white">app-server-dev-1</Td>
                            <Td color="white">t3.medium</Td>
                            <Td><Badge colorScheme="red">stopped</Badge></Td>
                            <Td color="white">us-west-2</Td>
                          </Tr>
                        </Tbody>
                      </Table>
                    </Box>
                  </CardBody>
                </Card>
                
                {/* S3 Buckets */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiDatabase} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">S3 Buckets</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <Box overflowX="auto">
                      <Table variant="simple" size="sm">
                        <Thead>
                          <Tr>
                            <Th color="gray.400">Bucket Name</Th>
                            <Th color="gray.400">Creation Date</Th>
                            <Th color="gray.400">Region</Th>
                            <Th color="gray.400">Access</Th>
                          </Tr>
                        </Thead>
                        <Tbody>
                          <Tr>
                            <Td color="white">company-website-assets</Td>
                            <Td color="white">2023-01-15</Td>
                            <Td color="white">us-east-1</Td>
                            <Td><Badge colorScheme="yellow">public-read</Badge></Td>
                          </Tr>
                          <Tr>
                            <Td color="white">app-backups-prod</Td>
                            <Td color="white">2023-02-20</Td>
                            <Td color="white">us-east-1</Td>
                            <Td><Badge colorScheme="green">private</Badge></Td>
                          </Tr>
                          <Tr>
                            <Td color="white">data-analytics-results</Td>
                            <Td color="white">2023-03-10</Td>
                            <Td color="white">us-west-2</Td>
                            <Td><Badge colorScheme="green">private</Badge></Td>
                          </Tr>
                        </Tbody>
                      </Table>
                    </Box>
                  </CardBody>
                </Card>
                
                {/* RDS Instances */}
                <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                  <CardHeader>
                    <HStack>
                      <Icon as={FiHardDrive} color="cyan.400" boxSize={5} />
                      <Heading size="md" color="white">RDS Instances</Heading>
                    </HStack>
                  </CardHeader>
                  <CardBody>
                    <Box overflowX="auto">
                      <Table variant="simple" size="sm">
                        <Thead>
                          <Tr>
                            <Th color="gray.400">Instance ID</Th>
                            <Th color="gray.400">Engine</Th>
                            <Th color="gray.400">Class</Th>
                            <Th color="gray.400">Status</Th>
                            <Th color="gray.400">Storage (GB)</Th>
                            <Th color="gray.400">Region</Th>
                          </Tr>
                        </Thead>
                        <Tbody>
                          <Tr>
                            <Td color="white">db-prod-main</Td>
                            <Td color="white">PostgreSQL</Td>
                            <Td color="white">db.r5.large</Td>
                            <Td><Badge colorScheme="green">available</Badge></Td>
                            <Td color="white">500</Td>
                            <Td color="white">us-east-1</Td>
                          </Tr>
                          <Tr>
                            <Td color="white">db-prod-replica</Td>
                            <Td color="white">PostgreSQL</Td>
                            <Td color="white">db.r5.large</Td>
                            <Td><Badge colorScheme="green">available</Badge></Td>
                            <Td color="white">500</Td>
                            <Td color="white">us-east-1</Td>
                          </Tr>
                          <Tr>
                            <Td color="white">db-dev</Td>
                            <Td color="white">MySQL</Td>
                            <Td color="white">db.t3.medium</Td>
                            <Td><Badge colorScheme="green">available</Badge></Td>
                            <Td color="white">100</Td>
                            <Td color="white">us-west-2</Td>
                          </Tr>
                        </Tbody>
                      </Table>
                    </Box>
                  </CardBody>
                </Card>
              </VStack>
            </TabPanel>
            
            <TabPanel p={0}>
              <Box p={6} bg="gray.800" borderRadius="md" textAlign="center">
                <Text color="gray.300">No Azure resources found. Connect an Azure account to view resources.</Text>
              </Box>
            </TabPanel>
            
            <TabPanel p={0}>
              <Box p={6} bg="gray.800" borderRadius="md" textAlign="center">
                <Text color="gray.300">No GCP resources found. Connect a GCP account to view resources.</Text>
              </Box>
            </TabPanel>
          </TabPanels>
        </Tabs>
      </VStack>
    </Container>
  );
};

export default Resources;

/**
 * Cost Explorer Page
 * Displays cost analysis and trends across cloud providers
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
  Select,
  Flex,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  StatArrow
} from '@chakra-ui/react';

const CostExplorer: React.FC = () => {
  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Box>
          <Heading size="lg" mb={2} color="cyan.400">Cost Explorer</Heading>
          <Text color="gray.300">
            Analyze and track your cloud spending across all providers
          </Text>
        </Box>
        
        <Divider borderColor="gray.600" />
        
        <Flex justify="space-between" align="center">
          <HStack spacing={4}>
            <Select 
              placeholder="Last 30 days" 
              bg="gray.700" 
              borderColor="gray.600"
              color="white"
              w="200px"
              _hover={{ borderColor: "cyan.400" }}
            >
              <option value="7">Last 7 days</option>
              <option value="30">Last 30 days</option>
              <option value="90">Last 90 days</option>
              <option value="365">Last 12 months</option>
            </Select>
            
            <Select 
              placeholder="All accounts" 
              bg="gray.700" 
              borderColor="gray.600"
              color="white"
              w="200px"
              _hover={{ borderColor: "cyan.400" }}
            >
              <option value="aws">AWS Accounts</option>
              <option value="azure">Azure Accounts</option>
              <option value="gcp">GCP Accounts</option>
            </Select>
          </HStack>
        </Flex>
        
        {/* Cost Summary Cards */}
        <SimpleGrid columns={{ base: 1, md: 2, lg: 4 }} spacing={6}>
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Stat>
                <StatLabel color="gray.400">Total Cost</StatLabel>
                <StatNumber color="white">$12,456.78</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  8.2% from previous period
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Stat>
                <StatLabel color="gray.400">AWS Cost</StatLabel>
                <StatNumber color="white">$8,234.56</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  5.7% from previous period
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Stat>
                <StatLabel color="gray.400">Azure Cost</StatLabel>
                <StatNumber color="white">$3,456.78</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  12.3% from previous period
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
          
          <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
            <CardBody>
              <Stat>
                <StatLabel color="gray.400">GCP Cost</StatLabel>
                <StatNumber color="white">$765.44</StatNumber>
                <StatHelpText>
                  <StatArrow type="increase" />
                  9.1% from previous period
                </StatHelpText>
              </Stat>
            </CardBody>
          </Card>
        </SimpleGrid>
        
        <Tabs variant="soft-rounded" colorScheme="cyan">
          <TabList>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Cost Breakdown</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Cost Trends</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Cost by Service</Tab>
            <Tab color="gray.300" _selected={{ color: 'white', bg: 'cyan.800' }}>Cost by Region</Tab>
          </TabList>
          
          <TabPanels mt={4}>
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Cost Breakdown</Heading>
                </CardHeader>
                <CardBody>
                  <Box h="400px" display="flex" alignItems="center" justifyContent="center">
                    <Text color="gray.300">Cost breakdown chart would appear here</Text>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Cost Trends</Heading>
                </CardHeader>
                <CardBody>
                  <Box h="400px" display="flex" alignItems="center" justifyContent="center">
                    <Text color="gray.300">Cost trends chart would appear here</Text>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Cost by Service</Heading>
                </CardHeader>
                <CardBody>
                  <Box h="400px" display="flex" alignItems="center" justifyContent="center">
                    <Text color="gray.300">Cost by service chart would appear here</Text>
                  </Box>
                </CardBody>
              </Card>
            </TabPanel>
            
            <TabPanel p={0}>
              <Card bg="gray.800" borderColor="gray.700" borderWidth="1px">
                <CardHeader>
                  <Heading size="md" color="white">Cost by Region</Heading>
                </CardHeader>
                <CardBody>
                  <Box h="400px" display="flex" alignItems="center" justifyContent="center">
                    <Text color="gray.300">Cost by region chart would appear here</Text>
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

export default CostExplorer;

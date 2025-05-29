/**
 * Cloud Accounts Page
 * Main page for managing cloud provider accounts
 */

import React, { useState } from 'react';
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
  useColorModeValue,
  VStack,
  HStack,
  Divider,
  Button,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  Flex
} from '@chakra-ui/react';
import { AddIcon } from '@chakra-ui/icons';
import CloudAccountForm from '../components/CloudAccounts/CloudAccountForm';
import CloudAccountsList from '../components/CloudAccounts/CloudAccountsList';

const CloudAccountsPage: React.FC = () => {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const { isOpen, onOpen, onClose } = useDisclosure();
  
  const handleAccountAdded = () => {
    setRefreshTrigger(prev => prev + 1);
    onClose();
  };

  return (
    <Container maxW="container.xl" py={6}>
      <VStack spacing={6} align="stretch">
        <Flex justify="space-between" align="center">
          <Box>
            <Heading size="lg" mb={2} color="cyan.400">Cloud Accounts</Heading>
            <Text color="gray.300">
              Manage your cloud provider accounts and view cost data
            </Text>
          </Box>
          
          <Button 
            leftIcon={<AddIcon />} 
            colorScheme="cyan" 
            onClick={onOpen}
            _hover={{ bg: "cyan.500" }}
          >
            Add Account
          </Button>
        </Flex>
        
        <Divider borderColor="gray.600" />
        
        <Box 
          bg="gray.800" 
          borderRadius="md" 
          p={6} 
          boxShadow="lg"
          borderColor="gray.700"
          borderWidth="1px"
        >
          <CloudAccountsList 
            refreshTrigger={refreshTrigger} 
            onViewAccount={(account) => console.log('View account:', account)}
          />
        </Box>
      </VStack>
      
      {/* Add Account Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay bg="blackAlpha.700" backdropFilter="blur(10px)" />
        <ModalContent bg="gray.800" borderColor="gray.700" borderWidth="1px">
          <ModalHeader color="cyan.400">Add Cloud Account</ModalHeader>
          <ModalCloseButton color="white" />
          <ModalBody pb={6}>
            <CloudAccountForm onSuccess={handleAccountAdded} />
          </ModalBody>
        </ModalContent>
      </Modal>
    </Container>
  );
};

export default CloudAccountsPage;

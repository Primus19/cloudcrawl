/**
 * Login Page Component
 * Handles user authentication
 */

import React, { useState } from 'react';
import {
  Box,
  Button,
  FormControl,
  FormLabel,
  Input,
  VStack,
  Heading,
  Text,
  useToast,
  Container,
  Flex,
  Image,
  InputGroup,
  InputRightElement,
  IconButton
} from '@chakra-ui/react';
import { ViewIcon, ViewOffIcon } from '@chakra-ui/icons';
import { useAuth } from '../contexts/AuthContext';

const Login: React.FC = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [showPassword, setShowPassword] = useState(false);
  const [isLoading, setIsLoading] = useState(false);
  const { login } = useAuth();
  const toast = useToast();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!username || !password) {
      toast({
        title: 'Error',
        description: 'Please enter both username and password',
        status: 'error',
        duration: 3000,
        isClosable: true,
      });
      return;
    }
    
    setIsLoading(true);
    
    try {
      await login(username, password);
      
      toast({
        title: 'Login successful',
        description: 'Welcome to CloudCrawl',
        status: 'success',
        duration: 3000,
        isClosable: true,
      });
    } catch (error: any) {
      toast({
        title: 'Login failed',
        description: error.message || 'Invalid username or password',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Flex 
      minH="100vh" 
      align="center" 
      justify="center" 
      bg="gray.900"
      backgroundImage="linear-gradient(rgba(0, 0, 0, 0.7), rgba(0, 0, 0, 0.7)), url('https://images.unsplash.com/photo-1558494949-ef010cbdcc31?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=2000&q=80')"
      backgroundSize="cover"
      backgroundPosition="center"
    >
      <Container maxW="md">
        <Box 
          p={8} 
          bg="gray.800" 
          borderRadius="md" 
          boxShadow="xl"
          borderColor="gray.700"
          borderWidth="1px"
        >
          <VStack spacing={6} align="stretch">
            <Box textAlign="center" mb={4}>
              <Heading size="xl" color="cyan.400" mb={2}>CloudCrawl</Heading>
              <Text color="gray.300">Cloud Cost Optimization Platform</Text>
            </Box>
            
            <Box as="form" onSubmit={handleSubmit}>
              <VStack spacing={4}>
                <FormControl isRequired>
                  <FormLabel color="gray.300">Username</FormLabel>
                  <Input 
                    type="text" 
                    value={username} 
                    onChange={(e) => setUsername(e.target.value)} 
                    placeholder="Enter your username"
                    bg="gray.700"
                    borderColor="gray.600"
                    color="white"
                    _hover={{ borderColor: "cyan.400" }}
                    _focus={{ borderColor: "cyan.400", boxShadow: "0 0 0 1px #00B5D8" }}
                  />
                </FormControl>
                
                <FormControl isRequired>
                  <FormLabel color="gray.300">Password</FormLabel>
                  <InputGroup>
                    <Input 
                      type={showPassword ? "text" : "password"} 
                      value={password} 
                      onChange={(e) => setPassword(e.target.value)} 
                      placeholder="Enter your password"
                      bg="gray.700"
                      borderColor="gray.600"
                      color="white"
                      _hover={{ borderColor: "cyan.400" }}
                      _focus={{ borderColor: "cyan.400", boxShadow: "0 0 0 1px #00B5D8" }}
                    />
                    <InputRightElement>
                      <IconButton
                        aria-label={showPassword ? "Hide password" : "Show password"}
                        icon={showPassword ? <ViewOffIcon /> : <ViewIcon />}
                        onClick={() => setShowPassword(!showPassword)}
                        variant="ghost"
                        colorScheme="cyan"
                        size="sm"
                      />
                    </InputRightElement>
                  </InputGroup>
                </FormControl>
                
                <Button 
                  type="submit" 
                  colorScheme="cyan" 
                  width="full" 
                  mt={4} 
                  isLoading={isLoading}
                  _hover={{ bg: "cyan.500" }}
                >
                  Sign In
                </Button>
                
                <Text color="gray.400" fontSize="sm" textAlign="center" mt={2}>
                  Demo credentials: admin / admin
                </Text>
              </VStack>
            </Box>
          </VStack>
        </Box>
      </Container>
    </Flex>
  );
};

export default Login;

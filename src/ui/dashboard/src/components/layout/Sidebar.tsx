/**
 * Sidebar Component
 * Main navigation sidebar for the application
 */

import React from 'react';
import { 
  Box, 
  VStack, 
  Icon, 
  Text, 
  Flex, 
  Tooltip,
  Link
} from '@chakra-ui/react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import { 
  FiHome, 
  FiDollarSign, 
  FiServer, 
  FiTrendingUp, 
  FiZap, 
  FiSettings,
  FiCloud,
  FiCode,
  FiActivity
} from 'react-icons/fi';

interface NavItemProps {
  icon: any;
  children: string;
  to: string;
}

const NavItem = ({ icon, children, to }: NavItemProps) => {
  const location = useLocation();
  const isActive = location.pathname === to;
  
  return (
    <Tooltip label={children} placement="right" hasArrow>
      <Link
        as={RouterLink}
        to={to}
        style={{ textDecoration: 'none' }}
        _focus={{ boxShadow: 'none' }}
      >
        <Flex
          align="center"
          p="4"
          mx="4"
          borderRadius="lg"
          role="group"
          cursor="pointer"
          bg={isActive ? 'cyan.900' : 'transparent'}
          color={isActive ? 'white' : 'gray.400'}
          _hover={{
            bg: 'cyan.900',
            color: 'white',
          }}
          transition="all 0.2s"
        >
          <Icon
            mr="4"
            fontSize="16"
            as={icon}
            _groupHover={{
              color: 'cyan.400',
            }}
            color={isActive ? 'cyan.400' : 'gray.400'}
          />
          <Text fontSize="sm">{children}</Text>
        </Flex>
      </Link>
    </Tooltip>
  );
};

const Sidebar = () => {
  return (
    <Box
      bg="gray.800"
      borderRight="1px"
      borderRightColor="gray.700"
      w={{ base: 'full', md: 60 }}
      pos="fixed"
      h="full"
    >
      <Flex h="20" alignItems="center" mx="8" justifyContent="space-between">
        <Text fontSize="2xl" fontWeight="bold" color="cyan.400">
          CloudCrawl
        </Text>
      </Flex>
      <VStack spacing={0} align="stretch">
        <NavItem icon={FiHome} to="/">
          Dashboard
        </NavItem>
        <NavItem icon={FiDollarSign} to="/cost-explorer">
          Cost Explorer
        </NavItem>
        <NavItem icon={FiServer} to="/resources">
          Resources
        </NavItem>
        <NavItem icon={FiTrendingUp} to="/recommendations">
          Recommendations
        </NavItem>
        <NavItem icon={FiZap} to="/actions">
          Actions
        </NavItem>
        <NavItem icon={FiActivity} to="/workflows">
          Workflows
        </NavItem>
        
        <Box my={4} borderTop="1px" borderColor="gray.700" />
        
        <NavItem icon={FiCloud} to="/cloud-accounts">
          Cloud Accounts
        </NavItem>
        <NavItem icon={FiCode} to="/terraform">
          Terraform
        </NavItem>
        <NavItem icon={FiSettings} to="/settings">
          Settings
        </NavItem>
      </VStack>
    </Box>
  );
};

export default Sidebar;

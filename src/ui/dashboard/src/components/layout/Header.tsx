/**
 * Header Component
 * Top navigation bar for the application
 */

import React from 'react';
import {
  Box,
  Flex,
  Text,
  IconButton,
  Button,
  Stack,
  Collapse,
  Icon,
  Popover,
  PopoverTrigger,
  PopoverContent,
  useColorModeValue,
  useDisclosure,
  Avatar,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  HStack,
  Badge
} from '@chakra-ui/react';
import {
  HamburgerIcon,
  CloseIcon,
  ChevronDownIcon,
  ChevronRightIcon,
  BellIcon,
  SettingsIcon
} from '@chakra-ui/icons';
import { useAuth } from '../../contexts/AuthContext';

const Header = () => {
  const { isOpen, onToggle } = useDisclosure();
  const { user, logout } = useAuth();

  return (
    <Box
      bg="gray.800"
      px={4}
      borderBottom={1}
      borderStyle={'solid'}
      borderColor="gray.700"
      position="sticky"
      top={0}
      zIndex={10}
    >
      <Flex
        color="white"
        minH={'60px'}
        py={{ base: 2 }}
        px={{ base: 4 }}
        align={'center'}
        justify="flex-end"
      >
        <HStack spacing={4}>
          {/* Notifications */}
          <Menu>
            <MenuButton
              as={IconButton}
              aria-label="Notifications"
              icon={<BellIcon />}
              variant="ghost"
              colorScheme="cyan"
              fontSize="lg"
            />
            <MenuList bg="gray.700" borderColor="gray.600">
              <MenuItem bg="gray.700" _hover={{ bg: 'gray.600' }}>
                <Box>
                  <Text fontWeight="medium">Cost Alert</Text>
                  <Text fontSize="sm" color="gray.400">AWS costs exceeded threshold</Text>
                </Box>
              </MenuItem>
              <MenuItem bg="gray.700" _hover={{ bg: 'gray.600' }}>
                <Box>
                  <Text fontWeight="medium">New Recommendation</Text>
                  <Text fontSize="sm" color="gray.400">3 new cost-saving opportunities</Text>
                </Box>
              </MenuItem>
              <MenuDivider borderColor="gray.600" />
              <MenuItem bg="gray.700" _hover={{ bg: 'gray.600' }}>
                View all notifications
              </MenuItem>
            </MenuList>
          </Menu>

          {/* User Menu */}
          <Menu>
            <MenuButton
              as={Button}
              rounded={'full'}
              variant={'link'}
              cursor={'pointer'}
              minW={0}
            >
              <HStack>
                <Avatar
                  size={'sm'}
                  bg="cyan.500"
                  name={user?.full_name || 'User'}
                />
                <Box display={{ base: 'none', md: 'flex' }}>
                  <Text>{user?.full_name || 'User'}</Text>
                  <Badge ml={2} colorScheme="cyan" variant="solid">
                    {user?.role || 'User'}
                  </Badge>
                </Box>
              </HStack>
            </MenuButton>
            <MenuList bg="gray.700" borderColor="gray.600">
              <MenuItem bg="gray.700" _hover={{ bg: 'gray.600' }}>Profile</MenuItem>
              <MenuItem bg="gray.700" _hover={{ bg: 'gray.600' }}>Settings</MenuItem>
              <MenuDivider borderColor="gray.600" />
              <MenuItem 
                bg="gray.700" 
                _hover={{ bg: 'gray.600' }}
                onClick={() => logout()}
              >
                Sign Out
              </MenuItem>
            </MenuList>
          </Menu>
        </HStack>
      </Flex>
    </Box>
  );
};

export default Header;

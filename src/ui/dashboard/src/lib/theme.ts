import { createTheme } from '@mui/material/styles';

// Create a dark theme with cybersecurity-inspired colors
const theme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#4caf50', // Green for success/action
      light: '#80e27e',
      dark: '#087f23',
      contrastText: '#000000',
    },
    secondary: {
      main: '#03a9f4', // Blue for information
      light: '#67daff',
      dark: '#007ac1',
      contrastText: '#000000',
    },
    error: {
      main: '#f44336', // Red for errors/critical issues
      light: '#ff7961',
      dark: '#ba000d',
      contrastText: '#ffffff',
    },
    warning: {
      main: '#ff9800', // Orange for warnings
      light: '#ffc947',
      dark: '#c66900',
      contrastText: '#000000',
    },
    info: {
      main: '#2196f3', // Light blue for info
      light: '#6ec6ff',
      dark: '#0069c0',
      contrastText: '#000000',
    },
    success: {
      main: '#4caf50', // Green for success
      light: '#80e27e',
      dark: '#087f23',
      contrastText: '#000000',
    },
    background: {
      default: '#121212', // Dark background
      paper: '#1e1e1e', // Slightly lighter for cards/surfaces
    },
    text: {
      primary: '#ffffff',
      secondary: '#b0bec5',
      disabled: '#6c7a89',
    },
    divider: 'rgba(255, 255, 255, 0.12)',
    // Custom colors for cost optimization
    cost: {
      high: '#f44336', // Red for high cost
      medium: '#ff9800', // Orange for medium cost
      low: '#4caf50', // Green for low cost
      saving: '#00e676', // Bright green for savings
    },
  },
  typography: {
    fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
    h1: {
      fontSize: '2.5rem',
      fontWeight: 500,
    },
    h2: {
      fontSize: '2rem',
      fontWeight: 500,
    },
    h3: {
      fontSize: '1.75rem',
      fontWeight: 500,
    },
    h4: {
      fontSize: '1.5rem',
      fontWeight: 500,
    },
    h5: {
      fontSize: '1.25rem',
      fontWeight: 500,
    },
    h6: {
      fontSize: '1rem',
      fontWeight: 500,
    },
    subtitle1: {
      fontSize: '1rem',
      fontWeight: 400,
    },
    subtitle2: {
      fontSize: '0.875rem',
      fontWeight: 500,
    },
    body1: {
      fontSize: '1rem',
      fontWeight: 400,
    },
    body2: {
      fontSize: '0.875rem',
      fontWeight: 400,
    },
    button: {
      fontSize: '0.875rem',
      fontWeight: 500,
      textTransform: 'none',
    },
    caption: {
      fontSize: '0.75rem',
      fontWeight: 400,
    },
    overline: {
      fontSize: '0.75rem',
      fontWeight: 400,
      textTransform: 'uppercase',
    },
  },
  shape: {
    borderRadius: 8,
  },
  components: {
    MuiAppBar: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
        },
      },
    },
    MuiDrawer: {
      styleOverrides: {
        paper: {
          backgroundColor: '#1e1e1e',
          borderRight: '1px solid rgba(255, 255, 255, 0.12)',
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundColor: '#1e1e1e',
          boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)',
          border: '1px solid rgba(255, 255, 255, 0.05)',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 4,
          textTransform: 'none',
          fontWeight: 500,
        },
        contained: {
          boxShadow: '0 2px 4px rgba(0, 0, 0, 0.2)',
        },
      },
    },
    MuiTableHead: {
      styleOverrides: {
        root: {
          backgroundColor: 'rgba(255, 255, 255, 0.05)',
        },
      },
    },
    MuiTableRow: {
      styleOverrides: {
        root: {
          '&:nth-of-type(odd)': {
            backgroundColor: 'rgba(255, 255, 255, 0.02)',
          },
          '&:hover': {
            backgroundColor: 'rgba(255, 255, 255, 0.08)',
          },
        },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: {
          borderRadius: 4,
        },
      },
    },
  },
});

// Add custom types to the theme
declare module '@mui/material/styles' {
  interface Palette {
    cost: {
      high: string;
      medium: string;
      low: string;
      saving: string;
    };
  }
  
  interface PaletteOptions {
    cost?: {
      high: string;
      medium: string;
      low: string;
      saving: string;
    };
  }
}

export default theme;

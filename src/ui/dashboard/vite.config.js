// CommonJS syntax for vite.config.js
const path = require("path");
const react = require("@vitejs/plugin-react");
const { defineConfig } = require("vite");

module.exports = defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  build: {
    outDir: 'build',
    sourcemap: true,
    rollupOptions: {
<<<<<<< HEAD
      external: ['@mui/x-data-grid'],
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          mui: ['@mui/material', '@mui/icons-material']
=======
      external: [],
      output: {
        manualChunks: {
          vendor: ['react', 'react-dom', 'react-router-dom'],
          mui: ['@mui/material', '@mui/icons-material', '@mui/x-data-grid']
>>>>>>> 30402d48bafbc7664fafa92efffb15ad12e4e8fd
        }
      }
    }
  },
  optimizeDeps: {
    include: ['@mui/material', '@mui/icons-material', '@mui/x-data-grid']
  },
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
      },
    },
  },
});

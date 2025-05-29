// CommonJS syntax for vite.config.js
const { defineConfig } = require('vite');
const react = require('@vitejs/plugin-react');

module.exports = defineConfig({
  plugins: [react()],
  server: {
    host: '0.0.0.0',
    port: 3002,
    strictPort: true,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false
      }
    },
    cors: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      '.manusvm.computer'
    ]
  },
  preview: {
    host: '0.0.0.0',
    port: 4173,
    strictPort: true,
    allowedHosts: [
      'localhost',
      '127.0.0.1',
      '0.0.0.0',
      '.manusvm.computer'
    ]
  }
});

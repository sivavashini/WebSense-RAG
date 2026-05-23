import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    // Vercel deployment: frontend code calls /api/*.
    // During local Vite development, proxy those same paths to the local FastAPI server.
    proxy: {
      '/api/ws': {
        target: process.env.VITE_BACKEND_DEV_WS_TARGET || 'ws://127.0.0.1:8000',
        ws: true,
        changeOrigin: true,
      },
      '/api': {
        target: process.env.VITE_BACKEND_DEV_TARGET || 'http://127.0.0.1:8000',
        changeOrigin: true,
      },
    },
  },
})

import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  root: path.resolve('./'),
  build: {
    outDir: 'dist',       // frontend/dist
    emptyOutDir: true
  },
  server: {
    port: 5173,
    open: true
  }
})

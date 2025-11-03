import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  build: {
    outDir: 'dist', // output folder relative to the root of frontend
    emptyOutDir: true
  },
  root: path.resolve(__dirname)
})

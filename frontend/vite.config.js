/* Diretly from vite github https://github.com/vitejs/vite/blob/e4ad62ba6523e889f988b6e882d9d81be7f26711/packages/create-vite/template-react/vite.config.js */
import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
})

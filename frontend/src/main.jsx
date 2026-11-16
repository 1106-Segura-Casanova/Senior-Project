/* Purpose: Starts the app*/
/* Directly from Vite github with the exception of firebase import. github repo : https://github.com/vitejs/vite/blob/e4ad62ba6523e889f988b6e882d9d81be7f26711/packages/create-vite/template-react/src/main.jsx#L1-L10*/
import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import "./config/firebase"

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <App />
  </StrictMode>,
)

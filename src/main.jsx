import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { Toaster } from 'react-hot-toast'
import './index.css'
import App from './App.jsx'

createRoot(document.getElementById('root')).render(
  <StrictMode>
    <Toaster
      position="top-right"
      toastOptions={{
        style: {
          borderRadius: '12px',
          border: '1px solid rgba(15, 23, 42, 0.08)',
          background: 'rgba(255,255,255,0.95)',
          color: '#0f172a',
        },
      }}
    />
    <App />
  </StrictMode>,
)

import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.tsx'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)

import { GoogleReCaptchaProvider } from 'react-google-recaptcha-v3'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <GoogleReCaptchaProvider reCaptchaKey={import.meta.env.VITE_RECAPTCHA_SITE_KEY}>
      <App />
    </GoogleReCaptchaProvider>
  </React.StrictMode>,
)
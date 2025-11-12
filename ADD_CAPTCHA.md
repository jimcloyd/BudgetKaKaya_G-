# Adding CAPTCHA to Login and Registration

## Overview

We'll add Google reCAPTCHA v3 (invisible CAPTCHA) to protect login and registration from bots.

## Step 1: Get reCAPTCHA Keys

1. Go to: https://www.google.com/recaptcha/admin/create
2. Fill in:
   - **Label**: Family Budget Tracker
   - **reCAPTCHA type**: Select "reCAPTCHA v3"
   - **Domains**: 
     - `localhost` (for testing)
     - `budget-tracker-1593570189.s3-website-us-east-1.amazonaws.com`
     - Your custom domain (if you have one)
3. Accept terms and click **Submit**
4. You'll get:
   - **Site Key** (public, goes in frontend)
   - **Secret Key** (private, goes in backend)

## Step 2: Add to Frontend

### Install Package
```powershell
cd frontend
npm install react-google-recaptcha-v3
```

### Update .env.production
```
VITE_RECAPTCHA_SITE_KEY=your_site_key_here
```

### Wrap App with reCAPTCHA Provider
File: `frontend/src/main.tsx`

```typescript
import { GoogleReCaptchaProvider } from 'react-google-recaptcha-v3'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <GoogleReCaptchaProvider reCaptchaKey={import.meta.env.VITE_RECAPTCHA_SITE_KEY}>
      <App />
    </GoogleReCaptchaProvider>
  </React.StrictMode>,
)
```

### Update LoginPage
File: `frontend/src/pages/LoginPage.tsx`

```typescript
import { useGoogleReCaptcha } from 'react-google-recaptcha-v3'

const LoginPage = () => {
  const { executeRecaptcha } = useGoogleReCaptcha()
  
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    // Get reCAPTCHA token
    if (!executeRecaptcha) {
      setError('reCAPTCHA not loaded')
      return
    }
    
    const token = await executeRecaptcha('login')
    
    // Send token with login request
    await login(email, password, token)
  }
}
```

### Update RegisterPage
Same pattern as LoginPage

## Step 3: Add to Backend

### Install Package
```powershell
cd backend
pip install requests
```

### Update requirements.txt
Add: `requests==2.31.0`

### Create reCAPTCHA Verification Function
File: `backend/app/recaptcha.py`

```python
import requests
import os

def verify_recaptcha(token: str, action: str) -> bool:
    """Verify reCAPTCHA token with Google"""
    secret_key = os.getenv('RECAPTCHA_SECRET_KEY')
    
    if not secret_key:
        return True  # Skip in development
    
    response = requests.post(
        'https://www.google.com/recaptcha/api/siteverify',
        data={
            'secret': secret_key,
            'response': token
        }
    )
    
    result = response.json()
    
    # Check if verification succeeded and score is good
    return (
        result.get('success', False) and
        result.get('action') == action and
        result.get('score', 0) >= 0.5  # Adjust threshold as needed
    )
```

### Update Auth Routes
File: `backend/app/routes/auth.py`

```python
from app.recaptcha import verify_recaptcha

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    # Verify reCAPTCHA
    recaptcha_token = data.get('recaptcha_token')
    if not verify_recaptcha(recaptcha_token, 'login'):
        return jsonify({'error': 'reCAPTCHA verification failed'}), 400
    
    # Rest of login logic...
```

### Update Environment Variables
Add to Elastic Beanstalk:
```powershell
cd backend
eb setenv RECAPTCHA_SECRET_KEY=your_secret_key_here
```

## Step 4: Test

### Local Testing
1. Start backend: `python run.py`
2. Start frontend: `npm run dev`
3. Try logging in
4. Check browser console for reCAPTCHA token
5. Check backend logs for verification

### Production Testing
1. Deploy to Dev
2. Test login/registration
3. Check AWS logs

## Benefits

✅ **Invisible** - No clicking required  
✅ **Bot Protection** - Blocks automated attacks  
✅ **Brute Force Prevention** - Limits login attempts  
✅ **Free** - Google reCAPTCHA is free  
✅ **Easy** - Minimal code changes  

## Score Threshold

reCAPTCHA v3 returns a score (0.0 to 1.0):
- **1.0** - Very likely human
- **0.5** - Neutral (recommended threshold)
- **0.0** - Very likely bot

Adjust in `recaptcha.py` based on your needs.

## Alternative: reCAPTCHA v2

If you prefer the checkbox "I'm not a robot":

Use `react-google-recaptcha` instead:
```bash
npm install react-google-recaptcha
```

Requires user interaction but more obvious.

---

**Recommendation**: Use reCAPTCHA v3 for better user experience (invisible).

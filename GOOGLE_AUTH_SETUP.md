# Google OAuth Integration Setup Guide

Google authentication has been successfully integrated into your Neuro Agentic AI application! Follow these steps to complete the setup.

## 🔑 Prerequisites

You need to create a Google OAuth 2.0 Client ID from the Google Cloud Console.

## 📋 Setup Instructions

### Step 1: Create Google OAuth Credentials

1. Go to [Google Cloud Console](https://console.developers.google.com/)
2. Create a new project or select an existing one
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth Client ID**
5. Configure the OAuth consent screen if you haven't already
6. Select **Web application** as the application type
7. Add the following URLs:
   - **Authorized JavaScript origins**: `http://localhost:5173`
   - **Authorized redirect URIs**: `http://localhost:5173`
8. Click **Create** and copy your **Client ID** and **Client Secret**

### Step 2: Configure Backend

1. Navigate to the `backend` directory
2. Create a `.env` file (or update existing one):

```env
# Google OAuth Configuration
GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
GOOGLE_CLIENT_SECRET=your-google-client-secret

# JWT Secret Key (generate a secure random string)
SECRET_KEY=your-secret-key-change-this-in-production

# Gemini API Key
GOOGLE_API_KEY=your-gemini-api-key
```

3. Install the new dependencies:

```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Configure Frontend

1. Navigate to the `frontend` directory
2. Create a `.env` file:

```env
VITE_GOOGLE_CLIENT_ID=your-google-client-id.apps.googleusercontent.com
```

3. Install the new dependencies:

```bash
cd frontend
npm install
```

### Step 4: Run the Application

1. Start the backend server:

```bash
cd backend
uvicorn main:app --reload
```

2. Start the frontend development server:

```bash
cd frontend
npm run dev
```

3. Open your browser and navigate to `http://localhost:5173`

## ✨ Features Implemented

### Backend (FastAPI)

- ✅ JWT token generation and verification
- ✅ Google OAuth token validation
- ✅ Protected endpoints with bearer token authentication
- ✅ User session management
- ✅ Auth endpoints:
  - `POST /auth/google` - Authenticate with Google token
  - `GET /auth/me` - Get current user information
  - `POST /auth/logout` - Logout user

### Frontend (React)

- ✅ Google OAuth login button
- ✅ Authentication context for state management
- ✅ User profile display in navbar
- ✅ Automatic token persistence in localStorage
- ✅ Dropdown menu with user info and logout
- ✅ Responsive design with beautiful UI

## 🔒 Security Notes

1. **Never commit your `.env` files** to version control
2. Generate a strong, random `SECRET_KEY` for production
3. In production, update:
   - Backend CORS origins to match your domain
   - Google OAuth authorized origins and redirect URIs
   - Use HTTPS for all connections

## 🚀 Usage

1. Users click the "Sign in with Google" button
2. Google OAuth popup appears
3. After authentication, user info appears in the navbar
4. JWT token is stored in localStorage
5. Token is sent with protected API requests via Authorization header

## 🛡️ Protected Routes Example

To protect your analyze endpoint or other routes, add authentication:

```python
from api.auth import verify_token
from fastapi import Depends

@router.post("/analyze")
async def analyze_image(
    file: UploadFile,
    token_data: dict = Depends(verify_token)  # Add this
):
    # Your existing code
    # Access user email via token_data.get("sub")
    pass
```

## 📝 Notes

- The current implementation uses in-memory storage for users
- For production, integrate with a database (PostgreSQL, MongoDB, etc.)
- Consider adding refresh tokens for longer sessions
- Implement rate limiting for security

## 🆘 Troubleshooting

### "Invalid token" errors
- Ensure your GOOGLE_CLIENT_ID matches in both frontend and backend
- Check that the token is being sent in the Authorization header

### CORS errors
- Verify the frontend URL in backend's CORS middleware
- Ensure credentials are enabled

### Login button not appearing
- Check browser console for errors
- Verify npm install completed successfully
- Ensure .env file has the correct GOOGLE_CLIENT_ID

---

Happy coding! 🎉

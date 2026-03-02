# Render Deployment Guide

## Setup Instructions

### 1. Prerequisites
- GitHub account with your code pushed to a repository
- Render account (free tier available at render.com)

### 2. Deploy to Render

#### Option A: Using render.yaml (Recommended - Already Set Up)

1. **Push to GitHub**
   - Make sure all changes are committed and pushed:
   ```bash
   git add .
   git commit -m "Add render.yaml for deployment"
   git push origin main
   ```

2. **Create Blueprint**
   - Go to [Render Dashboard](https://dashboard.render.com)
   - Click "New +" → "Blueprint"
   - Connect your GitHub repository
   - Select the branch (main)
   - Render will automatically detect the render.yaml file

3. **Environment Variables**
   After deployment, set this variable in Render dashboard:
   - **VITE_API_URL**: `https://factory-dashboard-api.onrender.com`
     (Replace with your actual API service URL from the Render dashboard)

#### Option B: Manual Deployment

If the yaml approach doesn't work, manually create two services:

**Backend Service:**
- Go to Render Dashboard → "New +" → "Web Service"
- Connect GitHub repo
- Settings:
  - Name: `factory-dashboard-api`
  - Runtime: `Python`
  - Build Command: `pip install -r backend/requirements.txt`
  - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
  - Region: Choose closest to you
  - Plan: Free tier available

**Frontend Service:**
- Go to Render Dashboard → "New +" → "Static Site"
- Connect GitHub repo
- Settings:
  - Name: `factory-dashboard-web`
  - Build Command: `cd frontend && npm install && npm run build`
  - Publish Directory: `frontend/dist`
  - Environment Variables:
    - `VITE_API_URL`: Set after backend deployment

### 3. Important Notes

#### CORS Configuration
If you get CORS errors, add this to your FastAPI backend (backend/main.py):

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://your-frontend-url.onrender.com"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### Database
If using SQLite (factory.db):
- The database created locally will NOT persist on Render's free tier
- For production, use a paid instance or migrate to PostgreSQL
- To migrate to PostgreSQL:
  1. Create a PostgreSQL database on Render
  2. Update `DATABASE_URL` in your backend environment variables
  3. Update your backend code to use PostgreSQL connection string

#### Available Endpoints
- Backend API: `https://factory-dashboard-api.onrender.com`
- Frontend: `https://factory-dashboard-web.onrender.com`
- Metrics endpoint: `https://factory-dashboard-api.onrender.com/metrics`

### 4. Troubleshooting

**Frontend can't connect to API:**
- Check VITE_API_URL environment variable is set correctly
- Verify the backend service is running (check Render logs)
- Ensure CORS is properly configured in the backend

**Free tier limitations:**
- Services spin down after 15 minutes of inactivity
- This means the first request after inactivity will be slow
- Use paid tier for production

**Check Logs:**
- Go to your service in Render Dashboard
- Click "Logs" tab to see deployment and runtime errors

### 5. Next Steps
After deployment:
1. Test the API: `https://your-api-url.onrender.com/metrics`
2. Test the frontend at your static site URL
3. Monitor the Logs tab for any issues

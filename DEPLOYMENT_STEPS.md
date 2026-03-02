# 🚀 Deploy Factory Dashboard to Render - Quick Start

## Prerequisites
- ✅ GitHub account with repository
- ✅ Render account (free at [render.com](https://render.com))
- ✅ Code committed and pushed to GitHub

## Deployment Steps

### Step 1: Prepare Your GitHub Repository

```bash
# Make sure all changes are committed
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### Step 2: Deploy to Render (Using Blueprint)

1. **Login to Render**
   - Go to [https://dashboard.render.com](https://dashboard.render.com)
   - Sign in with GitHub account

2. **Create Blueprint**
   - Click **"New +"** button (top right)
   - Select **"Blueprint"**
   - Select your repository containing the Factory Dashboard
   - Select branch: **main** (or your default branch)

3. **Review and Deploy**
   - Render will automatically detect `render.yaml`
   - You'll see two services ready to deploy:
     - `factory-dashboard-api` (Backend)
     - `factory-dashboard-web` (Frontend)
   - Click **"Create New Blueprint Instance"**
   - Wait for deployment (5-10 minutes)

### Step 3: Connect Frontend and Backend

**Important:** The frontend needs to know the backend URL for production.

1. After deployment, note your **Backend API URL** from Render dashboard:
   - Format: `https://factory-dashboard-api-xxx.onrender.com`

2. Set environment variable for frontend:
   - Go to **factory-dashboard-web** service
   - Click **"Environment"**
   - Add new variable:
     - **Key**: `VITE_API_URL`
     - **Value**: `https://factory-dashboard-api-xxx.onrender.com` (your backend URL)
   - Click **"Deploy"** to apply changes

3. Wait for frontend to rebuild and deploy

### Step 4: Test Your Deployment

1. **Open Dashboard**
   - Backend: `https://factory-dashboard-api-xxx.onrender.com/health`
   - Frontend: `https://factory-dashboard-web-xxx.onrender.com`

2. **Test Features**
   - Load dashboard
   - Submit an event in "Post Event" tab
   - Check metrics update in "Dashboard" tab

## Troubleshooting

### Frontend Can't Connect to Backend
**Symptom:** Black page or "internal server error"

**Solution:**
1. Check `VITE_API_URL` is set correctly
2. Verify both services are running (check Render logs)
3. Ensure CORS is enabled in backend (it is by default)

### Services Taking a Long Time
**Cause:** Render free tier spins down after 15 minutes of inactivity

**Solution:** Make the first request and wait, or upgrade to paid tier

### Database Data Lost
**Cause:** SQLite on free plan doesn't persist across deploys

**Workaround for production:** Upgrade to PostgreSQL on Render
- Create PostgreSQL database on Render
- Set `DATABASE_URL` environment variable on backend
- Redeploy backend

## Environment Variables Explained

### For Frontend (factory-dashboard-web)
- `VITE_API_URL`: URL of backend API
  - Development: `http://localhost:8000`
  - Production: `https://your-backend-url.onrender.com`

### For Backend (factory-dashboard-api)
- `DATABASE_URL` (optional): PostgreSQL connection string
  - Default: Uses SQLite (`factory_dashboard.db`)
  - Production: `postgresql://user:pass@host:port/dbname`

## API Endpoints

Once deployed, your endpoints are available at:
- Health check: `https://factory-dashboard-api-xxx.onrender.com/health`
- Metrics: `https://factory-dashboard-api-xxx.onrender.com/metrics`
- Workers: `https://factory-dashboard-api-xxx.onrender.com/workers`
- Workstations: `https://factory-dashboard-api-xxx.onrender.com/workstations`
- Events: `https://factory-dashboard-api-xxx.onrender.com/events`

## Manual Deployment (If Blueprint Fails)

If the Blueprint approach doesn't work, you can manually create services:

### Backend Service
1. Go to Render → "New +" → "Web Service"
2. Connect GitHub repo
3. Settings:
   - **Name**: factory-dashboard-api
   - **Runtime**: Python 3
   - **Build Command**: `pip install -r backend/requirements.txt`
   - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`

### Frontend Service
1. Go to Render → "New +" → "Web Service"
2. Connect GitHub repo
3. Settings:
   - **Name**: factory-dashboard-web
   - **Build Command**: `cd frontend && npm install && npm run build`
   - **Start Command**: `npm run preview`
   - **Publish directory**: `frontend/dist`

## Next Steps

- Monitor Render logs: Dashboard → Service → Logs
- Set up auto-deploy: Active branch rebuilds on push
- Consider upgrading to paid plan for production
- Set up PostgreSQL for persistent data

## Support

- Render Docs: https://render.com/docs
- FastAPI Docs: https://fastapi.tiangolo.com/deployment/
- React Deployment: https://vitejs.dev/guide/static-deploy.html

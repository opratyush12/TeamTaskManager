# Railway Deployment Guide - Team Task Manager

This guide will help you deploy your Team Task Manager application on Railway.

## 📋 Prerequisites

- Railway account (https://railway.app)
- GitHub account
- Git installed locally
- Docker installed (for local testing)

## 🚀 Deployment Options

### Option 1: Deploy Backend and Frontend Separately (Recommended)

This is the recommended approach as Railway works best with separate services.

#### Step 1: Push Code to GitHub

1. **Initialize Git repository** (if not already done):
```bash
cd TeamTaskManager
git init
git add .
git commit -m "Initial commit - Team Task Manager"
```

2. **Create GitHub repository**:
   - Go to https://github.com/new
   - Create a new repository (e.g., `team-task-manager`)
   - Copy the repository URL

3. **Push to GitHub**:
```bash
git remote add origin https://github.com/YOUR_USERNAME/team-task-manager.git
git branch -M main
git push -u origin main
```

#### Step 2: Deploy Backend on Railway

1. **Login to Railway**:
   - Go to https://railway.app
   - Sign in with GitHub

2. **Create New Project**:
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Select your `team-task-manager` repository

3. **Configure Backend Service**:
   - Railway will detect the `railway.json` file
   - Add environment variables:
     - `SECRET_KEY`: Generate strong secret (use: `openssl rand -hex 32`)
     - `DATABASE_URL`: `sqlite:////app/data/task_manager.db`
     - `ALGORITHM`: `HS256`
     - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
     - `REFRESH_TOKEN_EXPIRE_DAYS`: `7`

4. **Add Volume for Database** (Important!):
   - Go to service settings
   - Click "Variables" tab
   - Add volume: `/app/data` (to persist SQLite database)

5. **Deploy**:
   - Railway will automatically build and deploy
   - Copy the backend URL (e.g., `https://your-app.railway.app`)

#### Step 3: Deploy Frontend on Railway

1. **Create Second Service**:
   - In the same project, click "New Service"
   - Select "Deploy from GitHub repo"
   - Select the same repository

2. **Configure Dockerfile**:
   - In service settings, go to "Settings"
   - Set "Dockerfile Path" to `Dockerfile.frontend`
   - Set "Root Directory" to `/` (or leave default)

3. **Add Environment Variable**:
   - Add `VITE_API_URL`: `https://your-backend-url.railway.app` (from Step 2)

4. **Configure Build**:
   - Railway will use the Dockerfile.frontend
   - Build args will be passed automatically

5. **Deploy**:
   - Railway will build and deploy
   - Copy the frontend URL

6. **Update Backend CORS**:
   - Go back to backend service
   - Add environment variable:
     - `CORS_ORIGINS`: `https://your-frontend-url.railway.app`
   - Redeploy backend if needed

#### Step 4: Update Backend for CORS

The backend is already configured for CORS with `allow_origins=["*"]` in development. For production, you should update it:

1. Edit `app/main.py` to use environment variable:
```python
import os

app.add_middleware(
    CORSMiddleware,
    allow_origins=os.getenv("CORS_ORIGINS", "*").split(","),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

2. Commit and push changes.

### Option 2: Deploy with Docker Compose (Alternative)

Railway also supports docker-compose, but it's more complex for multi-service apps.

1. Use the provided `docker-compose.yml`
2. Railway will deploy both services together
3. Less flexible for scaling individual services

## 🧪 Test Locally with Docker

Before deploying, test locally:

### Build and Run Backend
```bash
docker build -f Dockerfile.backend -t taskmanager-backend .
docker run -p 8000:8000 -e SECRET_KEY=test-secret taskmanager-backend
```

### Build and Run Frontend
```bash
docker build -f Dockerfile.frontend -t taskmanager-frontend .
docker run -p 80:80 taskmanager-frontend
```

### Or Use Docker Compose
```bash
# Set environment variable
export SECRET_KEY=$(openssl rand -hex 32)

# Build and run
docker-compose up --build

# Run in background
docker-compose up -d

# Stop
docker-compose down
```

Access:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 🔐 Environment Variables

### Backend (Required)
- `SECRET_KEY`: Strong random string (32+ characters)
- `DATABASE_URL`: Database connection string
- `ALGORITHM`: `HS256`
- `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
- `REFRESH_TOKEN_EXPIRE_DAYS`: `7`

### Backend (Optional)
- `CORS_ORIGINS`: Comma-separated list of allowed origins
- `PORT`: Railway sets this automatically

### Frontend (Build-time)
- `VITE_API_URL`: Backend API URL (must be set during build)

## 📊 Database Persistence

### Important for Railway!

Railway provides ephemeral storage by default. To persist your SQLite database:

1. **Add Volume**:
   - Go to backend service settings
   - Navigate to "Variables" or "Volumes"
   - Add mount: `/app/data`
   - This will persist the database across deployments

2. **Alternative: Use PostgreSQL**:
   For production, consider using Railway's PostgreSQL:
   ```bash
   # In Railway dashboard
   1. Add PostgreSQL service to project
   2. Link to backend service
   3. Update requirements.txt: add psycopg2-binary
   4. Update DATABASE_URL environment variable (Railway auto-sets this)
   5. Update database.py to handle PostgreSQL connection
   ```

## 🔄 CI/CD Setup

Railway automatically deploys when you push to main:

1. **Automatic Deployments**:
   - Push to GitHub main branch
   - Railway detects changes
   - Automatically rebuilds and deploys

2. **Manual Deployments**:
   - Go to Railway dashboard
   - Click "Deploy" button
   - Select commit or branch

3. **Rollback**:
   - Go to Deployments tab
   - Click on previous deployment
   - Click "Rollback"

## 🐛 Troubleshooting

### Backend won't start
- Check logs in Railway dashboard
- Verify all environment variables are set
- Check SECRET_KEY is set and not empty
- Verify database path is correct

### Frontend can't connect to backend
- Check VITE_API_URL is set correctly
- Verify CORS settings on backend
- Check both services are deployed and running
- Test backend URL directly (should return JSON)

### Database resets on deploy
- Add volume mount: `/app/data`
- Or switch to PostgreSQL for production

### Build fails
- Check Dockerfile syntax
- Verify all files are committed to Git
- Check .dockerignore isn't excluding needed files
- Review build logs in Railway

## 📈 Scaling

Railway makes scaling easy:

1. **Vertical Scaling**:
   - Go to service settings
   - Increase memory/CPU
   - Railway handles automatically

2. **Horizontal Scaling**:
   - Railway Pro plan supports replicas
   - Add replicas in service settings
   - Consider using PostgreSQL instead of SQLite

## 💰 Cost Optimization

- **Free Tier**: $5 credit/month, enough for small apps
- **Pro Plan**: $20/month for unlimited projects
- **Resource Usage**: Monitor in dashboard
- **Optimization Tips**:
  - Use appropriate container sizes
  - Enable HTTP/2 and gzip compression (already configured)
  - Cache static assets (already configured in Nginx)

## 🔒 Security Best Practices

1. **Never commit**:
   - `.env` files
   - Secret keys
   - Database files

2. **Always set**:
   - Strong SECRET_KEY
   - Proper CORS origins (not *)
   - HTTPS only (Railway provides this)

3. **Consider adding**:
   - Rate limiting
   - API authentication headers
   - Request size limits

## 📚 Additional Resources

- Railway Documentation: https://docs.railway.app
- Railway Discord: https://discord.gg/railway
- Docker Best Practices: https://docs.docker.com/develop/dev-best-practices/

## 🎉 Quick Deploy Checklist

- [ ] Push code to GitHub
- [ ] Create Railway project
- [ ] Deploy backend service
- [ ] Set environment variables (SECRET_KEY, etc.)
- [ ] Add volume for database persistence
- [ ] Copy backend URL
- [ ] Deploy frontend service
- [ ] Set VITE_API_URL to backend URL
- [ ] Update CORS_ORIGINS on backend
- [ ] Test the deployment
- [ ] Register first user
- [ ] Done! 🚀

## 🆘 Getting Help

If you encounter issues:
1. Check Railway logs
2. Review this guide
3. Check Railway Discord community
4. Review application logs in Railway dashboard

---

**Your app is now ready for Railway! 🚂**

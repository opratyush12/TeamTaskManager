# 🚂 Deploy to Railway - Step by Step

This is a simplified, step-by-step guide to deploy your Team Task Manager on Railway.

## Prerequisites
- ✅ Railway account (sign up at https://railway.app)
- ✅ GitHub account
- ✅ Code pushed to GitHub

## Step 1: Push to GitHub (5 minutes)

```bash
# Initialize git (if not already)
cd TeamTaskManager
git init

# Add all files
git add .

# Commit
git commit -m "Ready for Railway deployment"

# Create repo on GitHub
# Go to: https://github.com/new
# Create: team-task-manager

# Add remote and push
git remote add origin https://github.com/YOUR_USERNAME/team-task-manager.git
git branch -M main
git push -u origin main
```

## Step 2: Deploy Backend (10 minutes)

### 2.1 Create Project
1. Go to https://railway.app
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"**
4. Choose your `team-task-manager` repository

### 2.2 Configure Backend Service
Railway will auto-detect the configuration from `railway.json`

### 2.3 Add Environment Variables
Click on the service → **Variables** tab → Add these:

```
SECRET_KEY = [Generate with: openssl rand -hex 32]
DATABASE_URL = sqlite:////app/data/task_manager.db
ALGORITHM = HS256
ACCESS_TOKEN_EXPIRE_MINUTES = 30
REFRESH_TOKEN_EXPIRE_DAYS = 7
```

### 2.4 Add Volume (Important!)
1. Click **Settings** tab
2. Scroll to **Volumes**
3. Click **"+ New Volume"**
4. Mount path: `/app/data`
5. This persists your database!

### 2.5 Deploy
1. Click **Deploy** button
2. Wait for build to complete (3-5 minutes)
3. Copy the generated URL (e.g., `https://team-task-manager-production.railway.app`)

## Step 3: Deploy Frontend (10 minutes)

### 3.1 Create Frontend Service
1. In same project, click **"+ New"**
2. Select **"GitHub Repo"**
3. Choose same repository
4. Railway creates a second service

### 3.2 Configure Dockerfile
1. Click on the new service
2. Go to **Settings** tab
3. Find **Dockerfile Path**
4. Set to: `Dockerfile.frontend`

### 3.3 Add Environment Variable
Click **Variables** tab → Add:

```
VITE_API_URL = https://your-backend-url.railway.app
```
*(Use the URL you copied from Step 2.5)*

### 3.4 Deploy
1. Click **Deploy**
2. Wait for build (2-3 minutes)
3. Copy the frontend URL

### 3.5 Update Backend CORS
1. Go back to backend service
2. Click **Variables**
3. Add new variable:
```
CORS_ORIGINS = https://your-frontend-url.railway.app
```
4. Service will auto-restart

## Step 4: Test Your Deployment (5 minutes)

### 4.1 Access Your App
Open the frontend URL in your browser

### 4.2 Test Registration
1. Click **"Sign up"**
2. Fill in the form
3. Create account

### 4.3 Test Features
1. Create a team
2. Create a project
3. Create a task
4. Toggle theme

### 4.4 Verify Persistence
1. Create some data
2. Go to Railway backend service
3. Click **"Redeploy"**
4. Wait for redeploy
5. Open app again
6. Your data should still be there! ✅

## 🎉 Done! Your App is Live!

### Your URLs:
- **Frontend**: https://your-frontend.railway.app
- **Backend**: https://your-backend.railway.app
- **API Docs**: https://your-backend.railway.app/docs

## 📱 Share Your App

Share the frontend URL with others:
```
https://your-frontend.railway.app
```

They can register and start using it immediately!

## 🔧 Post-Deployment

### Monitor Your App
- Go to Railway dashboard
- Click on services to view logs
- Monitor CPU/RAM usage
- Check for errors

### Set Up Custom Domain (Optional)
1. Click on frontend service
2. Go to **Settings**
3. Click **"Generate Domain"** or **"Custom Domain"**
4. Follow instructions to add DNS records

### Enable Auto-Deploy
Already enabled! Every push to `main` branch auto-deploys.

## 💰 Free Tier Limits

Railway gives you **$5 credit per month** on the free tier.

This is enough for:
- Small backend (512MB RAM)
- Small frontend (512MB RAM)
- ~20-30 days of runtime

Estimated usage:
- **2 services × ~$0.15/day = $9/month** (might need Pro plan)

**Pro Plan**: $20/month for unlimited projects

## 🐛 Troubleshooting

### Backend not starting?
```bash
# Check logs in Railway dashboard
# Verify SECRET_KEY is set
# Check DATABASE_URL is correct
```

### Frontend not loading?
```bash
# Check VITE_API_URL is set correctly
# Verify backend URL is accessible
# Check browser console for errors
```

### Can't login?
```bash
# Check CORS_ORIGINS includes frontend URL
# Test backend API directly: https://your-backend.railway.app/docs
# Verify backend is running in Railway dashboard
```

### Database resets?
```bash
# Make sure volume is mounted at /app/data
# Go to backend service → Settings → Volumes
```

## 📊 Check Deployment Status

### Backend Health
Visit: `https://your-backend.railway.app/health`

Should return:
```json
{"status": "healthy"}
```

### Frontend
Visit: `https://your-frontend.railway.app`

Should show the login page

### API Docs
Visit: `https://your-backend.railway.app/docs`

Should show Swagger UI with all endpoints

## 🔄 Making Updates

### Update Code
```bash
# Make changes locally
git add .
git commit -m "Your update message"
git push

# Railway auto-deploys! ✨
```

### Update Environment Variables
1. Go to service in Railway
2. Click **Variables**
3. Add/update variable
4. Service auto-restarts

### Rollback
1. Click **Deployments** tab
2. Find previous deployment
3. Click **"..."** menu
4. Click **"Rollback"**

## 🎓 Next Steps

1. ✅ App is deployed
2. ✅ Database persists
3. ✅ Auto-deploy is enabled
4. Consider:
   - Add custom domain
   - Set up monitoring
   - Add more team members
   - Upgrade to Pro plan if needed

## 📚 Additional Help

- **Detailed Guide**: See `RAILWAY_DEPLOYMENT.md`
- **Docker Guide**: See `DOCKER_QUICK_START.md`
- **Full Docs**: See `FULL_PROJECT_GUIDE.md`
- **Railway Docs**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway

---

## 🎊 Congratulations!

Your Team Task Manager is now live on Railway!

**Time taken**: ~30 minutes
**Status**: ✅ Deployed and running
**Cost**: $5/month free credit (may need upgrade)

**Enjoy your deployed app! 🚀**

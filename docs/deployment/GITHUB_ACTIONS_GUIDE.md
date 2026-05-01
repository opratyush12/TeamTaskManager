# GitHub Actions CI/CD Guide

This guide explains the CI/CD pipeline configured for the Team Task Manager application.

## 📋 Overview

The project includes 4 automated workflows:

1. **Backend CI/CD** - Tests, builds, and deploys backend
2. **Frontend CI/CD** - Tests, builds, and deploys frontend
3. **Docker Compose CI** - Tests full Docker stack
4. **Code Quality** - Linting and security checks

## 🚀 Workflows

### 1. Backend CI/CD (`.github/workflows/backend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches (with backend changes)
- Pull requests to `main` or `develop`

**Jobs:**

#### Test
- Sets up Python 3.10
- Installs dependencies
- Runs flake8 linting
- Executes pytest with coverage

#### Build
- Builds Docker image using Buildx
- Caches layers for faster builds
- Runs only on push events

#### Deploy
- Deploys to Railway (main branch only)
- Requires `RAILWAY_TOKEN` secret

### 2. Frontend CI/CD (`.github/workflows/frontend-ci.yml`)

**Triggers:**
- Push to `main` or `develop` branches (with frontend changes)
- Pull requests to `main` or `develop`

**Jobs:**

#### Test
- Sets up Node.js 18
- Installs dependencies with npm ci
- Runs ESLint
- Builds production bundle
- Validates dist output

#### Build
- Builds Docker image with Nginx
- Caches layers
- Runs only on push events

#### Deploy
- Deploys to Railway (main branch only)
- Requires `RAILWAY_TOKEN` secret

### 3. Docker Compose CI (`.github/workflows/docker-compose-ci.yml`)

**Triggers:**
- Push/PR with docker configuration changes

**Jobs:**

#### Test Docker Compose
- Builds all images
- Starts services with docker-compose
- Waits for services to be healthy
- Tests backend API endpoint
- Tests frontend HTTP response
- Shows logs on failure

### 4. Code Quality (`.github/workflows/code-quality.yml`)

**Triggers:**
- All pull requests
- Push to main/develop

**Jobs:**

#### Code Quality Checks
- **Python**: Black formatting, isort imports, flake8 linting
- **Frontend**: ESLint
- **Security**: Safety check (Python), npm audit (Frontend)

## 🔐 Required Secrets

### Railway Deployment (Optional)

If you want automatic deployment to Railway:

1. Go to Railway dashboard
2. Generate a project token
3. Add to GitHub repository secrets:
   - Name: `RAILWAY_TOKEN`
   - Value: Your Railway project token

**To add secrets:**
1. Go to GitHub repository → Settings → Secrets and variables → Actions
2. Click "New repository secret"
3. Add `RAILWAY_TOKEN`

## 📦 Setup Instructions

### 1. Push to GitHub

```bash
# Initialize git (if not already done)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit with CI/CD"

# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Push to GitHub
git push -u origin main
```

### 2. Verify Workflows

After pushing:
1. Go to your GitHub repository
2. Click "Actions" tab
3. You should see workflows running
4. Click on any workflow to see details

### 3. Configure Railway Deployment (Optional)

If you want automatic deployment:

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login to Railway
railway login

# Link project
railway link

# Get project token
railway whoami

# Add token to GitHub secrets (manual step in GitHub UI)
```

## 🎯 Workflow Behavior

### Pull Requests
- ✅ Run all tests
- ✅ Build Docker images
- ✅ Check code quality
- ❌ No deployment

### Push to `develop`
- ✅ Run all tests
- ✅ Build Docker images
- ✅ Check code quality
- ❌ No deployment

### Push to `main`
- ✅ Run all tests
- ✅ Build Docker images
- ✅ Check code quality
- ✅ Deploy to Railway (if token configured)

## 🔍 Monitoring Builds

### View Workflow Status

**In GitHub:**
- Repository → Actions tab
- Click on workflow run to see details
- View logs for each job

**Status Badges:**

Add to README.md:

```markdown
![Backend CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/backend-ci.yml/badge.svg)
![Frontend CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/frontend-ci.yml/badge.svg)
![Docker CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-compose-ci.yml/badge.svg)
```

## 🐛 Troubleshooting

### Build Failures

**Python tests fail:**
- Check Python version (must be 3.10+)
- Verify all dependencies in requirements.txt
- Check SECRET_KEY is set in workflow

**Frontend build fails:**
- Check Node.js version (must be 18+)
- Verify package.json and package-lock.json
- Check for missing dependencies

**Docker build fails:**
- Verify Dockerfile paths are correct
- Check context in docker-compose.yml
- Review build logs for specific errors

### Deployment Failures

**Railway deployment fails:**
- Verify RAILWAY_TOKEN is set correctly
- Check Railway CLI version
- Ensure Railway project is linked
- Review Railway service configuration

**Service not starting:**
- Check environment variables
- Verify ports are correct
- Review service logs in Railway

## 🔧 Customization

### Adding New Tests

**Backend tests:**
Edit test files and they'll run automatically:
```python
# test_api.py
def test_new_endpoint():
    response = client.get("/new-endpoint")
    assert response.status_code == 200
```

**Frontend tests:**
Add test files in frontend:
```javascript
// frontend/src/__tests__/Component.test.jsx
import { render } from '@testing-library/react';
import Component from '../Component';

test('renders component', () => {
  render(<Component />);
});
```

### Modifying Triggers

Edit workflow files to change when they run:

```yaml
on:
  push:
    branches: [ main, develop, feature/* ]  # Add more branches
  schedule:
    - cron: '0 0 * * *'  # Run daily at midnight
```

### Adding New Jobs

Add to any workflow file:

```yaml
jobs:
  my-new-job:
    name: My Custom Job
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - name: Run custom script
        run: ./scripts/my-script.sh
```

## 📚 Best Practices

1. **Commit messages**: Use conventional commits (feat:, fix:, docs:, etc.)
2. **Branch protection**: Enable on main branch
   - Require PR reviews
   - Require status checks to pass
   - Require branches to be up to date
3. **Secrets**: Never commit secrets, use GitHub secrets
4. **Testing**: Write tests before pushing
5. **Docker cache**: Workflows use GitHub cache for faster builds

## 🔄 Workflow Updates

When modifying workflows:

1. Test locally first with Docker
2. Create feature branch
3. Push and create PR
4. Verify all checks pass
5. Merge to main

## 📊 Performance

**Typical run times:**
- Backend CI: ~2-3 minutes
- Frontend CI: ~3-4 minutes
- Docker Compose CI: ~5-7 minutes
- Code Quality: ~2 minutes

**Cache benefits:**
- First run: Full build time
- Subsequent runs: 50-70% faster with cache

## 🎉 Success Criteria

All workflows should:
- ✅ Pass all tests
- ✅ Build successfully
- ✅ Pass linting checks
- ✅ Deploy to Railway (main branch)
- ✅ Complete in under 10 minutes

---

**Need help?** Open an issue in the repository or check GitHub Actions documentation.

# Push to GitHub - Quick Guide

Your code is committed and ready to push! Follow these steps:

## 📋 Steps to Push

### 1. Create GitHub Repository

Go to https://github.com/new and create a new repository:
- **Name**: `team-task-manager` (or your preferred name)
- **Description**: Full-stack team task management app with FastAPI and React
- **Visibility**: Public or Private
- **DO NOT** initialize with README, .gitignore, or license (we already have these)

### 2. Add Remote and Push

Replace `YOUR_USERNAME` and `YOUR_REPO` with your GitHub username and repository name:

```bash
# Add remote
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git

# Rename branch to main (if needed)
git branch -M main

# Push to GitHub
git push -u origin main
```

**Example:**
```bash
git remote add origin https://github.com/johndoe/team-task-manager.git
git branch -M main
git push -u origin main
```

### 3. Verify Push

After pushing:
1. Refresh your GitHub repository page
2. You should see all files
3. Go to **Actions** tab to see CI/CD workflows running

## 🔧 Setup GitHub Actions (Optional Railway Deployment)

If you want automatic deployment to Railway:

### 1. Get Railway Token

```bash
# Install Railway CLI
npm install -g @railway/cli

# Login
railway login

# Get your project token
railway whoami
```

### 2. Add GitHub Secret

1. Go to your GitHub repository
2. Click **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Name: `RAILWAY_TOKEN`
5. Value: Your Railway project token
6. Click **Add secret**

## 📊 Add Status Badges (Optional)

Add these to the top of your README.md:

```markdown
![Backend CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/backend-ci.yml/badge.svg)
![Frontend CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/frontend-ci.yml/badge.svg)
![Docker CI](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/docker-compose-ci.yml/badge.svg)
![Code Quality](https://github.com/YOUR_USERNAME/YOUR_REPO/actions/workflows/code-quality.yml/badge.svg)
```

## 🎯 GitHub Actions Workflows

After pushing, these workflows will run automatically:

### ✅ On Push to Main/Develop:
- **Backend CI**: Tests, linting, builds Docker image, deploys to Railway
- **Frontend CI**: Tests, builds, Docker image, deploys to Railway
- **Docker Compose CI**: Tests full stack
- **Code Quality**: Linting and security checks

### ✅ On Pull Requests:
- All tests and builds run
- No deployment occurs

## 🔒 Branch Protection (Recommended)

Protect your main branch:

1. Go to **Settings** → **Branches**
2. Click **Add branch protection rule**
3. Branch name pattern: `main`
4. Enable:
   - ✅ Require a pull request before merging
   - ✅ Require status checks to pass before merging
   - ✅ Require branches to be up to date before merging
5. Select required status checks:
   - Backend CI / Test
   - Frontend CI / Test
   - Docker Compose CI
   - Code Quality
6. Save changes

## 🚀 Next Steps After Push

1. **Verify Actions**: Check Actions tab for workflow status
2. **Setup Railway** (if not done): Add `RAILWAY_TOKEN` secret
3. **Update README**: Add your GitHub badges
4. **Test Deployment**: Push a small change to test CI/CD
5. **Invite Collaborators**: Settings → Collaborators

## 🐛 Troubleshooting

### Push Rejected
```bash
# If you get "failed to push some refs"
git pull origin main --rebase
git push -u origin main
```

### Wrong Remote URL
```bash
# Check current remote
git remote -v

# Change remote URL
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
```

### Authentication Issues

**Using HTTPS:**
- You'll need a Personal Access Token (not password)
- Go to GitHub Settings → Developer settings → Personal access tokens → Tokens (classic)
- Generate new token with `repo` scope
- Use token as password when pushing

**Using SSH (recommended):**
```bash
# Change remote to SSH
git remote set-url origin git@github.com:YOUR_USERNAME/YOUR_REPO.git

# Generate SSH key (if you don't have one)
ssh-keygen -t ed25519 -C "your_email@example.com"

# Add key to GitHub
# Copy the public key
cat ~/.ssh/id_ed25519.pub

# Go to GitHub Settings → SSH and GPG keys → New SSH key
# Paste the key
```

## 📝 Commit Best Practices

For future commits:

```bash
# Make changes to files

# Stage changes
git add .

# Commit with descriptive message
git commit -m "feat: add user profile page"

# Push
git push
```

**Commit message conventions:**
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes (formatting)
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

## 🎉 Success!

Once pushed successfully:
- ✅ Code is on GitHub
- ✅ CI/CD workflows running
- ✅ Automatic deployment configured (if Railway token added)
- ✅ Team can collaborate

---

**Need help?** Check [GitHub Actions Guide](./GITHUB_ACTIONS_GUIDE.md) for more details.

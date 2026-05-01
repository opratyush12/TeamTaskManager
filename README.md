# 🚀 Team Task Manager

A modern, full-stack task management application with team collaboration, project organization, and comprehensive analytics.

![Tech Stack](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?style=for-the-badge&logo=docker&logoColor=white)

## ✨ Features

### 🔐 Authentication & Security
- JWT-based authentication with refresh tokens
- Password strength validation
- Role-based access control (RBAC)
- Secure password hashing with bcrypt

### 👥 Team Management
- Create and manage multiple teams
- Team roles: Owner, Manager, Member
- Add/remove team members
- Role-based permissions

### 📁 Project Organization
- Create projects within teams
- Status tracking (Active, Archived, Completed)
- Date range support
- Project overview and analytics

### ✅ Task Management
- Kanban-style task board
- Priority levels (Low, Medium, High, Urgent)
- Status workflow (Todo → In Progress → Review → Done)
- Task assignment to team members
- Due date tracking with overdue alerts
- Rich task filtering and search

### 📊 Dashboard & Analytics
- Real-time statistics and insights
- Task completion rate tracking
- Overdue task monitoring
- 7-day activity trends
- Priority and status distribution

### 🎨 Modern UI/UX
- Beautiful, responsive design
- Dark/Light theme toggle
- Smooth animations and transitions
- Intuitive navigation
- Mobile-friendly interface

---

## 📁 Project Structure

```
TeamTaskManager/
├── app/                    # Backend (FastAPI)
│   ├── api/               # API endpoints
│   ├── models/            # Database models
│   ├── schemas/           # Pydantic schemas
│   ├── services/          # Business logic
│   └── utils/             # Utilities (auth, RBAC)
│
├── frontend/              # Frontend (React + Vite)
│   └── src/
│       ├── components/    # React components
│       ├── context/       # State management
│       ├── services/      # API client
│       └── assets/        # Static assets
│
├── docker/                # Docker configuration
│   ├── backend/          # Backend Dockerfile
│   ├── frontend/         # Frontend Dockerfile + Nginx
│   └── docker-compose.yml # Multi-service setup
│
├── docs/                  # Documentation
│   ├── deployment/       # Deployment guides
│   ├── guides/           # User guides
│   └── api/              # API documentation
│
├── scripts/               # Helper scripts
│   └── docker-build.sh   # Docker operations
│
├── config/                # Configuration files
│   ├── railway.json      # Railway config
│   ├── railway.toml      # Alternative Railway config
│   └── .env.example      # Environment template
│
├── requirements.txt       # Python dependencies
└── README.md             # This file
```

---

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+**
- **Docker & Docker Compose** (for containerized deployment)

### Local Development

#### 1. Backend Setup

```bash
# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp config/.env.example .env

# Edit .env and set SECRET_KEY
# Generate: openssl rand -hex 32

# Initialize database
python -c "from app.database import init_db; init_db()"

# Start backend server
python -m uvicorn app.main:app --reload --port 8000
```

**Backend running at**: http://localhost:8000  
**API Docs**: http://localhost:8000/docs

#### 2. Frontend Setup

```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

**Frontend running at**: http://localhost:3000

### Using Docker Compose

```bash
# Generate secret key
export SECRET_KEY=$(openssl rand -hex 32)

# Start all services
docker-compose -f docker/docker-compose.yml up -d

# View logs
docker-compose -f docker/docker-compose.yml logs -f

# Stop services
docker-compose -f docker/docker-compose.yml down
```

**Access**:
- Frontend: http://localhost
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

---

## 📚 Documentation

### Getting Started
- **[Quick Start Guide](docs/guides/START_HERE.md)** - First-time user guide
- **[Full Project Guide](docs/guides/FULL_PROJECT_GUIDE.md)** - Complete documentation

### Deployment
- **[Deploy to Railway](docs/deployment/DEPLOY_TO_RAILWAY.md)** - 30-minute deployment guide
- **[Railway Deployment](docs/deployment/RAILWAY_DEPLOYMENT.md)** - Detailed Railway guide
- **[Docker Quick Start](docs/deployment/DOCKER_QUICK_START.md)** - Docker commands reference
- **[Deployment Summary](docs/deployment/DEPLOYMENT_SUMMARY.md)** - Overview of all options

### API Documentation
- **Interactive Docs**: http://localhost:8000/docs (when running)
- **ReDoc**: http://localhost:8000/redoc

---

## 🐳 Docker

### Build Images

```bash
# Backend
docker build -f docker/backend/Dockerfile -t taskmanager-backend .

# Frontend
docker build -f docker/frontend/Dockerfile -t taskmanager-frontend .
```

### Run Containers

```bash
# Backend
docker run -d -p 8000:8000 \
  -e SECRET_KEY=your-secret-key \
  --name taskmanager-backend \
  taskmanager-backend

# Frontend
docker run -d -p 80:80 \
  --name taskmanager-frontend \
  taskmanager-frontend
```

### Helper Script

```bash
# Make script executable (Linux/Mac)
chmod +x scripts/docker-build.sh

# Build both images
./scripts/docker-build.sh build

# Start services
./scripts/docker-build.sh up

# View logs
./scripts/docker-build.sh logs

# Stop services
./scripts/docker-build.sh down
```

---

## 🚂 Deploy to Railway

Railway provides a simple way to deploy your application to production.

### Quick Deploy (3 Steps)

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin YOUR_GITHUB_REPO
   git push -u origin main
   ```

2. **Deploy Backend**
   - Go to https://railway.app
   - New Project → Deploy from GitHub
   - Add environment variables
   - Add volume: `/app/data`

3. **Deploy Frontend**
   - Add new service in same project
   - Set Dockerfile path: `docker/frontend/Dockerfile`
   - Add `VITE_API_URL` with backend URL

**Detailed Guide**: [docs/deployment/DEPLOY_TO_RAILWAY.md](docs/deployment/DEPLOY_TO_RAILWAY.md)

---

## 🔧 Configuration

### Environment Variables

#### Backend (`/.env`)
```env
SECRET_KEY=your-32-char-secret-here
DATABASE_URL=sqlite:///./task_manager.db
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

Generate SECRET_KEY:
```bash
openssl rand -hex 32
```

#### Frontend (`/frontend/.env.production`)
```env
VITE_API_URL=https://your-backend-url.com
```

---

## 🧪 Testing

### Backend API Testing

```bash
# Run the test script
python test_api.py
```

### Manual Testing

1. Start both backend and frontend
2. Register a new account
3. Create a team
4. Create a project
5. Create tasks
6. Test all features

### Using API Docs

Visit http://localhost:8000/docs for interactive API testing.

---

## 🛠️ Tech Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - SQL toolkit and ORM
- **SQLite** - Database (easily switchable to PostgreSQL)
- **Pydantic** - Data validation
- **JWT** - Authentication
- **Bcrypt** - Password hashing
- **Alembic** - Database migrations

### Frontend
- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Icons** - Icon library
- **date-fns** - Date formatting

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **Nginx** - Web server (production frontend)
- **Railway** - Deployment platform

---

## 📊 Database Schema

### Core Models

- **Users** - System users with roles (Admin, Manager, Member)
- **Teams** - Team organization with many-to-many user relationships
- **TeamMembers** - Team membership with roles (Owner, Manager, Member)
- **Projects** - Project entities belonging to teams
- **Tasks** - Individual tasks with status, priority, and assignments

### Relationships

- Users ↔ Teams (Many-to-Many through TeamMembers)
- Teams → Projects (One-to-Many)
- Projects → Tasks (One-to-Many)
- Users → Tasks (One-to-Many as creator and assignee)

---

## 🎨 Features in Detail

### Authentication Flow
1. User registers with email and password
2. Password is validated and hashed
3. JWT tokens (access + refresh) are generated
4. Access token expires in 30 minutes
5. Refresh token valid for 7 days
6. Auto-refresh on token expiry

### RBAC Implementation
- **System Level**: Admin, Manager, Member
- **Team Level**: Owner, Manager, Member
- Granular permissions for each action
- Dynamic permission checking

### Task Workflow
```
Todo → In Progress → Review → Done
```
Each status change is tracked with timestamps.

### Priority Levels
- **Low** - Non-urgent tasks
- **Medium** - Regular priority
- **High** - Important tasks
- **Urgent** - Critical, time-sensitive tasks

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

### Coding Standards

- **Backend**: Follow PEP 8, use type hints
- **Frontend**: Use functional components with hooks
- **Components**: Keep them small and focused
- **Documentation**: Update docs for new features

---

## 🐛 Troubleshooting

### Common Issues

**Backend won't start**
- Check Python version (3.10+)
- Verify all dependencies installed
- Check `.env` file exists and SECRET_KEY is set
- Ensure port 8000 is not in use

**Frontend won't start**
- Check Node.js version (18+)
- Run `npm install` in frontend directory
- Verify port 3000 is available
- Check console for build errors

**Database issues**
- Delete `task_manager.db` and reinitialize
- Check file permissions
- Verify SQLite is installed

**Docker issues**
- Check Docker is running
- Verify docker-compose.yml paths
- Check logs: `docker-compose logs`
- Try rebuilding: `docker-compose up --build`

**More Help**: Check [docs/guides/FULL_PROJECT_GUIDE.md](docs/guides/FULL_PROJECT_GUIDE.md)

---

## 📈 Roadmap

### Planned Features
- [ ] Real-time updates with WebSockets
- [ ] Email notifications
- [ ] File attachments for tasks
- [ ] Comments and activity log
- [ ] Advanced search and filtering
- [ ] Gantt chart view
- [ ] Time tracking
- [ ] Export to PDF/Excel
- [ ] Mobile apps (React Native)
- [ ] Third-party integrations (Slack, Teams)

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🌟 Acknowledgments

- FastAPI for the amazing Python framework
- React team for the UI library
- Tailwind CSS for the styling system
- Railway for easy deployment
- All open-source contributors

---

## 📞 Support

- **Documentation**: Check the `docs/` folder
- **Issues**: Open an issue on GitHub
- **Discussions**: Use GitHub Discussions

---

## 🎉 Getting Started

Choose your path:

1. **Local Development**: Follow the [Quick Start](#-quick-start) above
2. **Docker**: Use [Docker Compose](#using-docker-compose)
3. **Production**: Deploy to [Railway](#-deploy-to-railway)

**Ready to go? Start with**: [docs/guides/START_HERE.md](docs/guides/START_HERE.md)

---

**Built with ❤️ using FastAPI, React, and Tailwind CSS**

# Team Task Manager - Complete Project Guide

## 🎉 Project Overview

A full-stack task management application with modern UI, featuring teams, projects, tasks, and comprehensive analytics.

## 🏗️ Architecture

### Backend (FastAPI + SQLite)
- **Location**: `./app/`
- **Server**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

### Frontend (React + Tailwind CSS)
- **Location**: `./frontend/`
- **Dev Server**: http://localhost:3000
- **Build Tool**: Vite

## ✨ Features

### 🔐 Authentication
- JWT-based authentication with access & refresh tokens
- Password strength validation
- Auto-login after registration
- Persistent sessions

### 👥 Team Management
- Create and manage teams
- Add/remove team members
- Role-based permissions (Owner, Manager, Member)
- Team overview with member count

### 📁 Project Management
- Create projects within teams
- Status tracking (Active, Archived, Completed)
- Date range support
- Team association

### ✅ Task Management
- Kanban-style task board
- Priority levels (Low, Medium, High, Urgent)
- Status workflow (Todo → In Progress → Review → Done)
- Task assignment to team members
- Due date tracking with overdue alerts
- Task filtering and search

### 📊 Dashboard
- Real-time statistics
- Task completion rate
- My tasks, team tasks, and overdue tasks
- 7-day activity trends
- Priority and status distribution

### 🌓 Theme Support
- Light and dark modes
- Smooth transitions
- Persistent preference
- System theme detection

## 🚀 Quick Start

### Backend Setup

1. **Install Python dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set environment variables:**
```bash
cp .env.example .env
# Edit .env with your SECRET_KEY
```

3. **Initialize database:**
```bash
python -c "from app.database import init_db; init_db()"
```

4. **Start backend server:**
```bash
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

### Frontend Setup

1. **Install Node dependencies:**
```bash
cd frontend
npm install
```

2. **Start development server:**
```bash
npm run dev
```

3. **Open browser:**
Navigate to http://localhost:3000

## 📁 Project Structure

```
TeamTaskManager/
├── app/                      # Backend (FastAPI)
│   ├── api/                 # API endpoints
│   │   ├── auth.py          # Authentication
│   │   ├── users.py         # User management
│   │   ├── teams.py         # Team management
│   │   ├── projects.py      # Project management
│   │   ├── tasks.py         # Task management
│   │   └── dashboard.py     # Dashboard analytics
│   ├── models/              # Database models
│   │   ├── user.py          # User model
│   │   ├── team.py          # Team & TeamMember models
│   │   ├── project.py       # Project model
│   │   └── task.py          # Task model
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py          # Auth schemas
│   │   ├── user.py          # User schemas
│   │   ├── team.py          # Team schemas
│   │   ├── project.py       # Project schemas
│   │   ├── task.py          # Task schemas
│   │   └── dashboard.py     # Dashboard schemas
│   ├── services/            # Business logic
│   │   ├── auth_service.py
│   │   ├── team_service.py
│   │   ├── project_service.py
│   │   ├── task_service.py
│   │   └── dashboard_service.py
│   ├── utils/               # Utilities
│   │   ├── security.py      # JWT & password hashing
│   │   └── rbac.py          # Role-based access control
│   ├── config.py            # Configuration
│   ├── database.py          # Database setup
│   ├── dependencies.py      # Auth dependencies
│   └── main.py              # FastAPI app
├── frontend/                 # Frontend (React)
│   ├── src/
│   │   ├── components/
│   │   │   ├── auth/        # Login & Register
│   │   │   ├── layout/      # Navbar, Sidebar, Layout
│   │   │   ├── dashboard/   # Dashboard widgets
│   │   │   ├── teams/       # Team management UI
│   │   │   ├── projects/    # Project management UI
│   │   │   ├── tasks/       # Task management UI
│   │   │   └── common/      # Reusable components
│   │   ├── context/         # React Context
│   │   │   ├── AuthContext.jsx
│   │   │   └── ThemeContext.jsx
│   │   ├── services/
│   │   │   └── api.js       # API client
│   │   ├── App.jsx          # Main app
│   │   ├── main.jsx         # Entry point
│   │   └── index.css        # Global styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── requirements.txt
├── .env.example
└── README.md
```

## 🎨 UI Components

### Common Components
- **Button**: Multiple variants (primary, secondary, outline, danger, ghost)
- **Modal**: Animated modals with sizes (sm, md, lg, xl)
- **Input**: With icons, validation, and error messages
- **Select**: Dropdown with custom styling
- **LoadingSpinner**: Full-screen or inline

### Layout Components
- **Navbar**: User info, theme toggle, logout
- **Sidebar**: Navigation menu with active states
- **Layout**: Main app layout wrapper

### Feature Components
- **Dashboard**: Stats cards, task lists, analytics
- **Teams**: Team cards, create team modal
- **Projects**: Project cards, create project modal
- **Tasks**: Kanban board, create task modal

## 🎯 Color Scheme

### Primary Colors (Blue)
- 50-900: Shades for primary actions
- Used for: Buttons, links, active states

### Status Colors
- **Gray**: Todo, Inactive
- **Blue**: In Progress, Info
- **Purple**: Review
- **Green**: Done, Success
- **Orange**: High priority
- **Red**: Urgent, Errors

### Priority Colors
- **Low**: Gray
- **Medium**: Blue
- **High**: Orange
- **Urgent**: Red

## 🔒 Security Features

### Backend
- JWT token authentication
- Password hashing with bcrypt (12 rounds)
- Password strength validation
- SQL injection prevention (SQLAlchemy ORM)
- CORS configuration
- Role-based access control (RBAC)
- Input validation with Pydantic

### Frontend
- Secure token storage (localStorage)
- Auto token refresh on expiry
- Protected routes
- Input sanitization
- XSS prevention

## 📊 Database Schema

### Users
- System-level roles: Admin, Manager, Member
- Email & username unique
- Password hashed
- Timestamps

### Teams
- Many-to-many with Users
- Team roles: Owner, Manager, Member
- Cascade delete team members

### Projects
- Belongs to Team
- Status: Active, Archived, Completed
- Date range support

### Tasks
- Belongs to Project
- Assigned to User (optional)
- Priority: Low, Medium, High, Urgent
- Status: Todo, In Progress, Review, Done
- Due date tracking

## 🚦 API Endpoints

### Authentication
- `POST /auth/register` - Register user
- `POST /auth/login` - Login
- `POST /auth/refresh` - Refresh token
- `GET /auth/me` - Current user

### Teams
- `GET /teams` - List teams
- `POST /teams` - Create team
- `GET /teams/{id}` - Get team
- `PUT /teams/{id}` - Update team
- `DELETE /teams/{id}` - Delete team
- `POST /teams/{id}/members` - Add member
- `DELETE /teams/{id}/members/{user_id}` - Remove member

### Projects
- `GET /projects` - List projects
- `POST /projects` - Create project
- `GET /projects/{id}` - Get project
- `PUT /projects/{id}` - Update project
- `DELETE /projects/{id}` - Delete project

### Tasks
- `GET /tasks` - List tasks (with filters)
- `POST /tasks` - Create task
- `GET /tasks/{id}` - Get task
- `PUT /tasks/{id}` - Update task
- `PUT /tasks/{id}/status` - Update status
- `PUT /tasks/{id}/assign` - Assign task
- `DELETE /tasks/{id}` - Delete task

### Dashboard
- `GET /dashboard/overview` - Stats overview
- `GET /dashboard/tasks` - Task aggregation
- `GET /dashboard/stats` - Analytics

## 🎭 Animations & Transitions

### Page Transitions
- Fade in on mount
- Slide up for cards
- Scale in for modals

### Hover Effects
- Card lift on hover
- Button scale
- Smooth color transitions

### Loading States
- Spinner animations
- Skeleton screens (can be added)
- Progressive loading

## 🧪 Testing

### Backend Testing
```bash
# Run with test data
python test_api.py
```

### Frontend Testing (Manual)
1. Register new user
2. Create a team
3. Add team members
4. Create a project
5. Create tasks
6. Assign tasks
7. Update task status
8. View dashboard
9. Toggle theme

## 📱 Responsive Design

- Mobile-first approach
- Breakpoints: sm (640px), md (768px), lg (1024px), xl (1280px)
- Grid layouts adapt to screen size
- Touch-friendly buttons and cards
- Collapsible sidebar (can be added)

## 🔧 Customization

### Theme Colors
Edit `frontend/tailwind.config.js`:
```js
colors: {
  primary: {
    // Custom color palette
  }
}
```

### Animation Speed
Edit `frontend/tailwind.config.js`:
```js
animation: {
  'slide-up': 'slideUp 0.3s ease-out', // Adjust duration
}
```

### API Base URL
Edit `frontend/src/services/api.js`:
```js
const API_URL = '/api'; // Change for production
```

## 🐛 Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Kill process on port 8000
taskkill /F /IM python.exe
# Or use different port
uvicorn app.main:app --port 8001
```

**Database locked:**
```bash
# Remove database and reinitialize
rm task_manager.db
python -c "from app.database import init_db; init_db()"
```

### Frontend Issues

**Dependencies not installing:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Port 3000 in use:**
Edit `vite.config.js`:
```js
server: {
  port: 3001 // Use different port
}
```

**API connection failed:**
- Check backend is running on port 8000
- Verify proxy in `vite.config.js`
- Check CORS settings in backend

## 📈 Future Enhancements

- [ ] Real-time updates with WebSockets
- [ ] Email notifications
- [ ] File attachments for tasks
- [ ] Comments and activity log
- [ ] Advanced filtering and search
- [ ] Gantt chart view
- [ ] Time tracking
- [ ] Export to PDF/Excel
- [ ] Mobile apps (React Native)
- [ ] Integration with Slack/Teams

## 🤝 Contributing

1. Fork the repository
2. Create feature branch
3. Make changes
4. Test thoroughly
5. Submit pull request

## 📄 License

MIT License - Feel free to use for personal or commercial projects

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Framer Motion](https://www.framer.com/motion/)

## 💡 Tips

1. **Development**: Use `--reload` flag for auto-restart
2. **Production**: Build frontend with `npm run build`
3. **Security**: Always use HTTPS in production
4. **Performance**: Enable caching for API responses
5. **Monitoring**: Add logging and error tracking
6. **Backup**: Regular database backups

## 📞 Support

For issues and questions:
- Check the documentation
- Review the code comments
- Test with the provided examples
- Search for similar issues

---

**Built with ❤️ using FastAPI, React, and Tailwind CSS**

# Task Manager Frontend

Modern, responsive React frontend for the Team Task Manager application.

## Features

- 🎨 **Modern UI**: Clean, intuitive interface with Tailwind CSS
- 🌓 **Dark/Light Theme**: Toggle between themes for user comfort
- ✨ **Smooth Animations**: Framer Motion animations and transitions
- 📱 **Responsive**: Works seamlessly on all devices
- 🔒 **Secure Authentication**: JWT-based auth with auto-refresh
- 📊 **Interactive Dashboard**: Real-time stats and task overview
- 👥 **Team Management**: Create and manage teams with role-based access
- 📁 **Project Organization**: Organize work within teams
- ✅ **Task Tracking**: Kanban-style task board with drag-and-drop
- 🎯 **Priority & Status**: Color-coded priorities and statuses

## Tech Stack

- **React 18** - UI library
- **Vite** - Build tool and dev server
- **Tailwind CSS** - Utility-first styling
- **Framer Motion** - Animations
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **React Icons** - Icon library
- **date-fns** - Date formatting

## Getting Started

### Prerequisites

- Node.js 16+ installed
- Backend server running on http://localhost:8000

### Installation

1. Install dependencies:
```bash
npm install
```

2. Start the development server:
```bash
npm run dev
```

3. Open http://localhost:3000 in your browser

### Build for Production

```bash
npm run build
npm run preview
```

## Project Structure

```
src/
├── components/
│   ├── auth/           # Login and registration
│   ├── layout/         # Navbar, Sidebar, Layout
│   ├── dashboard/      # Dashboard widgets
│   ├── teams/          # Team management
│   ├── projects/       # Project management
│   ├── tasks/          # Task management
│   └── common/         # Reusable components
├── context/            # React Context providers
│   ├── AuthContext.jsx # Authentication state
│   └── ThemeContext.jsx # Theme management
├── services/           # API services
│   └── api.js          # API client and endpoints
├── App.jsx             # Main app component
└── main.jsx            # Entry point
```

## Features in Detail

### Authentication
- Secure login and registration
- JWT token management with auto-refresh
- Protected routes
- Persistent sessions

### Dashboard
- Task statistics overview
- My tasks, team tasks, and overdue tasks
- Visual indicators for task status and priority
- Completion rate tracking

### Teams
- Create and manage teams
- Add/remove team members
- Role-based permissions (Owner, Manager, Member)
- Team overview cards

### Projects
- Create projects within teams
- Project status tracking (Active, Archived, Completed)
- Project cards with metadata
- Team association

### Tasks
- Kanban-style task board
- Create tasks with title, description, priority, and due date
- Assign tasks to team members
- Status workflow: Todo → In Progress → Review → Done
- Priority levels: Low, Medium, High, Urgent
- Due date tracking
- Filter and search tasks

### Theme Support
- Light and dark modes
- Smooth transitions between themes
- Persistent theme preference
- System preference detection

## API Integration

The frontend communicates with the backend API through axios:

- Automatic token injection in headers
- Token refresh on 401 errors
- Error handling and retry logic
- Request/response interceptors

## Customization

### Colors

Edit `tailwind.config.js` to customize the color scheme:

```js
theme: {
  extend: {
    colors: {
      primary: {
        // Your custom colors
      }
    }
  }
}
```

### Animations

Animations are defined in `tailwind.config.js` and can be customized:

```js
animation: {
  'slide-up': 'slideUp 0.3s ease-out',
  // Add your custom animations
}
```

## Troubleshooting

### Backend Connection Issues

If you're having trouble connecting to the backend:

1. Ensure backend is running on http://localhost:8000
2. Check CORS settings in backend
3. Verify proxy configuration in `vite.config.js`

### Token Expired

If you're logged out unexpectedly:

1. Check backend token expiration settings
2. Verify refresh token logic in `api.js`
3. Clear localStorage and try logging in again

## Contributing

1. Follow the existing code style
2. Use functional components with hooks
3. Keep components small and focused
4. Add proper TypeScript types (if converting to TS)
5. Test on both themes (light/dark)

## License

MIT

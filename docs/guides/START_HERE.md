# 🚀 Team Task Manager - Quick Start Guide

## ✅ Application is Running!

### 🌐 Access Points

**Frontend Application (Main UI)**
- URL: http://localhost:3000
- Click to open: [Launch Application](http://localhost:3000)

**Backend API Documentation**
- URL: http://localhost:8000/docs
- Interactive Swagger UI with all endpoints
- Click to open: [API Docs](http://localhost:8000/docs)

**Backend Health Check**
- URL: http://localhost:8000/health
- Status: ✅ Healthy

---

## 📝 Getting Started (First Time Users)

### Step 1: Register Your Account
1. Open http://localhost:3000 in your browser
2. You'll see the login page with a beautiful gradient background
3. Click **"Sign up"** at the bottom
4. Fill in the registration form:
   - Full Name: Your name
   - Username: Choose a username (min 3 chars)
   - Email: Your email address
   - Password: Strong password (min 8 chars, must include uppercase, lowercase, and digit)
   - Confirm Password: Re-enter password
5. Click **"Create Account"**
6. You'll be automatically logged in and redirected to the dashboard

### Step 2: Explore the Dashboard
After logging in, you'll see:
- **Stats Cards**: Total tasks, your tasks, overdue tasks, completion rate
- **My Tasks**: Your assigned tasks
- **Overdue Tasks**: Tasks that need attention
- **Recent Team Tasks**: Latest team activity

### Step 3: Create Your First Team
1. Click **"Teams"** in the sidebar (left menu)
2. Click the **"Create Team"** button (top right)
3. Enter team name and description
4. Click **"Create Team"**
5. Your team card will appear with member count

### Step 4: Create a Project
1. Click **"Projects"** in the sidebar
2. Click **"Create Project"**
3. Select your team from the dropdown
4. Enter project name and description
5. Click **"Create Project"**
6. Project card appears with status badge

### Step 5: Create Tasks
1. Click **"Tasks"** in the sidebar
2. You'll see a Kanban-style board with 4 columns:
   - Todo
   - In Progress
   - Review
   - Done
3. Click **"Create Task"**
4. Fill in task details:
   - Title: Task name
   - Description: Details
   - Project: Select from dropdown
   - Priority: Low, Medium, High, or Urgent
   - Due Date: Optional deadline
5. Click **"Create Task"**
6. Task appears in the "Todo" column

---

## 🎨 UI Features to Try

### Theme Toggle
- Look for the sun/moon icon in the top navbar
- Click to switch between light and dark mode
- Your preference is saved automatically

### Navigation
- Use the sidebar to navigate between sections
- Active page is highlighted with color
- Smooth transitions between pages

### Animations
- Watch cards animate when they appear
- Hover over cards to see lift effects
- Modals have smooth scale animations
- Buttons have press animations

### Task Management
- Click on any task to view details
- Color-coded priorities:
  - Gray: Low
  - Blue: Medium
  - Orange: High
  - Red: Urgent
- Status badges show current state

---

## 🎯 Sample Workflow

Here's a complete workflow to try:

1. **Register** → Create account
2. **Create Team** → "Engineering Team"
3. **Add Project** → "Website Redesign" in Engineering Team
4. **Create Tasks**:
   - "Design homepage" (High priority, due in 1 week)
   - "Setup development environment" (Medium, due in 2 days)
   - "Write documentation" (Low, due in 3 weeks)
5. **Assign Tasks** → Assign to yourself
6. **Update Status** → Move tasks through the workflow
7. **View Dashboard** → See your progress and stats
8. **Toggle Theme** → Try dark mode!

---

## 🔥 Cool Features to Explore

### Dashboard Statistics
- Real-time task counts
- Completion rate calculation
- 7-day activity trends
- Priority distribution

### Color-Coded Elements
- **Status Colors**:
  - Gray: Todo/Inactive
  - Blue: In Progress
  - Purple: Review
  - Green: Done/Complete
- **Priority Colors**:
  - As listed above

### Responsive Design
- Resize your browser window
- Layout adapts automatically
- Mobile-friendly interface

### Smooth Animations
- Page load animations
- Card hover effects
- Modal transitions
- Button press feedback

---

## 🛠️ Quick Commands

### If Servers Stop
Backend:
```bash
cd TeamTaskManager
python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

Frontend:
```bash
cd TeamTaskManager/frontend
npm run dev
```

### Check Server Status
```bash
# Backend
curl http://localhost:8000/health

# Frontend
curl http://localhost:3000
```

---

## 📱 Browser Recommendations

Best experience on:
- ✅ Chrome/Chromium (Recommended)
- ✅ Firefox
- ✅ Edge
- ✅ Safari

---

## 🎓 Tips for Best Experience

1. **Use Dark Mode**: Easier on the eyes, looks modern
2. **Create Multiple Teams**: Test team management
3. **Try All Priority Levels**: See the color coding
4. **Set Due Dates**: Watch overdue alerts
5. **Hover Over Elements**: Discover interactive animations
6. **Resize Window**: Test responsive design

---

## 🐛 Troubleshooting

**Can't access http://localhost:3000?**
- Check if frontend server is running
- Try refreshing the page
- Clear browser cache (Ctrl+Shift+R)

**Login not working?**
- Check if backend is running (http://localhost:8000/health)
- Verify you're using the correct email and password
- Password must meet requirements (8+ chars, uppercase, lowercase, digit)

**Page is blank?**
- Open browser console (F12)
- Check for errors
- Ensure both servers are running

**Need help?**
- Check `FULL_PROJECT_GUIDE.md` for detailed documentation
- Review `README.md` files in backend and frontend directories

---

## 🎉 You're All Set!

Open http://localhost:3000 and start exploring your new task management application!

**Have fun managing your tasks! 🚀**

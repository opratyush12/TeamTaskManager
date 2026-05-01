# New Features - Team Task Manager

## ✨ Recently Added Features

### 1. 📧 Add Team Members by Email

**What Changed:**
- Previously, you could only add team members by their user ID
- Now you can add members using their email address

**API Usage:**
```json
POST /teams/{team_id}/members
{
  "email": "user@example.com",
  "role": "member"
}
```

**Or using user_id:**
```json
{
  "user_id": "user-uuid",
  "role": "manager"
}
```

---

### 2. 🔔 In-App Notification System

**Features:**
- Real-time notifications for all important events
- Unread notification counter
- Mark as read/unread functionality
- Delete notifications
- Notification types:
  - Task assigned
  - Task completed
  - Team invitation
  - Team removed
  - Project created
  - Deadline approaching
  - Task overdue

**API Endpoints:**

**Get all notifications:**
```http
GET /notifications
GET /notifications?unread_only=true
```

**Get unread count:**
```http
GET /notifications/unread-count
Response: {"unread_count": 5}
```

**Mark as read:**
```http
PUT /notifications/mark-read
{
  "notification_ids": ["id1", "id2", "id3"]
}
```

**Mark all as read:**
```http
PUT /notifications/mark-all-read
```

**Delete notification:**
```http
DELETE /notifications/{notification_id}
```

**Notification Response:**
```json
{
  "id": "notif-uuid",
  "type": "task_assigned",
  "title": "New Task Assigned",
  "message": "John assigned you a task: Fix login bug",
  "link": "/tasks/task-123",
  "is_read": false,
  "created_at": "2026-05-01T10:30:00",
  "data": "{\"task_id\": \"task-123\", \"assigner\": \"John\"}"
}
```

---

### 3. ✅ Accept/Reject Task Assignments

**What Changed:**
- Tasks now have `assignment_status` field
- Users can accept or reject task assignments
- Rejected tasks get unassigned

**Assignment Status:**
- `pending` - Task assigned, waiting for acceptance
- `accepted` - User accepted the task
- `rejected` - User rejected the task

**API Endpoints:**

**Accept task:**
```http
PUT /tasks/{task_id}/accept
```
- Sets `assignment_status` to `accepted`
- Changes task status to `in_progress`
- Only the assigned user can accept

**Reject task:**
```http
PUT /tasks/{task_id}/reject
```
- Sets `assignment_status` to `rejected`
- Unassigns the task (`assigned_to` becomes null)
- Only the assigned user can reject

---

### 4. ✔️ Quick Complete Task Button

**What Changed:**
- New endpoint to quickly mark tasks as done
- Automatically sets completion timestamp
- Sends notification to task creator

**API Endpoint:**
```http
PUT /tasks/{task_id}/complete
```

**What it does:**
- Sets task `status` to `done`
- Sets `completed_at` to current timestamp
- Notifies task creator (if different from completer)

**Permissions:**
- Assigned user can complete
- Task creator can complete
- Team managers can complete

---

### 5. 🔢 Sort Tasks by Priority and Deadline

**What Changed:**
- Added sorting parameters to task listing
- Sort by priority, due date, or created date
- Ascending or descending order

**API Usage:**

**Sort by priority:**
```http
GET /tasks?sort_by=priority&sort_order=desc
```
Order: Urgent → High → Medium → Low

**Sort by deadline:**
```http
GET /tasks?sort_by=due_date&sort_order=asc
```
Shows nearest deadlines first (nulls last)

**Sort by creation date:**
```http
GET /tasks?sort_by=created_at&sort_order=desc
```
Shows newest tasks first

**Combine with filters:**
```http
GET /tasks?status=todo&sort_by=priority&sort_order=desc
```

---

## 🔄 Updated Database Schema

### Notifications Table
```sql
CREATE TABLE notifications (
    id VARCHAR PRIMARY KEY,
    user_id VARCHAR NOT NULL,
    type VARCHAR NOT NULL, -- enum
    title VARCHAR(200) NOT NULL,
    message TEXT NOT NULL,
    link VARCHAR(500),
    is_read BOOLEAN DEFAULT FALSE,
    data TEXT, -- JSON string
    created_at DATETIME,
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

### Tasks Table Updates
```sql
ALTER TABLE tasks ADD COLUMN assignment_status VARCHAR;
-- Values: pending, accepted, rejected
```

---

## 📱 Frontend Integration Guide

### Notification Bell Component

```javascript
// Get unread count
const { data } = await api.get('/notifications/unread-count');
// Display badge with data.unread_count

// Get notifications
const notifications = await api.get('/notifications?unread_only=true');

// Mark as read
await api.put('/notifications/mark-read', {
  notification_ids: ['id1', 'id2']
});
```

### Task Assignment Workflow

```javascript
// When user receives task assignment notification
// Show accept/reject buttons

// Accept task
await api.put(`/tasks/${taskId}/accept`);

// Reject task
await api.put(`/tasks/${taskId}/reject`);
```

### Complete Task Button

```javascript
// Add button in task view
<button onClick={() => completeTask(taskId)}>
  Mark Complete
</button>

async function completeTask(taskId) {
  await api.put(`/tasks/${taskId}/complete`);
  // Refresh task list
}
```

### Task Sorting

```javascript
// Add sort dropdown
<select onChange={(e) => setSortBy(e.target.value)}>
  <option value="created_at">Date Created</option>
  <option value="priority">Priority</option>
  <option value="due_date">Deadline</option>
</select>

// Fetch with sorting
const tasks = await api.get(`/tasks?sort_by=${sortBy}&sort_order=desc`);
```

---

## 🚀 Deployment Notes

### Database Migration

After deploying, the database will auto-create new tables/columns on first run:
- `notifications` table
- `tasks.assignment_status` column

**No manual migration needed** - SQLAlchemy handles it automatically.

### Backend Deployment

1. **Render:**
   - Redeploy backend service
   - New endpoints will be available immediately

2. **Railway:**
   - Push to GitHub
   - Auto-deploy if CI/CD configured

### Frontend Updates

Update `src/services/api.js` with new endpoints:

```javascript
// Notifications API
export const notificationsAPI = {
  getAll: (unreadOnly = false) => 
    api.get(`/notifications${unreadOnly ? '?unread_only=true' : ''}`),
  getUnreadCount: () => api.get('/notifications/unread-count'),
  markRead: (ids) => api.put('/notifications/mark-read', { notification_ids: ids }),
  markAllRead: () => api.put('/notifications/mark-all-read'),
  delete: (id) => api.delete(`/notifications/${id}`)
};

// Task assignment API
export const taskAssignmentAPI = {
  accept: (taskId) => api.put(`/tasks/${taskId}/accept`),
  reject: (taskId) => api.put(`/tasks/${taskId}/reject`),
  complete: (taskId) => api.put(`/tasks/${taskId}/complete`)
};
```

---

## ✅ Testing Checklist

### Notifications
- [ ] Create task and assign to user → assignee receives notification
- [ ] Complete task → creator receives notification
- [ ] Add team member → member receives notification
- [ ] Mark notification as read → unread count decreases
- [ ] Delete notification → removed from list

### Task Assignment
- [ ] Assign task → status is `pending`
- [ ] Accept task → status becomes `accepted`, task status is `in_progress`
- [ ] Reject task → status becomes `rejected`, task unassigned
- [ ] Only assigned user can accept/reject

### Task Completion
- [ ] Complete button works for assigned user
- [ ] Complete button works for task creator
- [ ] Completion timestamp is set
- [ ] Creator gets notification

### Task Sorting
- [ ] Sort by priority (urgent → low)
- [ ] Sort by due date (nearest first)
- [ ] Sort by created date
- [ ] Combine sorting with filters

### Team Members
- [ ] Add member by email works
- [ ] Add member by user_id still works
- [ ] Error if email not found
- [ ] Error if user already in team

---

## 🎯 Next Steps

Recommended frontend updates:
1. **Notification Bell** in navbar with unread count
2. **Notification Dropdown** with recent notifications
3. **Task Card Actions** (Accept, Reject, Complete buttons)
4. **Sort Dropdown** in task list view
5. **Email Input** in add team member modal

---

## 📊 API Summary

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/notifications` | GET | List notifications |
| `/notifications/unread-count` | GET | Get unread count |
| `/notifications/mark-read` | PUT | Mark as read |
| `/notifications/mark-all-read` | PUT | Mark all read |
| `/notifications/{id}` | DELETE | Delete notification |
| `/tasks/{id}/accept` | PUT | Accept assignment |
| `/tasks/{id}/reject` | PUT | Reject assignment |
| `/tasks/{id}/complete` | PUT | Mark complete |
| `/tasks?sort_by=priority` | GET | Sort tasks |
| `/teams/{id}/members` | POST | Add by email or user_id |

---

**All features are production-ready and pushed to GitHub!** 🎉

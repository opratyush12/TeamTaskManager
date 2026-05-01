import axios from 'axios';

const API_URL = import.meta.env.VITE_API_URL || '/api';

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle token refresh
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;

      try {
        const refreshToken = localStorage.getItem('refresh_token');
        const response = await axios.post(`${API_URL}/auth/refresh`, {
          refresh_token: refreshToken,
        });

        const { access_token, refresh_token } = response.data;
        localStorage.setItem('access_token', access_token);
        localStorage.setItem('refresh_token', refresh_token);

        originalRequest.headers.Authorization = `Bearer ${access_token}`;
        return api(originalRequest);
      } catch (refreshError) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        window.location.href = '/login';
        return Promise.reject(refreshError);
      }
    }

    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  getCurrentUser: () => api.get('/auth/me'),
  refresh: (refreshToken) => api.post('/auth/refresh', { refresh_token: refreshToken }),
};

// Teams API
export const teamsAPI = {
  getAll: () => api.get('/teams'),
  getById: (id) => api.get(`/teams/${id}`),
  create: (data) => api.post('/teams', data),
  update: (id, data) => api.put(`/teams/${id}`, data),
  delete: (id) => api.delete(`/teams/${id}`),
  addMember: (teamId, data) => api.post(`/teams/${teamId}/members`, data),
  removeMember: (teamId, userId) => api.delete(`/teams/${teamId}/members/${userId}`),
  updateMemberRole: (teamId, userId, data) => api.put(`/teams/${teamId}/members/${userId}/role`, data),
};

// Projects API
export const projectsAPI = {
  getAll: (teamId) => api.get('/projects', { params: { team_id: teamId } }),
  getById: (id) => api.get(`/projects/${id}`),
  create: (data) => api.post('/projects', data),
  update: (id, data) => api.put(`/projects/${id}`, data),
  delete: (id) => api.delete(`/projects/${id}`),
};

// Tasks API
export const tasksAPI = {
  getAll: (params = {}) => api.get('/tasks', { params }),
  getById: (id) => api.get(`/tasks/${id}`),
  create: (data) => api.post('/tasks', data),
  update: (id, data) => api.put(`/tasks/${id}`, data),
  updateStatus: (id, status) => api.put(`/tasks/${id}/status`, { status }),
  assign: (id, userId) => api.put(`/tasks/${id}/assign`, { assigned_to: userId }),
  delete: (id) => api.delete(`/tasks/${id}`),
};

// Dashboard API
export const dashboardAPI = {
  getOverview: () => api.get('/dashboard/overview'),
  getTasks: () => api.get('/dashboard/tasks'),
  getStats: () => api.get('/dashboard/stats'),
};

// Notifications API
export const notificationsAPI = {
  getAll: (unreadOnly = false) => api.get(`/notifications${unreadOnly ? '?unread_only=true' : ''}`),
  getUnreadCount: () => api.get('/notifications/unread-count'),
  markRead: (ids) => api.put('/notifications/mark-read', { notification_ids: ids }),
  markAllRead: () => api.put('/notifications/mark-all-read'),
  delete: (id) => api.delete(`/notifications/${id}`),
};

// Task actions API
export const taskActionsAPI = {
  accept: (taskId) => api.put(`/tasks/${taskId}/accept`),
  reject: (taskId) => api.put(`/tasks/${taskId}/reject`),
  complete: (taskId) => api.put(`/tasks/${taskId}/complete`),
};

export default api;

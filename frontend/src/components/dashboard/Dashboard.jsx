import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MdCheckCircle, MdPending, MdWarning, MdTrendingUp } from 'react-icons/md';
import { dashboardAPI } from '../../services/api';
import LoadingSpinner from '../common/LoadingSpinner';
import StatsCard from './StatsCard';
import TaskList from './TaskList';

const Dashboard = () => {
  const [loading, setLoading] = useState(true);
  const [overview, setOverview] = useState(null);
  const [tasks, setTasks] = useState(null);
  const [stats, setStats] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const [overviewRes, tasksRes, statsRes] = await Promise.all([
        dashboardAPI.getOverview(),
        dashboardAPI.getTasks(),
        dashboardAPI.getStats(),
      ]);

      setOverview(overviewRes.data);
      setTasks(tasksRes.data);
      setStats(statsRes.data);
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <LoadingSpinner fullScreen />;
  }

  const statsCards = [
    {
      title: 'Total Tasks',
      value: overview?.total_tasks || 0,
      icon: MdCheckCircle,
      color: 'blue',
      trend: `+${stats?.tasks_created_last_7_days || 0} this week`,
    },
    {
      title: 'My Tasks',
      value: overview?.my_tasks || 0,
      icon: MdPending,
      color: 'purple',
      trend: 'Active',
    },
    {
      title: 'Overdue',
      value: overview?.overdue_tasks || 0,
      icon: MdWarning,
      color: 'red',
      trend: 'Need attention',
    },
    {
      title: 'Completion Rate',
      value: `${stats?.completion_rate || 0}%`,
      icon: MdTrendingUp,
      color: 'green',
      trend: `${stats?.tasks_completed_last_7_days || 0} completed`,
    },
  ];

  return (
    <div className="space-y-6">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
      >
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Dashboard</h1>
        <p className="text-gray-600 dark:text-gray-400">Welcome back! Here's your overview.</p>
      </motion.div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsCards.map((stat, index) => (
          <StatsCard key={stat.title} {...stat} index={index} />
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <motion.div
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
          className="card p-6"
        >
          <h2 className="text-xl font-bold mb-4">My Tasks</h2>
          <TaskList tasks={tasks?.my_tasks || []} />
        </motion.div>

        <motion.div
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.4 }}
          className="card p-6"
        >
          <h2 className="text-xl font-bold mb-4">Overdue Tasks</h2>
          <TaskList tasks={tasks?.overdue_tasks || []} />
        </motion.div>
      </div>

      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
        className="card p-6"
      >
        <h2 className="text-xl font-bold mb-4">Recent Team Tasks</h2>
        <TaskList tasks={tasks?.team_tasks || []} />
      </motion.div>
    </div>
  );
};

export default Dashboard;

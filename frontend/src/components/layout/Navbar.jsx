import { motion } from 'framer-motion';
import { MdBrightness4, MdBrightness7, MdLogout, MdPerson } from 'react-icons/md';
import { useTheme } from '../../context/ThemeContext';
import { useAuth } from '../../context/AuthContext';
import { useNavigate } from 'react-router-dom';
import NotificationBell from './NotificationBell';

const Navbar = () => {
  const { isDark, toggleTheme } = useTheme();
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  return (
    <motion.nav
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 px-6 py-4"
    >
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-2xl font-bold text-primary-600 dark:text-primary-400">Task Manager</h1>
        </div>

        <div className="flex items-center space-x-4">
          <NotificationBell />

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-gray-100 dark:bg-gray-700 hover:bg-gray-200 dark:hover:bg-gray-600 transition-colors"
          >
            {isDark ? <MdBrightness7 className="w-5 h-5" /> : <MdBrightness4 className="w-5 h-5" />}
          </motion.button>

          <div className="flex items-center space-x-3 px-4 py-2 rounded-lg bg-gray-100 dark:bg-gray-700">
            <MdPerson className="w-5 h-5 text-gray-600 dark:text-gray-400" />
            <div>
              <p className="text-sm font-medium">{user?.full_name}</p>
              <p className="text-xs text-gray-500 dark:text-gray-400 capitalize">{user?.role}</p>
            </div>
          </div>

          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            onClick={handleLogout}
            className="p-2 rounded-lg bg-red-50 dark:bg-red-900/20 text-red-600 dark:text-red-400 hover:bg-red-100 dark:hover:bg-red-900/30 transition-colors"
          >
            <MdLogout className="w-5 h-5" />
          </motion.button>
        </div>
      </div>
    </motion.nav>
  );
};

export default Navbar;

import { NavLink } from 'react-router-dom';
import { motion } from 'framer-motion';
import { MdDashboard, MdGroup, MdFolder, MdTask } from 'react-icons/md';

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: MdDashboard },
  { path: '/teams', label: 'Teams', icon: MdGroup },
  { path: '/projects', label: 'Projects', icon: MdFolder },
  { path: '/tasks', label: 'Tasks', icon: MdTask },
];

const Sidebar = () => {
  return (
    <motion.aside
      initial={{ x: -20, opacity: 0 }}
      animate={{ x: 0, opacity: 1 }}
      transition={{ delay: 0.1 }}
      className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 p-4"
    >
      <nav className="space-y-2">
        {menuItems.map((item, index) => (
          <motion.div
            key={item.path}
            initial={{ x: -20, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            transition={{ delay: 0.1 * (index + 1) }}
          >
            <NavLink
              to={item.path}
              className={({ isActive }) =>
                `flex items-center space-x-3 px-4 py-3 rounded-lg transition-all duration-200 ${
                  isActive
                    ? 'bg-primary-50 dark:bg-primary-900/20 text-primary-600 dark:text-primary-400 font-medium'
                    : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
                }`
              }
            >
              {({ isActive }) => (
                <>
                  <item.icon className={`w-5 h-5 ${isActive ? 'animate-pulse' : ''}`} />
                  <span>{item.label}</span>
                </>
              )}
            </NavLink>
          </motion.div>
        ))}
      </nav>
    </motion.aside>
  );
};

export default Sidebar;

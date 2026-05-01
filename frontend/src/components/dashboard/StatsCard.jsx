import { motion } from 'framer-motion';

const StatsCard = ({ title, value, icon: Icon, color, trend, index }) => {
  const colors = {
    blue: 'from-blue-500 to-blue-600',
    purple: 'from-purple-500 to-purple-600',
    red: 'from-red-500 to-red-600',
    green: 'from-green-500 to-green-600',
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.1 * index }}
      whileHover={{ y: -5, transition: { duration: 0.2 } }}
      className="card p-6 overflow-hidden relative"
    >
      <div className="relative z-10">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-medium text-gray-600 dark:text-gray-400">{title}</h3>
          <div className={`p-3 rounded-lg bg-gradient-to-br ${colors[color]} text-white shadow-lg`}>
            <Icon className="w-6 h-6" />
          </div>
        </div>
        <p className="text-3xl font-bold text-gray-900 dark:text-white mb-2">{value}</p>
        <p className="text-sm text-gray-500 dark:text-gray-400">{trend}</p>
      </div>
      <div className={`absolute -right-8 -bottom-8 w-32 h-32 bg-gradient-to-br ${colors[color]} opacity-5 rounded-full`}></div>
    </motion.div>
  );
};

export default StatsCard;

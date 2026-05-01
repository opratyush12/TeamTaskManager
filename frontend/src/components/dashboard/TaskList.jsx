import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { Link } from 'react-router-dom';

const TaskList = ({ tasks }) => {
  if (tasks.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500 dark:text-gray-400">
        No tasks found
      </div>
    );
  }

  const priorityColors = {
    low: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
    medium: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    high: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
    urgent: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
  };

  const statusColors = {
    todo: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
    in_progress: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    review: 'bg-purple-100 text-purple-600 dark:bg-purple-900/30 dark:text-purple-400',
    done: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
  };

  return (
    <div className="space-y-3">
      {tasks.map((task, index) => (
        <motion.div
          key={task.id}
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.05 * index }}
          whileHover={{ x: 5 }}
        >
          <Link
            to={`/tasks/${task.id}`}
            className="block p-4 rounded-lg bg-gray-50 dark:bg-gray-700/50 hover:bg-gray-100 dark:hover:bg-gray-700 transition-all border border-gray-200 dark:border-gray-600"
          >
            <div className="flex items-start justify-between mb-2">
              <h4 className="font-medium text-gray-900 dark:text-white line-clamp-1">{task.title}</h4>
              <div className="flex items-center space-x-2">
                <span className={`px-2 py-1 rounded text-xs font-medium ${priorityColors[task.priority]}`}>
                  {task.priority}
                </span>
                <span className={`px-2 py-1 rounded text-xs font-medium ${statusColors[task.status]}`}>
                  {task.status.replace('_', ' ')}
                </span>
              </div>
            </div>
            {task.due_date && (
              <p className="text-sm text-gray-500 dark:text-gray-400">
                Due: {format(new Date(task.due_date), 'MMM dd, yyyy')}
              </p>
            )}
          </Link>
        </motion.div>
      ))}
    </div>
  );
};

export default TaskList;

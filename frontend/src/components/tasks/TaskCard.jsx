import { motion } from 'framer-motion';
import { format } from 'date-fns';
import { MdCheck, MdClose, MdCheckCircle, MdArrowForward } from 'react-icons/md';
import { taskActionsAPI } from '../../services/api';
import Button from '../common/Button';

const TaskCard = ({ task, onUpdate, currentUserId }) => {
  const priorityColors = {
    low: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
    medium: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
    high: 'bg-orange-100 text-orange-600 dark:bg-orange-900/30 dark:text-orange-400',
    urgent: 'bg-red-100 text-red-600 dark:bg-red-900/30 dark:text-red-400',
  };

  const handleAccept = async () => {
    try {
      await taskActionsAPI.accept(task.id);
      onUpdate();
    } catch (error) {
      console.error('Failed to accept task:', error);
      alert('Failed to accept task');
    }
  };

  const handleReject = async () => {
    try {
      await taskActionsAPI.reject(task.id);
      onUpdate();
    } catch (error) {
      console.error('Failed to reject task:', error);
      alert('Failed to reject task');
    }
  };

  const handleComplete = async () => {
    try {
      await taskActionsAPI.complete(task.id);
      onUpdate();
    } catch (error) {
      console.error('Failed to complete task:', error);
      alert('Failed to complete task');
    }
  };

  const isAssignedToCurrentUser = task.assigned_to === currentUserId;
  const isPending = task.assignment_status === 'pending';
  const canComplete = task.status !== 'done' && (isAssignedToCurrentUser || task.created_by === currentUserId);

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      whileHover={{ scale: 1.02 }}
      className="card p-4 space-y-3"
    >
      <div>
        <h4 className="font-medium text-gray-900 dark:text-white mb-1 line-clamp-2">
          {task.title}
        </h4>
        {task.description && (
          <p className="text-sm text-gray-600 dark:text-gray-400 line-clamp-2">
            {task.description}
          </p>
        )}
      </div>

      <div className="flex items-center justify-between">
        <span className={`px-2 py-1 rounded text-xs font-medium ${priorityColors[task.priority]}`}>
          {task.priority}
        </span>
        {task.due_date && (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {format(new Date(task.due_date), 'MMM dd')}
          </span>
        )}
      </div>

      {/* Assignment Status Badge */}
      {task.assignment_status && (
        <div className="flex items-center space-x-2">
          {task.assignment_status === 'pending' && (
            <span className="px-2 py-1 rounded text-xs font-medium bg-yellow-100 text-yellow-700 dark:bg-yellow-900/30 dark:text-yellow-400">
              Pending Acceptance
            </span>
          )}
          {task.assignment_status === 'accepted' && (
            <span className="px-2 py-1 rounded text-xs font-medium bg-green-100 text-green-700 dark:bg-green-900/30 dark:text-green-400">
              Accepted
            </span>
          )}
        </div>
      )}

      {/* Action Buttons */}
      <div className="space-y-2">
        {/* Accept/Reject buttons for pending assignments */}
        {isAssignedToCurrentUser && isPending && (
          <div className="flex space-x-2">
            <button
              onClick={handleAccept}
              className="flex-1 flex items-center justify-center space-x-1 px-3 py-2 bg-green-600 hover:bg-green-700 text-white text-sm rounded-lg transition-colors"
            >
              <MdCheck className="w-4 h-4" />
              <span>Accept</span>
            </button>
            <button
              onClick={handleReject}
              className="flex-1 flex items-center justify-center space-x-1 px-3 py-2 bg-red-600 hover:bg-red-700 text-white text-sm rounded-lg transition-colors"
            >
              <MdClose className="w-4 h-4" />
              <span>Reject</span>
            </button>
          </div>
        )}

        {/* Complete button */}
        {canComplete && (
          <button
            onClick={handleComplete}
            className="w-full flex items-center justify-center space-x-2 px-3 py-2 bg-primary-600 hover:bg-primary-700 text-white text-sm rounded-lg transition-colors"
          >
            <MdCheckCircle className="w-4 h-4" />
            <span>Mark Complete</span>
          </button>
        )}
      </div>

      {/* Assignee Info */}
      {task.assignee && (
        <div className="text-xs text-gray-500 dark:text-gray-400 pt-2 border-t border-gray-200 dark:border-gray-700">
          Assigned to: {task.assignee.full_name}
        </div>
      )}
    </motion.div>
  );
};

export default TaskCard;

import { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { MdAdd, MdFolder } from 'react-icons/md';
import { projectsAPI, teamsAPI } from '../../services/api';
import Button from '../common/Button';
import Modal from '../common/Modal';
import Input from '../common/Input';
import Select from '../common/Select';
import LoadingSpinner from '../common/LoadingSpinner';

const Projects = () => {
  const [projects, setProjects] = useState([]);
  const [teams, setTeams] = useState([]);
  const [loading, setLoading] = useState(true);
  const [modalOpen, setModalOpen] = useState(false);
  const [formData, setFormData] = useState({ name: '', description: '', team_id: '' });

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [projectsRes, teamsRes] = await Promise.all([
        projectsAPI.getAll(),
        teamsAPI.getAll(),
      ]);
      setProjects(projectsRes.data);
      setTeams(teamsRes.data);
    } catch (error) {
      console.error('Failed to fetch data:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await projectsAPI.create(formData);
      setModalOpen(false);
      setFormData({ name: '', description: '', team_id: '' });
      fetchData();
    } catch (error) {
      console.error('Failed to create project:', error);
    }
  };

  if (loading) return <LoadingSpinner fullScreen />;

  const statusColors = {
    active: 'bg-green-100 text-green-600 dark:bg-green-900/30 dark:text-green-400',
    archived: 'bg-gray-100 text-gray-600 dark:bg-gray-700 dark:text-gray-300',
    completed: 'bg-blue-100 text-blue-600 dark:bg-blue-900/30 dark:text-blue-400',
  };

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Projects</h1>
          <p className="text-gray-600 dark:text-gray-400">Organize work within your teams</p>
        </div>
        <Button onClick={() => setModalOpen(true)} icon={MdAdd}>
          Create Project
        </Button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((project, index) => (
          <motion.div
            key={project.id}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 * index }}
            whileHover={{ y: -5 }}
            className="card p-6 cursor-pointer"
          >
            <div className="flex items-center justify-between mb-4">
              <div className="p-3 bg-orange-100 dark:bg-orange-900/30 rounded-lg">
                <MdFolder className="w-8 h-8 text-orange-600 dark:text-orange-400" />
              </div>
              <span className={`px-3 py-1 rounded-full text-xs font-medium ${statusColors[project.status]}`}>
                {project.status}
              </span>
            </div>
            <h3 className="text-lg font-bold text-gray-900 dark:text-white mb-2">{project.name}</h3>
            <p className="text-sm text-gray-500 dark:text-gray-400 line-clamp-2">{project.description}</p>
          </motion.div>
        ))}
      </div>

      <Modal isOpen={modalOpen} onClose={() => setModalOpen(false)} title="Create New Project">
        <form onSubmit={handleSubmit} className="space-y-4">
          <Select
            label="Team"
            value={formData.team_id}
            onChange={(e) => setFormData({ ...formData, team_id: e.target.value })}
            options={teams.map((team) => ({ value: team.id, label: team.name }))}
            required
          />
          <Input
            label="Project Name"
            value={formData.name}
            onChange={(e) => setFormData({ ...formData, name: e.target.value })}
            placeholder="Website Redesign"
            required
          />
          <Input
            label="Description"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            placeholder="Project description..."
          />
          <div className="flex justify-end space-x-3 pt-4">
            <Button variant="secondary" onClick={() => setModalOpen(false)}>
              Cancel
            </Button>
            <Button type="submit">Create Project</Button>
          </div>
        </form>
      </Modal>
    </div>
  );
};

export default Projects;

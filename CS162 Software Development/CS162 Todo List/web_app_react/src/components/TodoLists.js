import { useState, useEffect } from 'react';
import axios from 'axios';
import TasksList from './TaskList';
import AddList from './AddList';

function TodoLists() {
  const [tasks, setTasks] = useState([]);

  const findTaskById = (tasks, taskId) => {
    for (let task of tasks) {
      if (task.id === taskId) return task;
      if (task.sub_items && task.sub_items.length) {
        const found = findTaskById(task.sub_items, taskId);
        if (found) return found;
      }
    }
    return undefined;
  };

  const getUncles = (taskId) => {
    const task = findTaskById(tasks, taskId);
    const parentId = task.parent_id;

    if (parentId === null) {
      return [];
    }

    const parentTask = findTaskById(tasks, parentId);

    if (parentTask.parent_id === null) {
      return tasks.filter(t => t.id !== parentId && t.id !== taskId);
    }

    const grandParentTask = findTaskById(tasks, parentTask.parent_id);
    if (!grandParentTask || !grandParentTask.sub_items) return [];

    return grandParentTask.sub_items.filter(t => t.id !== parentId);
  };

  const moveTask = (taskId, newParentId) => {
    axios.put(`/tasks/${taskId}/move`, { new_parent_id: newParentId })
        .then(response => {
            fetchTasks();
        })
        .catch(error => {
            console.error('Error moving task', error);
        });
  };

  const fetchTasks = () => {
    const token = localStorage.getItem('token');
    axios.defaults.headers.common['Authorization'] = 'Bearer ' + token;

    axios.get('/get-tasks')
      .then(response => {
        setTasks(response.data.tasks);
      })
      .catch(error => {
        console.error('Error fetching tasks', error);
      });
  };

  const deleteTask = (taskId) => {
    axios.delete(`/tasks/${taskId}`)
      .then(() => {
        fetchTasks();
      })
      .catch(error => {
        console.error('Error deleting task', error);
      });
  };

  const addList = (content, parentId = null) => {
    const taskData = {
      content: content
    };
    if (parentId) {
      taskData.parent_id = parentId;
    }

    axios.post('/tasks', taskData)
      .then(response => {
        fetchTasks();
      })
      .catch(error => {
        console.error('Error adding task', error);
      });
  };

  const addTask = (content, parentId = null) => {
    const taskData = {
      content: content
    };
    if (parentId) {
      taskData.parent_id = parentId;
    }

    axios.post('/tasks', taskData)
      .then(response => {
        fetchTasks();
      })
      .catch(error => {
        console.error('Error adding task', error);
      });
  };

  const toggleTaskCompletion = (taskId) => {
    const task = findTaskById(tasks, taskId);
    if (!task) return;

    axios.put(`/tasks/${taskId}`, { is_completed: !task.is_completed })
      .then(() => {
        fetchTasks();
      })
      .catch(error => {
        console.error('Error toggling task completion', error);
      });
  };

  const updateTaskContent = (taskId, newContent) => {
    axios.put(`/tasks/${taskId}`, { content: newContent })
      .then(() => {
        fetchTasks();
      })
      .catch(error => {
        console.error('Error updating task content', error);
      });
  };

  useEffect(fetchTasks, []);

  return (
    <div>
      <AddList onAdd={addList} />
      <TasksList 
      tasks={tasks} 
      onDelete={deleteTask} 
      onAdd={addTask} 
      onToggleCompletion={toggleTaskCompletion} 
      onUpdateContent={updateTaskContent} 
      getUncles={getUncles}
      onMoveTask={moveTask}
      />
    </div>
  );
}

export default TodoLists;
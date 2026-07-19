import React, { useEffect, useState, useCallback } from 'react';
import Login from './components/Login';
import Register from './components/Register';
import TaskForm from './components/TaskForm';
import TaskList from './components/TaskList';
import { getTasks, createTask, updateTask, deleteTask } from './api';
import './App.css';

function App() {
  const [user, setUser] = useState(null);
  const [showRegister, setShowRegister] = useState(false);
  const [tasks, setTasks] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError('');
    try {
      const res = await getTasks();
      setTasks(res.data);
    } catch (err) {
      setError('Could not load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    const token = localStorage.getItem('taskflow_token');
    if (token) {
      // A stored token exists; treat the user as logged in and fetch their tasks.
      setUser({ name: 'Welcome back' });
    }
  }, []);

  useEffect(() => {
    if (user) {
      loadTasks();
    }
  }, [user, loadTasks]);

  function handleLogout() {
    localStorage.removeItem('taskflow_token');
    setUser(null);
    setTasks([]);
  }

  async function handleCreateTask(taskData) {
    try {
      const res = await createTask(taskData);
      setTasks((prev) => [res.data, ...prev]);
    } catch (err) {
      setError('Could not create task.');
    }
  }

  async function handleUpdateStatus(id, status) {
    try {
      const res = await updateTask(id, { status });
      setTasks((prev) => prev.map((t) => (t._id === id ? res.data : t)));
    } catch (err) {
      setError('Could not update task.');
    }
  }

  async function handleDeleteTask(id) {
    try {
      await deleteTask(id);
      setTasks((prev) => prev.filter((t) => t._id !== id));
    } catch (err) {
      setError('Could not delete task.');
    }
  }

  if (!user) {
    return (
      <div className="app-container">
        <h1>TaskFlow</h1>
        <p className="tagline">CI/CD Testing Demo Application</p>

        {showRegister ? (
          <Register onRegister={setUser} />
        ) : (
          <Login onLogin={setUser} />
        )}

        <button className="link-button" onClick={() => setShowRegister((s) => !s)}>
          {showRegister ? 'Already have an account? Log in' : "Don't have an account? Register"}
        </button>
      </div>
    );
  }

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>TaskFlow</h1>
        <button onClick={handleLogout}>Log Out</button>
      </header>

      <TaskForm onCreate={handleCreateTask} />

      {loading && <p>Loading tasks...</p>}
      {error && <p className="error-message">{error}</p>}

      <TaskList tasks={tasks} onUpdateStatus={handleUpdateStatus} onDelete={handleDeleteTask} />
    </div>
  );
}

export default App;

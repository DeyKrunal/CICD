const Task = require('../models/Task');

// GET /api/tasks  (supports ?status=todo and ?search=keyword)
async function getTasks(req, res) {
  try {
    const filter = { owner: req.user.id };

    if (req.query.status) {
      filter.status = req.query.status;
    }
    if (req.query.search) {
      filter.title = { $regex: req.query.search, $options: 'i' };
    }

    const tasks = await Task.find(filter).sort({ createdAt: -1 });
    return res.status(200).json(tasks);
  } catch (err) {
    return res.status(500).json({ message: 'Server error fetching tasks', error: err.message });
  }
}

// GET /api/tasks/:id
async function getTaskById(req, res) {
  try {
    const task = await Task.findOne({ _id: req.params.id, owner: req.user.id });
    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }
    return res.status(200).json(task);
  } catch (err) {
    return res.status(500).json({ message: 'Server error fetching task', error: err.message });
  }
}

// POST /api/tasks
async function createTask(req, res) {
  try {
    const { title, description, status } = req.body;

    if (!title) {
      return res.status(400).json({ message: 'Task title is required' });
    }

    const task = await Task.create({
      title,
      description,
      status,
      owner: req.user.id,
    });

    return res.status(201).json(task);
  } catch (err) {
    return res.status(500).json({ message: 'Server error creating task', error: err.message });
  }
}

// PUT /api/tasks/:id
async function updateTask(req, res) {
  try {
    const task = await Task.findOneAndUpdate(
      { _id: req.params.id, owner: req.user.id },
      req.body,
      { new: true, runValidators: true }
    );

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    return res.status(200).json(task);
  } catch (err) {
    return res.status(500).json({ message: 'Server error updating task', error: err.message });
  }
}

// DELETE /api/tasks/:id
async function deleteTask(req, res) {
  try {
    const task = await Task.findOneAndDelete({ _id: req.params.id, owner: req.user.id });

    if (!task) {
      return res.status(404).json({ message: 'Task not found' });
    }

    return res.status(200).json({ message: 'Task deleted successfully' });
  } catch (err) {
    return res.status(500).json({ message: 'Server error deleting task', error: err.message });
  }
}

module.exports = { getTasks, getTaskById, createTask, updateTask, deleteTask };


const STATUS_LABELS = {
  todo: 'To Do',
  'in-progress': 'In Progress',
  done: 'Done',
};

function TaskList({ tasks, onUpdateStatus, onDelete }) {
  if (!tasks.length) {
    return <p className="empty-state">No tasks yet. Add your first task above!</p>;
  }

  return (
    <ul className="task-list">
      {tasks.map((task) => (
        <li key={task._id} className={`task-item task-${task.status}`}>
          <div className="task-info">
            <h3>{task.title}</h3>
            {task.description && <p>{task.description}</p>}
          </div>

          <div className="task-actions">
            <select
              aria-label={`Change status for ${task.title}`}
              value={task.status}
              onChange={(e) => onUpdateStatus(task._id, e.target.value)}
            >
              {Object.entries(STATUS_LABELS).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>

            <button onClick={() => onDelete(task._id)} aria-label={`Delete ${task.title}`}>
              Delete
            </button>
            <button onClick={() => onUpdate(task._id, task.status)} aria-label={`Updates ${task.title}`}>
              Update
            </button>
          </div>
        </li>
      ))}
    </ul>
  );
}

export default TaskList;

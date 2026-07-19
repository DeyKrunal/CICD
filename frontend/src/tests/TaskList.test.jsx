import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskList from '../components/TaskList';

const sampleTasks = [
  { _id: '1', title: 'Write README', description: 'Document the project', status: 'todo' },
  { _id: '2', title: 'Fix bug', description: '', status: 'in-progress' },
];

test('shows an empty state message when there are no tasks', () => {
  render(<TaskList tasks={[]} onUpdateStatus={() => {}} onDelete={() => {}} />);
  expect(screen.getByText(/no tasks yet/i)).toBeInTheDocument();
});

test('renders a list item for every task', () => {
  render(<TaskList tasks={sampleTasks} onUpdateStatus={() => {}} onDelete={() => {}} />);
  expect(screen.getByText('Write README')).toBeInTheDocument();
  expect(screen.getByText('Fix bug')).toBeInTheDocument();
});

test('calls onDelete with the correct task id when Delete is clicked', async () => {
  const user = userEvent.setup();
  const handleDelete = jest.fn();
  render(<TaskList tasks={sampleTasks} onUpdateStatus={() => {}} onDelete={handleDelete} />);

  await user.click(screen.getByLabelText(/delete write readme/i));

  expect(handleDelete).toHaveBeenCalledWith('1');
});

test('calls onUpdateStatus when a new status is selected', async () => {
  const user = userEvent.setup();
  const handleUpdateStatus = jest.fn();
  render(<TaskList tasks={sampleTasks} onUpdateStatus={handleUpdateStatus} onDelete={() => {}} />);

  await user.selectOptions(screen.getByLabelText(/change status for write readme/i), 'done');

  expect(handleUpdateStatus).toHaveBeenCalledWith('1', 'done');
});

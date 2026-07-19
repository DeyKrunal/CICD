import React from 'react';
import { render, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import TaskForm from '../components/TaskForm';

test('renders task title and description inputs', () => {
  render(<TaskForm onCreate={() => {}} />);
  expect(screen.getByLabelText(/task title/i)).toBeInTheDocument();
  expect(screen.getByLabelText(/task description/i)).toBeInTheDocument();
});

test('calls onCreate with the entered title and description on submit', async () => {
  const user = userEvent.setup();
  const handleCreate = jest.fn();
  render(<TaskForm onCreate={handleCreate} />);

  await user.type(screen.getByLabelText(/task title/i), 'Write tests');
  await user.type(screen.getByLabelText(/task description/i), 'Cover the CI pipeline');
  await user.click(screen.getByRole('button', { name: /add task/i }));

  expect(handleCreate).toHaveBeenCalledWith({
    title: 'Write tests',
    description: 'Cover the CI pipeline',
  });
});

test('does not call onCreate when title is empty', async () => {
  const user = userEvent.setup();
  const handleCreate = jest.fn();
  render(<TaskForm onCreate={handleCreate} />);

  await user.click(screen.getByRole('button', { name: /add task/i }));

  expect(handleCreate).not.toHaveBeenCalled();
});

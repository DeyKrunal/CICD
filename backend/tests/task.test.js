const request = require('supertest');
const app = require('../app');

describe('Task API', () => {
  let token;

  beforeEach(async () => {
    const user = {
      name: 'Task Tester',
      email: 'tasktester@example.com',
      password: 'password123',
    };
    const res = await request(app).post('/api/auth/register').send(user);
    token = res.body.token;
  });

  test('GET /api/tasks requires authentication', async () => {
    const res = await request(app).get('/api/tasks');
    expect(res.statusCode).toBe(401);
  });

  test('POST /api/tasks creates a new task', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Write seminar notes', description: 'Prepare demo script' });

    expect(res.statusCode).toBe(201);
    expect(res.body.title).toBe('Write seminar notes');
    expect(res.body.status).toBe('todo');
  });

  test('POST /api/tasks fails without a title (error handling)', async () => {
    const res = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ description: 'Missing title' });

    expect(res.statusCode).toBe(400);
  });

  test('GET /api/tasks returns only the logged-in user\'s tasks', async () => {
    await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Task 1' });

    const res = await request(app).get('/api/tasks').set('Authorization', `Bearer ${token}`);

    expect(res.statusCode).toBe(200);
    expect(Array.isArray(res.body)).toBe(true);
    expect(res.body.length).toBe(1);
  });

  test('PUT /api/tasks/:id updates a task', async () => {
    const createRes = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Old title' });

    const res = await request(app)
      .put(`/api/tasks/${createRes.body._id}`)
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Updated title', status: 'in-progress' });

    expect(res.statusCode).toBe(200);
    expect(res.body.title).toBe('Updated title');
    expect(res.body.status).toBe('in-progress');
  });

  test('DELETE /api/tasks/:id deletes a task', async () => {
    const createRes = await request(app)
      .post('/api/tasks')
      .set('Authorization', `Bearer ${token}`)
      .send({ title: 'Task to delete' });

    const deleteRes = await request(app)
      .delete(`/api/tasks/${createRes.body._id}`)
      .set('Authorization', `Bearer ${token}`);

    expect(deleteRes.statusCode).toBe(200);

    const getRes = await request(app)
      .get(`/api/tasks/${createRes.body._id}`)
      .set('Authorization', `Bearer ${token}`);

    expect(getRes.statusCode).toBe(404);
  });
});

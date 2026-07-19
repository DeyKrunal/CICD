const request = require('supertest');
const app = require('../app');

describe('Auth API', () => {
  const newUser = {
    name: 'Test User',
    email: 'testuser@example.com',
    password: 'password123',
  };

  test('GET /api/health returns API availability status', async () => {
    const res = await request(app).get('/api/health');
    expect(res.statusCode).toBe(200);
    expect(res.body.status).toBe('ok');
  });

  test('POST /api/auth/register creates a new user and returns a token', async () => {
    const res = await request(app).post('/api/auth/register').send(newUser);

    expect(res.statusCode).toBe(201);
    expect(res.body).toHaveProperty('token');
    expect(res.body.user.email).toBe(newUser.email);
  });

  test('POST /api/auth/register rejects a duplicate email', async () => {
    await request(app).post('/api/auth/register').send(newUser);
    const res = await request(app).post('/api/auth/register').send(newUser);

    expect(res.statusCode).toBe(409);
  });

  test('POST /api/auth/register rejects missing fields (error handling)', async () => {
    const res = await request(app).post('/api/auth/register').send({ email: 'incomplete@example.com' });
    expect(res.statusCode).toBe(400);
  });

  test('POST /api/auth/login succeeds with correct credentials', async () => {
    await request(app).post('/api/auth/register').send(newUser);

    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: newUser.email, password: newUser.password });

    expect(res.statusCode).toBe(200);
    expect(res.body).toHaveProperty('token');
  });

  test('POST /api/auth/login fails with incorrect password (error handling)', async () => {
    await request(app).post('/api/auth/register').send(newUser);

    const res = await request(app)
      .post('/api/auth/login')
      .send({ email: newUser.email, password: 'wrongpassword' });

    expect(res.statusCode).toBe(401);
  });
});

# How to Run the Tests

Covers all 3 test suites in this project:

| Suite | Tool | Location | Needs app running? |
|---|---|---|---|
| Backend API tests | Jest + Supertest | `backend/` | No (uses in-memory MongoDB) |
| Frontend component tests | Jest + React Testing Library | `frontend/` | No |
| Selenium E2E tests (TC01–TC05) | Selenium + pytest + Chrome | `selenium-tests/` | Yes (backend + frontend + MongoDB) |

## 0. Prerequisites

- Node.js v16+ and npm (`node -v`, `npm -v`)
- Python 3.10+ (`python --version`)
- Google Chrome installed (Selenium 4 downloads the driver automatically via Selenium Manager)
- MongoDB running locally **or** a MongoDB Atlas URI
- `.env` files in place (see `backend/.env.example`, `frontend/.env.example`):

```env
# backend/.env
PORT=5000
MONGO_URI=mongodb://localhost:27017/my_database
JWT_SECRET=your_secret_key
```

```env
# frontend/.env
REACT_APP_API_URL=http://localhost:5000
```

Install project dependencies once:

```powershell
cd backend; npm install; cd ..
cd frontend; npm install; cd ..
```

## 1. Backend tests (Jest + Supertest)

```powershell
cd backend
npm test
```

- Uses `mongodb-memory-server`, so no real database is touched.
- `JWT_SECRET=test_secret` is injected by the `npm test` script itself.

## 2. Frontend tests (Jest + React Testing Library)

```powershell
cd frontend
npm test
```

- Runs `react-scripts test --watchAll=false` (single run, no watch mode).
- Covers `src/tests/TaskForm.test.jsx` and `src/tests/TaskList.test.jsx`.

## 3. Selenium E2E tests (TC01–TC05)

Tests `selenium-tests/test_taskflow.py`:

| ID | Test | What it does |
|---|---|---|
| TC01 | Add a new todo | Types into Task title + Add Task, asserts it appears in UI and in MongoDB (`GET /api/tasks`) |
| TC02 | Mark todo as completed | Sets status dropdown to Done, asserts `task-done` style + DB `status == "done"` |
| TC03 | Edit an existing todo | Edits via `PUT /api/tasks/:id` (no working Edit UI exists yet — see note below), refreshes, asserts new text in UI + DB |
| TC04 | Delete a todo | Clicks Delete, asserts it disappears from UI and MongoDB |
| TC05 | Validate empty todo submission | Clicks Add with empty input, asserts count unchanged + browser validation message |

> Note: the spec describes a checkbox + Edit/Save buttons, but the real UI uses a
> status `<select>` dropdown, and `TaskList.jsx` has no working edit-text UI
> (its `Update` button calls an undefined `onUpdate`). TC02/TC03 are adapted to
> the real UI; see the docstring at the top of `test_taskflow.py`.

### 3a. Start the app (2 terminals)

Terminal 1 — backend:

```powershell
cd backend
npm start
# expect: Server running on port 5000 + MongoDB connected
```

Terminal 2 — frontend:

```powershell
cd frontend
npm start
# expect: app at http://localhost:3000
```

### 3b. Register one test user

1. Open `http://localhost:3000`
2. Click "Don't have an account? Register"
3. Register with e.g. `selenium@test.com` / `password123`
4. Log out (so the test can log in fresh)

### 3c. Install Selenium deps + run

```powershell
cd selenium-tests
pip install -r requirements.txt
python -m pytest test_taskflow.py -v
```

> On Windows, if `pytest` alone says "not recognized", always use
> `python -m pytest` (the Scripts folder may not be on PATH).

Run a single case:

```powershell
python -m pytest test_taskflow.py::test_TC01_add_new_todo -v
python -m pytest test_taskflow.py::test_TC05_empty_todo_rejected -v
```

> Login method: the suite logs in via the API (`POST /api/auth/login`) and
> injects the JWT into `localStorage`, instead of typing into the Login UI.
> This is deliberate — driving the Login UI leaves Chrome/chromedriver in a
> state where keystrokes no longer reach the task form (React swaps the whole
> tree after login). The `TEST_EMAIL` account must still exist (step 3b).

### 3e. Test report (auto-generated)

Every run automatically writes a dated report folder via
`selenium-tests/conftest.py` — no extra flags needed:

```text
test-reports/<YYYY-MM-DD>/TaskFlow_Selenium_Report.html   # full TC01–TC05 tables + actual test data
test-reports/<YYYY-MM-DD>/test-results.xml                # JUnit-style results
```

### 3d. Configuration (env variables)

| Variable | Default | Purpose |
|---|---|---|
| `TASKFLOW_URL` | `http://localhost:3000` | Frontend URL |
| `TASKFLOW_API_URL` | `http://localhost:5000` | Backend URL (for MongoDB persistence asserts) |
| `TEST_EMAIL` | `selenium@test.com` | Must match the user registered in 3b |
| `TEST_PASSWORD` | `password123` | Password of that user |

PowerShell example:

```powershell
$env:TASKFLOW_URL = "http://localhost:3000"
$env:TASKFLOW_API_URL = "http://localhost:5000"
$env:TEST_EMAIL = "selenium@test.com"
$env:TEST_PASSWORD = "password123"
python -m pytest test_taskflow.py -v
```

`cmd.exe` example:

```bat
set TEST_EMAIL=selenium@test.com
set TEST_PASSWORD=password123
python -m pytest test_taskflow.py -v
```

## 4. Troubleshooting

| Symptom | Fix |
|---|---|
| Backend `npm test` fails on DB | In-memory server downloads a binary on first run — needs internet once |
| Frontend `npm test` hangs | Use `npm test` (already includes `--watchAll=false`); press `q` if a watcher starts |
| Selenium: `Login failed ... Register this account` | Register the `TEST_EMAIL` account in the UI first (step 3b), or set `TEST_EMAIL`/`TEST_PASSWORD` to an existing account |
| Selenium: `Chrome ... not found` / driver error | Install Google Chrome; Selenium 4 fetches the driver automatically — no manual chromedriver needed |
| Selenium: connection refused on `:3000`/`:5000` | Backend + frontend must both be running (step 3a) before pytest |
| `ModuleNotFoundError: requests` | Re-run `pip install -r requirements.txt` (`requests` is required for the DB assertions) |

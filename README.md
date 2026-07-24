# TaskFlow - CI/CD Testing Demo Application 

> A hands-on task management application built to demonstrate the complete software testing lifecycle — from Alpha Testing and Beta Testing to fully automated Continuous Integration and Continuous Deployment (CI/CD) using GitHub Actions.

This project demonstrates:

- 🧪 Software testing lifecycle
- 🔬 Alpha testing
- 👥 Beta testing
- 🤖 Automated testing
- 🔄 Continuous Integration
- 🚀 Continuous Deployment
- ⚙️ GitHub Actions workflow

Whether you are a complete beginner who has never run a Node.js app before, or an experienced developer looking for a reference CI/CD pipeline, this README will walk you through everything you need to understand, install, run, and present this project.

---

## Table of Contents

1. [Project Overview](#2-project-overview)
2. [Objectives of the Project](#3-objectives-of-the-project)
3. [Features](#4-features)
4. [Technology Stack](#5-technology-stack)
5. [Project Architecture](#6-project-architecture)
6. [Folder Structure](#7-folder-structure)
7. [Prerequisites](#8-prerequisites)
8. [Installation Guide](#9-installation-guide)
9. [Environment Configuration](#10-environment-configuration)
10. [Running the Application](#11-running-the-application)
11. [Testing Guide](#12-testing-guide)
12. [Automated Testing](#13-automated-testing)
13. [CI/CD Pipeline Explanation](#14-cicd-pipeline-explanation)
14. [GitHub Actions Workflow](#15-github-actions-workflow)
15. [Seminar Demo Instructions](#16-seminar-demo-instructions)
16. [Alpha vs Beta Testing Comparison](#17-alpha-testing-vs-beta-testing-comparison)
17. [Advantages of CI/CD](#18-advantages-of-cicd)
18. [Troubleshooting Guide](#19-troubleshooting-guide)
19. [Future Improvements](#20-future-improvements)
20. [Contributors](#21-contributors)
21. [License](#22-license)

---

## 2. Project Overview

**TaskFlow** is a full-stack task management web application — similar in spirit to a simple to-do list or project tracker — where users can register, log in, and manage their own tasks (create, view, update, delete, and organize them by status).

However, the *primary purpose* of TaskFlow is not just to manage tasks. It exists as a **teaching tool** to demonstrate how real-world software teams take code from a developer's laptop all the way to a live, working application — safely, automatically, and with confidence that nothing is broken along the way.

### Why this application was developed

In a real software company, code doesn't just get written and shipped directly to users. It goes through a structured process to make sure it actually works, doesn't break existing features, and is safe to release. TaskFlow was built to give students and beginner developers a small, understandable, but *real* example of that entire process, including:

- Writing application code (frontend + backend)
- Manually testing the application internally (**Alpha Testing**)
- Releasing it to a small group of test users for feedback (**Beta Testing**)
- Automatically testing every code change using scripts (**Automated Testing**)
- Automatically building and verifying the app every time code is pushed (**Continuous Integration**)
- Automatically deploying the app once all tests pass (**Continuous Deployment**)

### How it demonstrates real software development practices

Here is the simplified real-world flow that TaskFlow is built to illustrate:

```
1. Developers write code
2. Code is pushed to GitHub
3. GitHub Actions automatically runs tests
4. Only successful builds are deployed
```

In other words, this project is a *working example* of a **CI/CD pipeline**, wrapped around a simple, easy-to-understand task manager app so that the testing and deployment concepts are easy to see and demonstrate — for example, during a college seminar.

---

## 3. Objectives of the Project

By the end of working through this project, you should be able to:

- ✅ Understand what **Alpha Testing** is and how it's performed
- ✅ Understand what **Beta Testing** is and how it's performed
- ✅ Learn how **automated testing** works using tools like Jest and Supertest
- ✅ Learn how **GitHub Actions** automates repetitive development tasks
- ✅ Demonstrate a complete, working **CI/CD pipeline**
- ✅ Understand the full **software delivery workflow**, from code to deployment
- ✅ Be able to explain and present these concepts confidently in a seminar or interview

---

## 4. Features

### User Features

- 📝 User registration — new users can create an account
- 🔐 User login — secure sign-in for registered users
- 🛡️ Authentication — protects routes and data using tokens (JWT)
- 👤 Profile management — users can view and update their profile details

### Task Features

- ➕ Create tasks — add a new task with a title, description, and status
- 📋 View tasks — see a list of all your tasks
- ✏️ Update tasks — edit task details at any time
- 🗑️ Delete tasks — remove tasks that are no longer needed
- 🔄 Change task status — mark tasks as *To Do*, *In Progress*, or *Done*
- 🔍 Filter tasks — quickly find tasks by status or keyword

### Developer Features

- 🤖 Automated testing — backend and frontend tests run without manual effort
- ⚙️ GitHub Actions pipeline — every push is automatically built and tested
- 🚀 Deployment automation — successful builds can be deployed automatically
- 📊 Test reports — clear pass/fail results after every pipeline run

---

## 5. Technology Stack

| Technology             | Purpose            |
| ---------------------- | ------------------ |
| React.js                | Frontend UI        |
| Node.js                 | Backend runtime    |
| Express.js               | API development    |
| MongoDB                 | Database           |
| Jest                    | Testing framework  |
| React Testing Library    | Frontend testing   |
| Supertest               | API testing        |
| GitHub Actions           | CI/CD automation   |

### What each technology does (in simple terms)

- **React.js** — A JavaScript library used to build the user interface (the buttons, forms, and pages users actually see and click on in the browser).
- **Node.js** — Lets JavaScript run *outside* the browser, on a server. This is what powers the backend of TaskFlow.
- **Express.js** — A lightweight framework built on top of Node.js that makes it easy to create API routes (URLs the frontend talks to, like `/api/tasks`).
- **MongoDB** — A NoSQL database that stores data (like users and tasks) in flexible, JSON-like documents instead of rigid tables.
- **Jest** — A JavaScript testing framework used to write and run automated tests for both frontend and backend code.
- **React Testing Library** — A tool built specifically to test React components the way a real user would interact with them (clicking buttons, typing into forms, etc.).
- **Supertest** — A library used to test API endpoints by sending fake HTTP requests to them and checking the responses.
- **GitHub Actions** — GitHub's built-in automation tool. It watches your repository and automatically runs jobs (like tests and deployments) whenever code is pushed.

---

## 6. Project Architecture

TaskFlow follows a standard three-tier web application architecture, combined with an automated delivery pipeline.

### Application Architecture (how the app runs)

```
User
 |
Frontend (React)
 |
Backend API (Node + Express)
 |
Database (MongoDB)
```

**Explanation:**

1. **User** — A person opens the TaskFlow website in their browser.
2. **Frontend (React)** — The browser loads the React application, which displays the interface (login page, task list, forms, etc.).
3. **Backend API (Node + Express)** — When the user does something (like creating a task), the frontend sends a request to the backend API.
4. **Database (MongoDB)** — The backend reads from or writes to MongoDB to permanently store the data, then sends a response back up to the frontend.

### Delivery Architecture (how code becomes a live app)

```
Developer
 |
Git Push
 |
GitHub Repository
 |
GitHub Actions
 |
Automated Tests
 |
Deployment
```

**Explanation:**

1. **Developer** — Writes or edits code on their local machine.
2. **Git Push** — Uploads (pushes) the code changes to GitHub using Git.
3. **GitHub Repository** — Stores the official, shared copy of the project's code.
4. **GitHub Actions** — Automatically detects the new push and starts a pipeline (a series of automated steps).
5. **Automated Tests** — The pipeline runs all backend and frontend tests to check that nothing is broken.
6. **Deployment** — If (and only if) all tests pass, the application is automatically deployed/updated.

---

## 7. Folder Structure

```
TaskFlow-CICD-Demo

├── frontend
│   ├── src
│   ├── components
│   ├── tests
│   └── package.json
│
├── backend
│   ├── routes
│   ├── controllers
│   ├── models
│   ├── tests
│   └── package.json
│
├── .github
│   └── workflows
│       └── cicd.yml
│
├── ALPHA_TESTING.md
├── BETA_TESTING.md
├── SEMINAR_NOTES.md
└── README.md
```

### Explanation of each folder/file

- **`frontend/`** — Contains the entire React application (the user interface).
  - **`src/`** — The main source code of the React app (pages, logic, styling).
  - **`components/`** — Reusable UI pieces, like buttons, task cards, and forms.
  - **`tests/`** — Automated tests for the frontend, written using Jest and React Testing Library.
  - **`package.json`** — Lists the frontend's dependencies and scripts (like `npm start`, `npm test`).

- **`backend/`** — Contains the entire Node.js + Express server (the API).
  - **`routes/`** — Defines the API endpoints (e.g., `/api/tasks`, `/api/users`).
  - **`controllers/`** — Contains the logic that runs when a route is called (e.g., what happens when a task is created).
  - **`models/`** — Defines the structure (schema) of data stored in MongoDB (e.g., what a "Task" or "User" looks like).
  - **`tests/`** — Automated backend tests, written using Jest and Supertest.
  - **`package.json`** — Lists the backend's dependencies and scripts.

- **`.github/workflows/cicd.yml`** — The GitHub Actions configuration file. This is the file that defines the entire CI/CD pipeline: when it runs, what steps it performs, and in what order.

- **`ALPHA_TESTING.md`** — A document describing the internal Alpha Testing process and results.

- **`BETA_TESTING.md`** — A document describing the Beta Testing process, feedback collected, and results.

- **`SEMINAR_NOTES.md`** — Speaker notes and a script to help present this project during a seminar or demo.

- **`README.md`** — This file — the main documentation for the project.

---

## 8. Prerequisites

Before installing TaskFlow, make sure the following software is installed on your computer:

| Requirement            | Purpose                                             |
| ----------------------- | ---------------------------------------------------- |
| **Node.js** (v16 or higher) | Runs the backend server and frontend build tools    |
| **npm** (comes with Node.js) | Installs project dependencies                     |
| **Git**                  | Downloads (clones) the project and manages versions |
| **GitHub account**        | Needed to fork/clone the repository and view Actions |
| **MongoDB** (local or Atlas cloud account) | Stores application data                |

### Verifying your installation

Open a terminal (Command Prompt, PowerShell, or Terminal app) and run each of the following commands:

```bash
node -v
```
This should print your installed Node.js version, e.g. `v18.17.0`. If you see an error, Node.js is not installed correctly.

```bash
npm -v
```
This should print your installed npm version, e.g. `9.6.7`. npm is installed automatically with Node.js.

```bash
git --version
```
This should print your installed Git version, e.g. `git version 2.41.0`. If this fails, install Git from [git-scm.com](https://git-scm.com/).

> 💡 **Tip:** If any of these commands are not recognized, it usually means the software either isn't installed, or isn't added to your system's PATH. Reinstalling the software and restarting your terminal usually fixes this.

---

## 9. Installation Guide

Follow these steps in order. Each command should be run in your terminal.

### Step 1: Clone the Repository

```bash
git clone repository-url

cd TaskFlow-CICD-Demo
```

**What this does:** `git clone` downloads a full copy of the project from GitHub onto your computer. `cd TaskFlow-CICD-Demo` moves your terminal into the newly created project folder so subsequent commands run in the right place.

### Step 2: Install Backend Dependencies

```bash
cd backend

npm install
```

**What this does:** `cd backend` moves into the backend folder. `npm install` reads the `package.json` file and downloads all the libraries the backend needs to run (Express, MongoDB drivers, testing tools, etc.) into a `node_modules` folder.

### Step 3: Install Frontend Dependencies

```bash
cd frontend

npm install
```

**What this does:** Same idea as above, but for the frontend — `npm install` downloads React and all other frontend libraries needed to run the user interface.

> 📌 **Note:** Run these two `npm install` commands from the project's `backend` and `frontend` folders respectively — not from the root folder — since each has its own separate `package.json`.

---

## 10. Environment Configuration

TaskFlow uses **environment variables** to store configuration values and secrets (like database URLs and secret keys) *outside* of the actual code. This keeps sensitive information private and makes it easy to use different settings in different environments (local, testing, production) without changing any code.

### Backend Environment File

Create a file named `.env` inside the `backend` folder with the following content:

```env
PORT=5000

MONGO_URI=your_database_url

JWT_SECRET=your_secret_key
```

- **`PORT`** — The port number the backend server will run on (e.g., `http://localhost:5000`).
- **`MONGO_URI`** — The connection string for your MongoDB database (local or cloud-based, like MongoDB Atlas).
- **`JWT_SECRET`** — A private key used to sign and verify authentication tokens (JWTs) securely. This should be a long, random string that is never shared publicly.

### Frontend Environment File

Create a file named `.env` inside the `frontend` folder with the following content:

```env
REACT_APP_API_URL=http://localhost:5000
```

- **`REACT_APP_API_URL`** — Tells the React frontend where to send its API requests (i.e., where the backend server is running).

### Why environment variables matter

- 🔒 **Security** — Secrets like `JWT_SECRET` and database credentials are never hard-coded or committed to GitHub.
- 🔧 **Flexibility** — The same code can run against a local database during development and a cloud database in production, just by changing `.env` values.
- 🚫 **Best practice** — The `.env` file should always be added to `.gitignore` so it is never pushed to GitHub.

---

## 11. Running the Application

Once dependencies are installed and `.env` files are configured, you can run TaskFlow locally.

### Start the Backend

From inside the `backend` folder:

```bash
npm start
```

This starts the Express API server (by default at `http://localhost:5000`). It handles requests from the frontend, talks to MongoDB, and returns data such as tasks and user information.

### Start the Frontend

From inside the `frontend` folder (in a **separate** terminal window):

```bash
npm start
```

This starts the React development server (usually at `http://localhost:3000`) and should automatically open TaskFlow in your default web browser.

### What happens when both are running

1. The **backend** listens for API requests and manages data in MongoDB.
2. The **frontend** displays the user interface and sends requests to the backend whenever the user interacts with the app.
3. Your **browser** opens the application, letting you register, log in, and manage tasks — all powered by the frontend talking to the backend behind the scenes.

---

## 12. Testing Guide

TaskFlow demonstrates two important types of *manual*, human-driven testing: **Alpha Testing** and **Beta Testing**.

### Alpha Testing

Alpha Testing is the **first round of testing**, performed internally before the application is shown to any real, outside users.

**Key characteristics:**

- Performed by the developers or an internal testing team
- Conducted in a controlled, internal environment
- Goal: catch bugs, crashes, and major issues *before* anyone outside the team sees the app
- Happens *before* Beta Testing and before any public release

📄 See **[`ALPHA_TESTING.md`](./ALPHA_TESTING.md)** for the full checklist of test cases, steps to reproduce them, and space to record results. To use it, simply go through each test case listed in the file, perform the described action in the running application, and mark it as Pass or Fail.

### Beta Testing

Beta Testing is the **second round of testing**, performed *after* Alpha Testing, using a small group of real, outside users.

**Key characteristics:**

- Performed by real users (not the development team)
- Conducted in a real-world (or close to real-world) environment
- Goal: collect genuine feedback and uncover usability issues developers might not notice themselves
- Happens *before* the final, public release

📄 See **[`BETA_TESTING.md`](./BETA_TESTING.md)** for the feedback form template, testing instructions for volunteers, and a summary of feedback collected.

---

## 13. Automated Testing

In addition to manual Alpha/Beta testing, TaskFlow includes **automated tests** — scripts that test the code itself, without any human clicking through the app.

### Backend Testing

Run backend tests with:

```bash
npm test
```
*(run this command from inside the `backend` folder)*

**What gets tested:**

- ✅ **API availability** — Confirms the server starts and responds to requests.
- ✅ **Task creation** — Confirms new tasks are correctly saved to the database.
- ✅ **Task update** — Confirms existing tasks can be modified correctly.
- ✅ **Error handling** — Confirms the API responds properly (with the right error messages/codes) when something goes wrong, like invalid input.

These tests use **Jest** as the test runner and **Supertest** to simulate HTTP requests to the API, without needing a real browser or frontend.

### Frontend Testing

Run frontend tests with:

```bash
npm test
```
*(run this command from inside the `frontend` folder)*

**What gets tested:**

- ✅ **Component testing** — Confirms individual React components (like a task card or login form) render correctly.
- ✅ **UI testing** — Confirms the correct text, buttons, and elements appear on screen.
- ✅ **User interaction testing** — Simulates real user actions (typing, clicking) using React Testing Library to confirm the app responds as expected (e.g., clicking "Delete" actually removes a task).

> 💡 Automated tests are what make the **CI/CD pipeline** possible — GitHub Actions runs these exact same `npm test` commands automatically on every push.

---

## 14. CI/CD Pipeline Explanation

**CI/CD** stands for **Continuous Integration** and **Continuous Deployment** (or Delivery). In simple terms:

- **Continuous Integration (CI)** — Every time code is pushed, it is automatically combined ("integrated") with the existing project and tested, to catch problems early.
- **Continuous Deployment (CD)** — If all tests pass, the code is automatically deployed (released) without needing a manual, error-prone release process.

TaskFlow's entire pipeline is defined in one file:

```
.github/workflows/cicd.yml
```

This YAML file tells GitHub exactly what to do, and in what order, every time code changes.

### The Pipeline Stages

```
Code Change
     ↓
Git Push
     ↓
GitHub Actions Triggered
     ↓
Install Dependencies
     ↓
Run Tests
     ↓
Build Application
     ↓
Deploy
```

**Explanation of each stage:**

1. **Code Change** — A developer edits code locally (e.g., fixes a bug or adds a feature).
2. **Git Push** — The developer pushes the change to the GitHub repository.
3. **GitHub Actions Triggered** — GitHub detects the push and automatically starts the workflow defined in `cicd.yml`.
4. **Install Dependencies** — The pipeline runs `npm install` for both frontend and backend, in a clean, temporary environment, to ensure everything needed is present.
5. **Run Tests** — The pipeline runs `npm test` for both frontend and backend, exactly like a developer would locally, to check that nothing is broken.
6. **Build Application** — If tests pass, the frontend is compiled into an optimized, production-ready version (e.g., using `npm run build`).
7. **Deploy** — The tested, built application is automatically deployed/published, making the update available without any manual steps.

> 🔑 **Key idea:** If *any* stage fails (especially the testing stage), the pipeline stops immediately — the broken code is **never deployed**.

---

## 15. GitHub Actions Workflow

GitHub Actions is configured to automatically trigger the pipeline on specific events, defined inside `cicd.yml`.

### When the pipeline runs

```yaml
on:
  push:
  pull_request:
```

- **`push`** — The pipeline runs automatically whenever code is pushed to the repository (e.g., to the `main` branch).
- **`pull_request`** — The pipeline also runs automatically whenever someone opens a Pull Request, so problems are caught *before* code is even merged.

### Successful Pipeline Run

When everything works correctly, you'll see:

```
✓ Build Passed
✓ Tests Passed
✓ Deployment Completed
```

### Failed Pipeline Run

If something is broken (e.g., a test fails), you'll see:

```
✗ Test Failed
✗ Deployment Blocked
```

### Why this matters

This automated "gatekeeper" behavior is one of the most important benefits of CI/CD: **broken or untested code physically cannot reach real users**, because the deployment step only runs *after* all tests pass. This removes the risk of a developer forgetting to test something manually, or accidentally deploying code that breaks the application.

---

## 16. Seminar Demo Instructions

This section provides a complete, step-by-step script for presenting TaskFlow during a seminar, class demo, or presentation. (See also `SEMINAR_NOTES.md` for speaker notes.)

### Step 1: Introduce the Repository

- Open the GitHub repository in a browser.
- Walk the audience through the folder structure (`frontend/`, `backend/`, `.github/workflows/`, etc.).
- Briefly explain the purpose of the project: demonstrating Alpha/Beta testing and a full CI/CD pipeline.

### Step 2: Demonstrate the Running Application

- Show the application running locally (or deployed) in the browser.
- Demonstrate the core features live:
  - **Login** — Log in with a test account.
  - **Create task** — Add a new task.
  - **Update task** — Edit the task you just created.
  - **Delete task** — Remove a task.

### Step 3: Make a Code Change

- Make a small, visible change to the code (e.g., update a button label or add a small feature).
- Push the change to GitHub:

```bash
git add .

git commit -m "Feature update"

git push
```

### Step 4: Show GitHub Actions in Action

- Open the **Actions** tab on GitHub.
- Show the workflow that was automatically triggered by the push.
- Walk through each step live as it runs: installing dependencies, running tests, building, and deploying.

### Step 5: Introduce a Bug (Show a Failure)

- Intentionally introduce a small bug (e.g., break a test or add invalid code).
- Push the change and show the pipeline **fail**.
- Explain to the audience: *"CI prevents faulty code from being deployed — this is exactly why the deployment step never ran."*

### Step 6: Fix the Issue and Show Success

- Fix the bug you introduced.
- Push the corrected code.
- Show the pipeline running again — this time succeeding — and the application deploying successfully.

> 🎤 **Presentation Tip:** This "break it, then fix it" demonstration (Steps 5–6) is often the most memorable part of the seminar, as it visibly proves that CI/CD protects real applications from broken code.

---

## 17. Alpha Testing vs Beta Testing Comparison

| Feature      | Alpha Testing            | Beta Testing           |
| ------------- | -------------------------- | ------------------------- |
| **Tester**     | Internal team              | Real users                |
| **Environment** | Developer environment      | User environment          |
| **Purpose**    | Find technical issues       | Collect feedback           |
| **Timing**     | Before beta                | Before final release       |

---

## 18. Advantages of CI/CD

- ⚡ **Faster releases** — New features and fixes reach users much more quickly, since the release process is automated.
- ✅ **Automated quality checks** — Every single change is tested the same way, every time, with no steps skipped.
- 🐛 **Reduced manual errors** — Removes the risk of a human forgetting to run a test or a build step before releasing.
- 🤝 **Better collaboration** — Multiple developers can work on the same project confidently, knowing the pipeline will catch conflicts or breakages.
- 🔎 **Early bug detection** — Problems are caught within minutes of being introduced, rather than being discovered much later (or by users in production).

---

## 19. Troubleshooting Guide

### `npm install` error

If dependencies fail to install, try clearing the npm cache and reinstalling:

```bash
npm cache clean --force
npm install
```

### Database connection error

If the backend cannot connect to MongoDB, check the following:

- ✅ Is the `MONGO_URI` in your `.env` file correct and complete?
- ✅ Are your environment variables actually being loaded (is the `.env` file in the correct folder)?
- ✅ Is your MongoDB service (local or Atlas) actually running and accessible from your network?

### GitHub Actions failure

If the pipeline fails on GitHub, check the following:

- ✅ Review the **error logs** in the failed workflow run (Actions tab → click the failed run → expand the failed step).
- ✅ Identify which specific **test case(s) failed** and reproduce them locally using `npm test`.
- ✅ Check for **dependency version mismatches** between your local environment and the versions specified in `package.json`.

---

## 20. Future Improvements

TaskFlow is intentionally kept simple for teaching purposes, but here are natural next steps for extending it:

- 🐳 **Docker support** — Containerize the frontend and backend for consistent environments everywhere.
- ☸️ **Kubernetes deployment** — Orchestrate and scale the application across multiple containers/servers.
- 📈 **Cloud monitoring** — Add logging and monitoring (e.g., with a service like Datadog or Grafana) to track application health in production.
- 🔐 **Advanced authentication** — Add features like OAuth login (Google/GitHub sign-in), password resets, and multi-factor authentication.
- 📱 **Mobile application** — Build a companion mobile app (e.g., with React Native) that uses the same backend API.
- 🏎️ **Performance testing** — Add load and stress testing to see how the application behaves under heavy traffic.

---

## 21. Contributors

```
Developed for:
Software Testing and CI/CD Seminar

Project Type:
Educational Demonstration Project
```

This project was built as a learning resource to make abstract software engineering concepts — like Alpha/Beta testing and CI/CD — tangible and easy to demonstrate to others.

---

## 22. License

This project is released as an open-source educational resource under the **MIT License**.

```
MIT License

Copyright (c) 2026

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
```

Feel free to fork, modify, and use this project for your own learning, teaching, or seminar purposes.

---

<p align="center">Made with ❤️ to make CI/CD click.</p>

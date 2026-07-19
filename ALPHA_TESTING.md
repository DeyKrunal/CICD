# Alpha Testing - TaskFlow

Alpha Testing is performed **internally**, by the development team, before the application is shown to any real outside users. The goal is to catch obvious bugs, crashes, and broken functionality early.

## How to Use This Document

1. Run the application locally (see the main `README.md` for setup instructions).
2. Go through each test case below in order.
3. Perform the described action.
4. Record the actual result and mark the test as **Pass** or **Fail**.
5. Log any failed test as a bug/issue before moving on to Beta Testing.

## Test Environment

| Item             | Value                          |
| ----------------- | ------------------------------- |
| Tested by          | _(internal tester name)_        |
| Date               | _(date of testing)_             |
| Backend URL        | http://localhost:5000           |
| Frontend URL       | http://localhost:3000           |
| Browser            | _(e.g. Chrome 126)_             |

## Test Cases

| # | Test Case | Steps | Expected Result | Actual Result | Status |
|---|-----------|-------|------------------|-----------------|--------|
| 1 | User registration | Fill in name, email, password on Register page and submit | New account is created, user is logged in | | Pass / Fail |
| 2 | Duplicate registration | Register again with the same email | Error message is shown, no duplicate account is created | | Pass / Fail |
| 3 | User login | Enter valid credentials on Login page | User is logged in and redirected to task dashboard | | Pass / Fail |
| 4 | Invalid login | Enter an incorrect password | Clear error message is shown, login is rejected | | Pass / Fail |
| 5 | Create task | Enter a title and click "Add Task" | New task appears at the top of the task list | | Pass / Fail |
| 6 | Empty task title | Try submitting the task form with no title | Form does not submit / task is not created | | Pass / Fail |
| 7 | Update task status | Change a task's status dropdown | Task moves to the new status and UI updates | | Pass / Fail |
| 8 | Delete task | Click "Delete" on a task | Task is removed from the list immediately | | Pass / Fail |
| 9 | Logout | Click "Log Out" | User is returned to the login screen | | Pass / Fail |
| 10 | API health check | Visit `http://localhost:5000/api/health` | Returns `{ "status": "ok" }` | | Pass / Fail |

## Summary

- Total test cases: 10
- Passed: ____
- Failed: ____
- Critical issues found: ____

> Once all critical issues from Alpha Testing are resolved, the application is ready to move on to **Beta Testing** (see `BETA_TESTING.md`).

# Selenium Test Report — TaskFlow (TC01–TC05)

- **Date:** 2026-10-08
- **Suite:** `selenium-tests/test_taskflow.py`
- **Command:** `python -m pytest selenium-tests/test_taskflow.py -v`
- **Machine-readable output:** `selenium-tests/test-results.xml` (JUnit XML)
- **Environment:** Windows (win32) · Python 3.13.11 · pytest 8.3.3 · Selenium 4.50.0 · Headless Chrome
- **App under test:** Frontend `http://localhost:3000` · Backend `http://localhost:5000` · Login via API + JWT injection (`selenium@test.com`)

## Summary

| Total | Passed | Failed | Errors | Skipped | Suite time |
|------:|-------:|-------:|-------:|--------:|-----------:|
| 5 | 5 | 0 | 0 | 0 | 7.83 s |

**Result: ALL TESTS PASSED ✔**

## Detailed results

| TC ID | Test case | Status | Time |
|---|---|--------|-----:|
| TC01 | Add a new todo — enter todo, click Add; appears in list and in MongoDB | PASSED | 1.94 s |
| TC02 | Mark todo as completed — status dropdown to Done; `task-done` style + persisted | PASSED | 0.66 s |
| TC03 | Edit an existing todo — `PUT /api/tasks/:id`, refresh, new text shown + persisted | PASSED | 0.77 s |
| TC04 | Delete a todo — disappears from UI and MongoDB | PASSED | 0.63 s |
| TC05 | Validate empty todo submission — no todo created, validation message shown | PASSED | 3.37 s |

## Raw console output

```text
============================= test session starts =============================
platform win32 -- Python 3.13.11, pytest-8.3.3, pluggy-1.6.0 -- C:\Python313\python.exe
cachedir: .pytest_cache
rootdir: D:\Projects\CICD\TaskFlow-CICD-Demo
plugins: anyio-4.13.0, colcon-core-0.20.1, cov-7.0.0, repeat-0.9.4, rerunfailures-16.1
collecting ... collected 5 items

selenium-tests/test_taskflow.py::test_TC01_add_new_todo PASSED           [ 20%]
selenium-tests/test_taskflow.py::test_TC02_mark_todo_completed PASSED    [ 40%]
selenium-tests/test_taskflow.py::test_TC03_edit_existing_todo PASSED     [ 60%]
selenium-tests/test_taskflow.py::test_TC04_delete_todo PASSED            [ 80%]
selenium-tests/test_taskflow.py::test_TC05_empty_todo_rejected PASSED    [100%]

- generated xml file: D:\Projects\CICD\TaskFlow-CICD-Demo\selenium-tests\test-results.xml -
============================== 5 passed in 7.83s ==============================
```

## Notes

- Each UI assertion is paired with a MongoDB persistence check via `GET /api/tasks`.
- Known app deviations covered by the suite: status is changed through a `<select>` dropdown (spec says checkbox); TC03 edits through the API because `TaskList.jsx` has no working edit-text UI (its `Update` button calls an undefined `onUpdate`).
- To re-generate this report: run the command above, then refresh the table/timings from the console output and `test-results.xml`.

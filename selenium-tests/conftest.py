"""Pytest hooks: auto-generate the dated test-report folder when the suite finishes.

Just run the suite — no extra flags needed::

    python -m pytest selenium-tests/test_taskflow.py

After the session ends, this creates/overwrites::

    test-reports/<YYYY-MM-DD>/TaskFlow_Selenium_Report.html
    test-reports/<YYYY-MM-DD>/test-results.xml   (JUnit-style)

Per-test input data is picked up from the ``[TESTDATA] ...`` lines the tests
print (captured stdout), so the HTML shows the actual values used in that run.
"""

import datetime
import html as html_module
import re
from pathlib import Path

# Static documentation per test case: (module, scenario, preconditions,
# steps_html, expected, severity, priority, comments)
CASES = {
    "test_TC01_add_new_todo": (
        "Tasks — Create",
        "Verify a new todo can be added and is stored in MongoDB",
        "User is registered and logged in; task form is visible",
        "<ol><li>Enter the todo in the Task title input field</li>"
        "<li>Click <strong>Add Task</strong></li></ol>",
        "The new todo appears in the list and is stored in MongoDB",
        "High", "P1",
        "UI + database assertions both checked.",
    ),
    "test_TC02_mark_todo_completed": (
        "Tasks — Status update",
        "Verify a todo can be marked as completed and the status is saved",
        "Logged in; a todo exists in the list",
        "<ol><li>Locate the existing todo</li>"
        "<li>Set its status dropdown (“Change status for…”) to <strong>Done</strong></li></ol>",
        "The todo is marked completed (done styling) and the updated status is saved in MongoDB",
        "High", "P1",
        "Spec mentions a checkbox; the app uses a status dropdown instead — test adapted to the real UI.",
    ),
    "test_TC03_edit_existing_todo": (
        "Tasks — Edit",
        "Verify todo text can be changed and the update persists",
        "Logged in; a todo exists in the list",
        "<ol><li>Send the updated title through <code>PUT /api/tasks/:id</code></li>"
        "<li>Refresh the page</li>"
        "<li>Verify the updated text is displayed and present in <code>GET /api/tasks</code></li></ol>",
        "The updated todo text is displayed and persisted in the database",
        "Medium", "P2",
        "TaskList.jsx has no working edit-text UI (its “Update” button calls an undefined "
        "<code>onUpdate</code>), so the edit goes through the API. Convert to UI clicks once an inline Edit/Save UI exists.",
    ),
    "test_TC04_delete_todo": (
        "Tasks — Delete",
        "Verify a todo can be deleted from the UI and the database",
        "Logged in; a todo exists in the list",
        "<ol><li>Locate the existing todo</li>"
        "<li>Click <strong>Delete</strong> (aria-label “Delete …”)</li>"
        "<li>Confirm if prompted (no confirmation dialog in this app)</li></ol>",
        "The todo disappears from the UI and is removed from MongoDB",
        "High", "P1",
        "No confirmation prompt exists. Minor UI note: the delete button text reads “Deletes”.",
    ),
    "test_TC05_empty_todo_rejected": (
        "Tasks — Input validation",
        "Verify an empty todo cannot be submitted",
        "Logged in; task form is visible; task count recorded before the attempt",
        "<ol><li>Leave the todo input empty</li>"
        "<li>Click <strong>Add Task</strong></li></ol>",
        "No empty todo is created; an appropriate validation message is shown",
        "Medium", "P2",
        "Validation is enforced by the HTML <code>required</code> attribute plus a "
        "<code>title.trim()</code> guard — no custom error banner is rendered.",
    ),
}

ENVIRONMENT = "Local QA – Headless Chrome (Windows) · Frontend :3000 · Backend :5000 · MongoDB local"

_results = {}  # nodeid -> {status, time, data, error}


def _record(report):
    name = report.nodeid.split("::")[-1]
    entry = _results.setdefault(name, {"status": "Pass", "time": 0.0, "data": "", "error": ""})
    entry["time"] += getattr(report, "duration", 0.0)
    if report.failed:
        entry["status"] = "Blocked" if report.when == "setup" else "Fail"
        try:
            entry["error"] = str(report.longrepr)[:600]
        except Exception:
            entry["error"] = "see console output"
    for stream in (getattr(report, "capstdout", ""), getattr(report, "capstderr", "")):
        m = re.search(r"\[TESTDATA\] (.*)", stream or "")
        if m:
            entry["data"] = m.group(1).strip()


def pytest_runtest_logreport(report):
    _record(report)


def pytest_sessionfinish(session, exitstatus):
    if not _results:
        return
    day = datetime.date.today().isoformat()
    outdir = Path(session.config.rootpath) / "test-reports" / day
    outdir.mkdir(parents=True, exist_ok=True)
    _write_xml(outdir / "test-results.xml")
    _write_html(outdir / "TaskFlow_Selenium_Report.html")
    print(f"\n[REPORT] Test report written to {outdir}")


def _write_xml(path):
    total = len(_results)
    failed = sum(1 for r in _results.values() if r["status"] == "Fail")
    errors = sum(1 for r in _results.values() if r["status"] == "Blocked")
    suite_time = sum(r["time"] for r in _results.values())
    lines = [
        '<?xml version="1.0" encoding="utf-8"?>',
        f'<testsuite name="taskflow-selenium" tests="{total}" failures="{failed}" '
        f'errors="{errors}" skipped="0" time="{suite_time:.3f}">',
    ]
    for name in sorted(_results):
        r = _results[name]
        lines.append(f'  <testcase classname="selenium-tests.test_taskflow" name="{name}" time="{r["time"]:.3f}">')
        if r["status"] == "Fail":
            lines.append(f'    <failure message="assertion failed">{html_module.escape(r["error"])}</failure>')
        elif r["status"] == "Blocked":
            lines.append(f'    <error message="setup error">{html_module.escape(r["error"])}</error>')
        if r["data"]:
            lines.append(f'    <system-out>[TESTDATA] {html_module.escape(r["data"])}</system-out>')
        lines.append("  </testcase>")
    lines.append("</testsuite>")
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def _write_html(path):
    total = len(_results)
    passed = sum(1 for r in _results.values() if r["status"] == "Pass")
    failed = sum(1 for r in _results.values() if r["status"] == "Fail")
    blocked = sum(1 for r in _results.values() if r["status"] == "Blocked")
    suite_time = sum(r["time"] for r in _results.values())
    verdict = "ALL TESTS PASSED ✔" if (failed == 0 and blocked == 0) else "FAILURES PRESENT ✘"

    sections = []
    for tcid in ["test_TC01_add_new_todo", "test_TC02_mark_todo_completed",
                 "test_TC03_edit_existing_todo", "test_TC04_delete_todo",
                 "test_TC05_empty_todo_rejected"]:
        short = re.search(r"TC\d+", tcid).group(0)
        meta = CASES.get(tcid, ("", "", "", "", "", "", "", ""))
        module, scenario, pre, steps, expected, sev, pri, comments = meta
        r = _results.get(tcid, {"status": "Not run", "time": 0.0, "data": "—", "error": ""})
        badge = ("<span class=\"pass\">Pass</span>" if r["status"] == "Pass"
                 else f"<span class=\"fail\">{html_module.escape(r['status'])}</span>")
        if r["status"] == "Pass":
            actual = f"{html_module.escape(expected)} — observed in this run ({r['time']:.2f} s)."
        elif r["data"]:
            actual = f"Did not pass. Error: <code>{html_module.escape(r['error'][:300])}</code>"
        else:
            actual = "Not executed in this run."
        data = html_module.escape(r["data"]) if r["data"] else "— (no test data captured)"
        sections.append(
            f"<h2>{short} — {html_module.escape(scenario)}</h2>\n"
            "<table class=\"case\">\n"
            f"  <tr><th>Test Case ID</th><td>{short}</td></tr>\n"
            f"  <tr><th>Module</th><td>{module}</td></tr>\n"
            f"  <tr><th>Test Scenario</th><td>{html_module.escape(scenario)}</td></tr>\n"
            f"  <tr><th>Preconditions</th><td>{pre}</td></tr>\n"
            f"  <tr><th>Test Data</th><td><code>{data}</code></td></tr>\n"
            f"  <tr><th>Test Steps</th><td>{steps}</td></tr>\n"
            f"  <tr><th>Expected Result</th><td>{expected}</td></tr>\n"
            f"  <tr><th>Actual Result</th><td>{actual}</td></tr>\n"
            f"  <tr><th>Status</th><td>{badge}</td></tr>\n"
            f"  <tr><th>Severity</th><td>{sev}</td></tr>\n"
            f"  <tr><th>Priority</th><td>{pri}</td></tr>\n"
            f"  <tr><th>Environment</th><td>{ENVIRONMENT}</td></tr>\n"
            f"  <tr><th>Comments</th><td>{comments}</td></tr>\n"
            "</table>"
        )

    css = (
        "body{font-family:-apple-system,'Segoe UI',Roboto,Arial,sans-serif;margin:2rem;color:#1e1e2f;background:#f5f6fa}"
        "h1,h2{color:#312e81}"
        ".meta{background:#fff;border-radius:8px;padding:1rem 1.5rem;margin-bottom:1.5rem;box-shadow:0 1px 4px rgba(0,0,0,.08)}"
        ".meta p{margin:.3rem 0}"
        ".summary{display:flex;gap:1rem;margin-bottom:1.5rem;flex-wrap:wrap}"
        ".card{background:#fff;border-radius:8px;padding:.8rem 1.4rem;box-shadow:0 1px 4px rgba(0,0,0,.08);min-width:110px;text-align:center}"
        ".card .num{font-size:1.8rem;font-weight:bold}"
        ".green{color:#16a34a}.red{color:#dc2626}"
        "table.case{width:100%;border-collapse:collapse;background:#fff;margin-bottom:2rem;box-shadow:0 1px 4px rgba(0,0,0,.08)}"
        "table.case th,table.case td{border:1px solid #ddd;padding:.5rem .8rem;text-align:left;vertical-align:top}"
        "table.case th{background:#eef2ff;width:180px}"
        ".pass{background:#dcfce7;color:#166534;font-weight:bold;padding:.1rem .6rem;border-radius:4px}"
        ".fail{background:#fee2e2;color:#991b1b;font-weight:bold;padding:.1rem .6rem;border-radius:4px}"
        "code{background:#f1f5f9;padding:.1rem .35rem;border-radius:4px;font-size:.9em}"
        "ol{margin:.2rem 0;padding-left:1.2rem}"
        "footer{color:#666;font-size:.85rem;margin-top:2rem}"
    )

    html_doc = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>TaskFlow Selenium Test Report</title>
<style>{css}</style>
</head>
<body>
<h1>TaskFlow — Selenium Test Report</h1>
<div class="meta">
  <p><strong>Generated:</strong> {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}</p>
  <p><strong>Suite:</strong> <code>selenium-tests/test_taskflow.py</code></p>
  <p><strong>Command:</strong> <code>python -m pytest selenium-tests/test_taskflow.py</code></p>
  <p><strong>Environment:</strong> {ENVIRONMENT}</p>
  <p><strong>Result: {verdict}</strong></p>
</div>
<div class="summary">
  <div class="card"><div class="num">{total}</div><div>Total</div></div>
  <div class="card"><div class="num green">{passed}</div><div>Passed</div></div>
  <div class="card"><div class="num red">{failed}</div><div>Failed</div></div>
  <div class="card"><div class="num">{blocked}</div><div>Blocked</div></div>
  <div class="card"><div class="num">{suite_time:.2f} s</div><div>Duration</div></div>
</div>
{''.join(sections)}
<footer>Machine-readable results: <code>test-results.xml</code> (same folder) · Auto-generated by <code>selenium-tests/conftest.py</code> after the test session.</footer>
</body>
</html>
"""
    path.write_text(html_doc, encoding="utf-8")

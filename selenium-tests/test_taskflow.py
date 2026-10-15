"""
TaskFlow Selenium E2E tests — covers TC01–TC05.

Mapping of the requested test cases to the REAL TaskFlow UI
(src/components/TaskForm.jsx, TaskList.jsx, Login.jsx):

  TC01 Add todo            -> Task title input + "Add Task" button
  TC02 Mark as completed   -> status <select> ("Change status for <title>") set to "Done".
                             (Spec says checkbox — app uses a dropdown instead.)
  TC03 Edit todo           -> App currently has NO working edit-text UI
                             (TaskList.jsx "Update" button calls undefined onUpdate).
                             So this test edits via the PUT /api/tasks/:id API, then
                             refreshes and asserts the new text is displayed + persisted.
  TC04 Delete todo         -> "Delete <title>" button (labelled "Deletes")
  TC05 Empty validation    -> HTML `required` + `if (!title.trim()) return;`
                             -> no new task, browser blocks submit.

Run:
  pip install -r requirements.txt
  # start backend (:5000) + frontend (:3000) first, then:
  pytest test_taskflow.py -v

Env overrides:
  TASKFLOW_URL      default http://localhost:3000
  TASKFLOW_API_URL  default http://localhost:5000
  TEST_EMAIL / TEST_PASSWORD  login account (must already exist via Register UI)
"""

import os
import time
import uuid

import pytest
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select, WebDriverWait

BASE_URL = os.getenv("TASKFLOW_URL", "http://localhost:3000")
API_URL = os.getenv("TASKFLOW_API_URL", "http://localhost:5000")
TEST_EMAIL = os.getenv("TEST_EMAIL", "selenium@test.com")
TEST_PASSWORD = os.getenv("TEST_PASSWORD", "password123")
TIMEOUT = 15


# ---------- helpers ----------

def unique_title(prefix="Selenium todo"):
    return f"{prefix} {uuid.uuid4().hex[:8]}"


def make_driver():
    opts = ChromeOptions()
    opts.add_argument("--headless=new")
    opts.add_argument("--no-sandbox")
    opts.add_argument("--disable-dev-shm-usage")
    opts.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=opts)


def login(driver, wait):
    """Log in via the API and inject the JWT into localStorage.

    NOTE: deliberate choice, not a shortcut. Driving the Login UI and then
    typing into the freshly-mounted task form hits a chromedriver/Chrome
    focus bug on this app (React swaps the whole tree after login: keystrokes
    reach no element, zero key/input events fire, even with click-first /
    ActionChains). API login + token injection avoids the broken state and is
    the standard pattern for E2E suites. The account must already exist
    (register once in the UI).
    """
    driver.get(BASE_URL)

    # If we are already logged in (token from a previous step), skip.
    if driver.find_elements(By.CSS_SELECTOR, "form.task-form"):
        return

    try:
        r = requests.post(f"{API_URL}/api/auth/login",
                          json={"email": TEST_EMAIL, "password": TEST_PASSWORD},
                          timeout=10)
        r.raise_for_status()
        token = r.json()["token"]
    except Exception as exc:
        pytest.fail(
            f"API login failed for {TEST_EMAIL}: {exc}. "
            "Register this account in the UI first or set TEST_EMAIL/TEST_PASSWORD."
        )

    driver.execute_script("localStorage.setItem('taskflow_token', arguments[0]);", token)
    driver.refresh()

    try:
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.task-form")))
    except Exception:
        pytest.fail("Task form did not appear after token injection; is the frontend running?")


def add_task_via_ui(driver, wait, title, description=""):
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.task-form")))
    title_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Task title"]')
    desc_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Task description"]')
    title_input.clear()
    title_input.send_keys(title)
    desc_input.clear()
    if description:
        desc_input.send_keys(description)
    driver.find_element(By.XPATH, "//form[contains(@class,'task-form')]//button[@type='submit']").click()
    # New task prepends to list — wait for its heading to appear.
    wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//ul[contains(@class,'task-list')]//h3[normalize-space()={_xq(title)}]")
    ))


def task_li(driver, title):
    return driver.find_element(
        By.XPATH, f"//ul[contains(@class,'task-list')]/li[.//h3[normalize-space()={_xq(title)}]]"
    )


def task_count(driver):
    return len(driver.find_elements(By.XPATH, "//ul[contains(@class,'task-list')]/li"))


def api_token():
    """Get a JWT for DB-level persistence assertions."""
    r = requests.post(f"{API_URL}/api/auth/login",
                      json={"email": TEST_EMAIL, "password": TEST_PASSWORD}, timeout=10)
    r.raise_for_status()
    return r.json()["token"]


def api_tasks():
    r = requests.get(f"{API_URL}/api/tasks",
                     headers={"Authorization": f"Bearer {api_token()}"}, timeout=10)
    r.raise_for_status()
    return r.json()


def _xq(s):
    """XPath-quoted string literal."""
    if "'" not in s:
        return f"'{s}'"
    return "concat('" + "', \"'\", '".join(s.split("'")) + "')"


# ---------- fixtures ----------

@pytest.fixture(scope="module")
def driver():
    d = make_driver()
    yield d
    d.quit()


@pytest.fixture(scope="module")
def wait(driver):
    return WebDriverWait(driver, TIMEOUT)


@pytest.fixture(scope="module", autouse=True)
def logged_in(driver, wait):
    login(driver, wait)


@pytest.fixture()
def fresh_title(driver, wait):
    """Creates one uniquely-named todo via the UI and returns its title."""
    title = unique_title()
    add_task_via_ui(driver, wait, title, description="selenium e2e")
    return title


# ---------- TC01–TC05 ----------

def test_TC01_add_new_todo(driver, wait):
    """TC01: Enter todo -> Add -> appears in list + stored in MongoDB."""
    title = unique_title("TC01 Buy milk")
    print(f"[TESTDATA] TC01 title={title!r}")
    add_task_via_ui(driver, wait, title)

    assert task_li(driver, title).is_displayed()

    titles_in_db = [t["title"] for t in api_tasks()]
    assert title in titles_in_db, "Todo visible in UI but NOT persisted in MongoDB"


def test_TC02_mark_todo_completed(driver, wait, fresh_title):
    """TC02: Set status dropdown to Done -> task-done styling + persisted."""
    print(f"[TESTDATA] TC02 target={fresh_title!r} new_status=done")
    li = task_li(driver, fresh_title)
    select_el = li.find_element(By.XPATH, ".//select")
    Select(select_el).select_by_value("done")

    # Wait for the re-rendered <li> to pick up the done style.
    wait.until(lambda d: "task-done" in task_li(d, fresh_title).get_attribute("class"))
    assert "task-done" in task_li(driver, fresh_title).get_attribute("class")

    match = [t for t in api_tasks() if t["title"] == fresh_title]
    assert match and match[0]["status"] == "done", "Status change not saved in MongoDB"


def test_TC03_edit_existing_todo(driver, wait, fresh_title):
    """TC03: Change todo text -> updated text displayed + persisted.

    NOTE: TaskList.jsx currently has no working edit UI (the "Update"
    button calls an undefined `onUpdate`), so the edit goes through the
    real PUT /api/tasks/:id endpoint, then we refresh and verify the UI.
    Once an inline Edit/Save UI exists, replace the API block with:
      li.find_element(edit_btn).click(); input.clear(); input.send_keys(new);
      save.click()
    """
    new_title = fresh_title + " [edited]"
    print(f"[TESTDATA] TC03 old={fresh_title!r} new={new_title!r}")
    token = api_token()
    current = next(t for t in api_tasks() if t["title"] == fresh_title)

    r = requests.put(f"{API_URL}/api/tasks/{current['_id']}",
                     headers={"Authorization": f"Bearer {token}"},
                     json={"title": new_title}, timeout=10)
    assert r.status_code == 200, f"PUT /api/tasks/:id failed: {r.text}"

    driver.refresh()
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.task-form")))
    wait.until(EC.presence_of_element_located(
        (By.XPATH, f"//ul[contains(@class,'task-list')]//h3[normalize-space()={_xq(new_title)}]")
    ))
    assert task_li(driver, new_title).is_displayed()

    assert any(t["title"] == new_title for t in api_tasks()), "Edit not persisted in MongoDB"


def test_TC04_delete_todo(driver, wait, fresh_title):
    """TC04: Delete -> disappears from UI + removed from MongoDB."""
    print(f"[TESTDATA] TC04 target={fresh_title!r}")
    li = task_li(driver, fresh_title)
    li.find_element(By.XPATH, ".//button[starts-with(@aria-label,'Delete')]").click()

    wait.until_not(EC.presence_of_element_located(
        (By.XPATH, f"//ul[contains(@class,'task-list')]//h3[normalize-space()={_xq(fresh_title)}]")
    ))
    assert not driver.find_elements(
        By.XPATH, f"//ul[contains(@class,'task-list')]//h3[normalize-space()={_xq(fresh_title)}]")

    # Give the DELETE request a moment, then confirm MongoDB no longer has it.
    deadline = time.time() + 10
    while time.time() < deadline:
        if all(t["title"] != fresh_title for t in api_tasks()):
            break
        time.sleep(1)
    assert all(t["title"] != fresh_title for t in api_tasks()), "Todo deleted in UI but still in MongoDB"


def test_TC05_empty_todo_rejected(driver, wait):
    """TC05: Empty input + Add -> no todo created (HTML5 required blocks submit)."""
    print("[TESTDATA] TC05 title=<empty> description=<empty>")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "form.task-form")))
    before = task_count(driver)

    title_input = driver.find_element(By.CSS_SELECTOR, 'input[aria-label="Task title"]')
    title_input.clear()  # leave empty
    driver.find_element(By.XPATH, "//form[contains(@class,'task-form')]//button[@type='submit']").click()

    time.sleep(1)  # allow any (incorrect) submission to render
    assert task_count(driver) == before, "Empty todo was added — validation missing"

    # The browser's built-in validation should flag the required input.
    assert title_input.get_attribute("validationMessage") != "", \
        "Expected a validation message for the empty required field"

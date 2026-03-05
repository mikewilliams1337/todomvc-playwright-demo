# todomvc-playwright-demo
Playwright + Python E2E testing demo (TodoMVC) with pytest, POM structure.

Automated tests for the following website: https://demo.playwright.dev/todomvc/#/

Tests cover the following requirements:

• A new todo item can be added using English text.
• A new todo item can be added using non-English characters.
• A new todo item can be added that includes numbers.
• A todo item can be marked as completed and appears correctly in the "Completed" view.
• A todo item can be deleted and no longer appears in any view.
• The "Active" filter correctly shows only items that are not completed.
• The "Completed" filter correctly shows only items that have been marked as completed.

## Getting Started

### 1. Install dependencies

Create and activate a virtual environment (if not already done):

```
python -m venv .venv
.venv\Scripts\Activate.ps1  # PowerShell (Windows)
# or
source .venv/bin/activate   # Bash (Linux/macOS)
```

Install required packages:

```
pip install -r requirements.txt
```

Install Playwright browsers:

```
.venv\Scripts\python.exe -m playwright install chromium
```

### 2. Run all tests

```
pytest -v
```
Or, if you want to use the venv's python directly:
```
.venv\Scripts\python.exe -m pytest -v
```

#### Optional: Run with browser UI or slow motion
- To see the browser UI: `pytest --headed`
- To slow down actions for debugging: `pytest --slowmo=500`
- Combine both: `pytest --headed --slowmo=500`

You can use these flags with any test run command above.

### 3. Run a specific test file

```
pytest -v tests/test_add_new_todo_en.py
```


### 4. Run smoke or prompt-based tests separately

If you want to run the smoke test or the prompt-based test (which are excluded from the main test run), use:

```
pytest -v tests/smokeTest.py
```

or for the prompt-based test (allowing interactive input):

```
pytest -s -v tests/prompt_new_editTest.py
```

You can also run them with the venv's python directly:

```
.venv\Scripts\python.exe -m pytest -v tests/smokeTest.py
.venv\Scripts\python.exe -m pytest -s -v tests/prompt_new_editTest.py
```

---

- All tests are located in the `tests/` directory.
- The project uses the Page Object Model (POM) pattern in the `pages/` directory.
- See test files for more usage examples.

## Additional Notes & Troubleshooting

- **Python version:** This project requires Python 3.8 or newer.
- **First run:** The first time you run Playwright, it will download the required browser binaries.
- **Prompt-based test:** The prompt-based test (`prompt_new_editTest.py`) requires user input and is not suitable for automated CI runs.
- **Windows Execution Policy:** If you get a policy error when activating the venv, run:
  ```
  Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
  ```
  in PowerShell.
- **Update Playwright browsers:** If you need to update the browsers, run:
  ```
  .venv\Scripts\python.exe -m playwright install chromium
  ```
- **Troubleshooting:** If you see errors about missing packages or browsers, ensure your venv is activated and all install steps above have been completed.

## Pytest Command Flags Key

- `-m` : Run library module as a script (e.g., `python -m pytest`).
- `-v` : Verbose output—shows each test name and result.
- `-s` : Disable output capture—allows interactive input/output (needed for prompt-based tests).
- `-r` : Show extra summary info for skipped, failed, or xfailed tests (e.g., `-rA` for all).
- `--headed` : Run browser in headed (UI) mode (custom flag for this project).
- `--slowmo` : Slow down Playwright actions by N milliseconds (custom flag for this project).

You can combine these flags as needed in your test commands.

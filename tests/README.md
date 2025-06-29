# Tests for Notebook-LM Audio2YouTube

This directory contains unit tests for the core functions in `audio2yt_app.py`.

## Structure

- Each function in the main app has a corresponding test.
- Tests use `pytest` and `unittest.mock` for mocking external dependencies (e.g., subprocess, OpenAI, Streamlit, YouTube API).
- Temporary files and directories are used for safe, isolated testing.

## Running the Tests

Activate your virtual environment and run:

```bash
PYTHONPATH=. pytest tests/ --maxfail=3 --disable-warnings -v
```

## Adding New Tests

- Place new test files in this directory, prefixed with `test_`.
- Use `pytest` style: functions named `test_*`.
- Mock all external APIs and side effects.
- Use fixtures for setup/teardown if needed.

## Best Practices

- Keep tests fast and isolated.
- Cover both success and failure cases.
- Document any non-obvious test logic with comments.
- If you add a new feature, add or update tests!

## Need Help?

Open an issue or ask in your PR—contributors are happy to help!

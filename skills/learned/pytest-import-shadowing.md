---
name: pytest-import-shadowing
description: "Fix ModuleNotFoundError in pytest when test directory shadows source package with __init__.py"
user-invocable: false
origin: auto-extracted
---

# Pytest Import Shadowing by Test Directory

**Extracted:** 2026-04-14
**Context:** When pytest tests fail with ModuleNotFoundError despite correct sys.path configuration

## Problem

Pytest tests fail with `ModuleNotFoundError` or `ImportError: cannot import name 'X' from 'package'` even when:
- The package exists in `src/package/`
- `conftest.py` correctly adds `src/` to `sys.path`
- Direct Python imports work: `python -c "import sys; sys.path.insert(0, 'src'); from package import X"`
- The error message shows pytest importing from `tests/package/__init__.py` instead of `src/package/__init__.py`

**Example error:**
```
ImportError: cannot import name 'MyClass' from 'my_package' (/path/to/project/tests/my_package/__init__.py)
```

Note the path points to `tests/` instead of `src/`.

## Root Cause

Python's import system finds `tests/my_package/__init__.py` **before** `src/my_package/__init__.py` because:

1. Pytest adds the test directory to `sys.path` automatically
2. When a test directory has the same name as a source package AND contains `__init__.py`, Python treats it as the package
3. The empty or minimal `__init__.py` in tests shadows the real package in `src/`

This happens even with `sys.path.insert(0, 'src')` in conftest.py because pytest's own path manipulation runs first.

## Solution

**Remove `__init__.py` from test directories that match source package names:**

```bash
# If you have:
src/my_package/__init__.py       # ← Keep this
tests/my_package/__init__.py     # ← DELETE this

# After removal:
src/my_package/__init__.py       # ← Source package
tests/my_package/                # ← Just a directory (not a package)
  test_module.py
  test_another.py
```

Test files can still import from the source package normally:
```python
# tests/my_package/test_module.py
from my_package import MyClass  # Works! Imports from src/my_package/
```

## When to Use

**Trigger conditions:**
- Pytest import errors showing test directory path in error message
- `conftest.py` has correct `sys.path` setup but imports still fail
- Error message: `cannot import name 'X' from 'package' (/path/tests/package/__init__.py)`
- Test directory name matches source package name

**Diagnostic command:**
```bash
# Check if test directory has __init__.py shadowing source
find tests -name "__init__.py" -exec echo {} \;
# If any match source package names in src/, remove them
```

## Related Patterns

- Pytest does NOT require `__init__.py` in test directories (since pytest 3.0+)
- Use `__init__.py` in tests only for shared fixtures/utilities, and name the directory differently (e.g., `tests/helpers/`)
- For namespace packages, prefer `src/` layout with `conftest.py` path configuration over placing packages directly in root

## Example Fix Sequence

```bash
# 1. Identify the issue
pytest tests/my_package/test_module.py
# ImportError: cannot import name 'X' from 'my_package' (/path/tests/my_package/__init__.py)

# 2. Remove shadowing __init__.py
rm tests/my_package/__init__.py

# 3. Verify fix
pytest tests/my_package/test_module.py
# ✓ Imports now resolve to src/my_package/
```

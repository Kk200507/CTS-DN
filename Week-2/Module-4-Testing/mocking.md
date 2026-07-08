# Mocking and Test Doubles

In unit testing, we want to isolate the code under test from external dependencies (such as APIs, databases, or complex calculations) to ensure tests are fast, predictable, and simple. We achieve this isolation using **Test Doubles**.

---

## 1. Types of Test Doubles (Gerard Meszaros Classification)

| Type | Description |
|---|---|
| **Dummy** | Passed around but never actually used. Typically used just to fill parameter lists. |
| **Stub** | Provides pre-determined, hardcoded answers to calls made during the test. Doesn't respond to anything else. |
| **Spy** | A stub that also records details of how it was called (e.g., number of times called, arguments received). |
| **Mock** | Pre-programmed with expectations (e.g., "object must be called with argument X"). Can automatically fail a test if expectations aren't met. |
| **Fake** | Has a working implementation, but usually takes shortcut routes that make it unsuitable for production (e.g., an In-Memory SQLite database instead of PostgreSQL). |

---

## 2. Mocking in Python (`unittest.mock`)

Python includes a powerful built-in mocking library.

### Key Tools:
- **`Mock`**: Create placeholder objects. You can dynamically set attributes and return values.
- **`MagicMock`**: A subclass of `Mock` that implements default magic methods (like `__len__`, `__str__`, `__iter__`). This is the default choice for most mocking needs.
- **`patch`**: A helper that intercepts import lookups, allowing you to temporarily replace classes or functions in a specific module.

### Python Example: Mocking an API Call
```python
# target_code.py
import requests

def get_github_username(user_id):
    response = requests.get(f"https://api.github.com/users/{user_id}")
    if response.status_code == 200:
        return response.json()["login"]
    return None
```

```python
# test_code.py
import unittest
from unittest.mock import patch, MagicMock
from target_code import get_github_username

class TestGitHubAPI(unittest.TestCase):
    # Patch requests.get so no real HTTP request is sent
    @patch('target_code.requests.get')
    def test_get_github_username_success(self, mock_get):
        # 1. Arrange: setup mock response object
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"login": "octocat"}
        mock_get.return_value = mock_response

        # 2. Act
        username = get_github_username("octocat")

        # 3. Assert
        self.assertEqual(username, "octocat")
        mock_get.assert_called_once_with("https://api.github.com/users/octocat")
```

---

## 3. Mocking in JavaScript

### A. Jest Mocks
Jest provides native functions to mock files, modules, and individual callbacks:

```javascript
// Mocking a module
jest.mock('axios');
import axios from 'axios';

test('should fetch users', () => {
  axios.get.mockResolvedValue({ data: { name: 'Bob' } });
  // Call your code that triggers axios.get
});
```

### B. Sinon.js (Commonly used with Mocha)
Since Mocha is just a test runner and has no built-in mocking utility, Javascript developers use **Sinon.js** to create spies, stubs, and mocks:

```javascript
const sinon = require('sinon');
const api = require('./my_api');

// Create a stub that returns a fixed value
const stub = sinon.stub(api, 'fetchData').returns('mocked_data');
```

---

## 4. The Pitfalls of Over-Mocking

While mocking is highly useful, excessive mocking is a common anti-pattern that leads to low-quality test suites.

1. **False Confidence**: If you mock everything, you are testing your assumptions about the system, not the actual system. Your tests might pass even if the real modules are completely incompatible.
2. **Brittle Tests**: Over-mocking binds your tests directly to the internal implementation details of your code. If you refactor a function's internals without changing its input/output, your tests will break because the mocked calls changed.
3. **High Maintenance**: Maintaining complex mock configurations makes codebase refactoring tedious and frustrating.

> [!TIP]
> **Mock at boundaries**: Mock external services (third-party APIs, databases, payment gateways) and system resources (email servers, file systems). Prefer using real domain logic, utilities, and helper functions in tests instead of mocking them.

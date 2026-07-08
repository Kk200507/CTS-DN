# Testing Fundamentals

Testing is a core practice in software engineering that ensures code behaves as expected, prevents regressions, and serves as living documentation.

---

## 1. The Testing Pyramid

The testing pyramid represents the ideal distribution of different test types in a healthy test suite.

```
       / \
      /   \      End-to-End (E2E) (Fewest, slowest, highest cost)
     / E2E \
    /-------\
   /         \   Integration Tests (Medium count, medium speed)
  /  Integr  \
 /-------------\
/               \ Unit Tests (Most numerous, fastest, lowest cost)
/     Unit      \
/_______________\
```

### A. Unit Tests
- **Scope**: Tests the smallest testable parts of an application (e.g., a single function, method, or class) in isolation from external dependencies.
- **Speed**: Extremely fast (milliseconds).
- **Cost**: Low execution and maintenance cost.
- **Example**: Testing that a `calculate_tax()` function returns the correct amount for a given input.

### B. Integration Tests
- **Scope**: Verifies that two or more components work together (e.g., database interactions, API endpoints, file system access).
- **Speed**: Slower (seconds).
- **Cost**: Medium cost.
- **Example**: Testing that an API endpoint successfully retrieves a user record from a running database.

### C. End-to-End (E2E) Tests
- **Scope**: Tests the entire application workflow from the user's perspective, simulating real user interactions (usually involving UI and backend).
- **Speed**: Very slow (seconds to minutes).
- **Cost**: High cost, high maintenance, prone to flakiness.
- **Example**: Simulating a user logging in, adding items to a cart, checking out, and verifying a confirmation email is received.

---

## 2. The Arrange-Act-Assert (AAA) Pattern

AAA is a clean code structure pattern for writing readable and structured test cases.

- **Arrange**: Set up the testing environment, inputs, and mock dependencies.
- **Act**: Execute the function or method being tested.
- **Assert**: Verify that the output match the expected behavior.

### Python Example
```python
def test_user_registration():
    # 1. Arrange
    user_data = {"username": "test_user", "email": "test@example.com"}
    service = UserService()
    
    # 2. Act
    new_user = service.register(user_data)
    
    # 3. Assert
    assert new_user.username == "test_user"
    assert new_user.id is not None
```

---

## 3. Boundary Conditions and Edge Cases

When designing test cases, focusing on basic inputs is not enough. You must test input boundaries where errors frequently occur.

### The Boundary Value Analysis (BVA) Guidelines
If a function accepts inputs between `min` and `max` (e.g., age from `18` to `65`):
- **Just below boundary**: `17` (Invalid)
- **Boundary**: `18` (Valid)
- **Just above boundary**: `19` (Valid)
- **Nominal value**: `30` (Valid)
- **Boundary**: `65` (Valid)
- **Just above boundary**: `66` (Invalid)

### Typical Edge Cases:
- **Numbers**: `0`, negative numbers, extremely large values, floating point precision limits.
- **Strings**: Empty strings (`""`), strings with special characters, emojis, extremely long inputs, `null`/`None`.
- **Collections**: Empty arrays, duplicates in arrays, unsorted arrays, index out of bounds.

---

## 4. Manual vs. Automated Testing & Regression Testing

### Manual vs. Automated Testing
- **Manual Testing**: A human steps through the application to find bugs. Essential for exploratory testing, UX evaluations, and early prototyping. However, it is slow, error-prone, and doesn't scale.
- **Automated Testing**: Scripts execute tests and verify results automatically. Essential for continuous integration, speed, scalability, and repeatability.

### Regression Testing
A **regression** is a bug that appears in a feature that was previously working, often introduced by new code additions or refactoring.
- **Regression Testing** is the practice of running the entire suite of automated tests after code changes to guarantee that existing functionalities have not broken.

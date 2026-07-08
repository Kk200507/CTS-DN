# Code Coverage

Code Coverage is a measurement metric that shows what percentage of your source code is executed when your automated test suite runs. It helps identify untested sections of your application.

---

## 1. Core Coverage Metrics

Not all coverage is created equal. Testing tools measure coverage at different levels of granularity:

### A. Statement Coverage
- Measures whether each individual line (or statement) of code was executed at least once during tests.
- **Limitation**: Highly superficial. It does not account for complex branching logic.

### B. Branch Coverage
- Measures whether every decision branch (e.g., the `True` and `False` paths of an `if` statement) has been executed.
- **Example**:
  ```python
  def check_status(active, premium):
      if active and premium: # Two conditions, multiple branches
          return "Premium Active"
      return "Inactive or Standard"
  ```
  Statement coverage might check one line, but branch coverage ensures both the true outcome and the false outcome of the condition are fully executed.

### C. Path Coverage
- Measures whether every unique path through a function (all combinations of branches) is executed.
- Highly thorough, but can lead to a combinatorial explosion of paths, making 100% path coverage impractical for complex functions.

---

## 2. Coverage Tools

### Python: `coverage.py`
`coverage.py` is the standard tool for measuring code coverage of Python programs. It integrates seamlessly with PyTest.

#### Installation
```bash
pip install coverage pytest-cov
```

#### Running Coverage
```bash
# Run tests and output terminal coverage report
pytest --cov=my_project tests/

# Generate an HTML interactive report
coverage html
```
*This creates a `htmlcov/` directory containing an interactive webpage highlighting which exact lines were executed and which were missed.*

---

### JavaScript: `nyc` (Istanbul) & Jest
- **Jest**: Includes coverage tracking out of the box using Istanbul underneath.
  ```bash
  jest --coverage
  ```
- **Mocha**: Typically paired with `nyc` (the command-line interface for Istanbul).
  ```bash
  npm install nyc --save-dev
  nyc mocha tests/
  ```

---

## 3. The 100% Coverage Trap

A common trap in software engineering is treating **100% Code Coverage** as a metric for test quality.

> [!WARNING]
> High coverage does **not** equal high-quality tests.
> - Coverage measures which lines were *executed*, not whether the *assertions* verify correct behavior.
> - A test can execute a line of code, but if it lacks assertions, bugs on that line will still go completely unnoticed.

### Example: 100% Statement Coverage, 0% Bug Detection
```python
def divide(a, b):
    return a / b

# Test:
def test_divide():
    divide(10, 2) # Executes the statement, but makes no assertions!
```
This test yields 100% statement coverage for the `divide` function. However:
1. It does not check if the return value is correct (`5`).
2. It fails to test the edge case of division by zero (`b = 0`), which would crash the system.

### Best Practice Recommendations:
- Aim for a reasonable target (e.g., **80% to 90%** coverage).
- Focus coverage efforts on **critical business logic**, algorithms, and data transformation functions rather than trivial code (like basic getters, setters, or routing setups).
- Combine coverage metrics with peer code reviews and boundary testing to ensure assertions are actually meaningful.

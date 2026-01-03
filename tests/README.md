# VitalTrack Selenium Tests

This directory contains Selenium-based end-to-end tests for the VitalTrack application.

## Setup

### Prerequisites
- Python 3.7 or higher
- Chrome browser installed
- pip (Python package manager)

### Installation

1. Install test dependencies:
```bash
pip install -r tests/requirements.txt
```

This will install:
- selenium (WebDriver for browser automation)
- pytest (Testing framework)
- pytest-html (HTML test reports)
- webdriver-manager (Automatic ChromeDriver management)

## Running Tests

### Run Optimized (Parallel - Recommended)
The fastest way to run the full suite is in parallel using multiple CPU cores:
```bash
pytest tests/ -n auto --dist loadfile
```

### Run All (Sequential)
```bash
pytest tests/
```

### Run Specific Test File
```bash
pytest tests/test_navigation.py
pytest tests/test_meal_logging.py
pytest tests/test_symptom_logging.py
pytest tests/test_trends.py
pytest tests/test_data_management.py
```

### Run Tests by Marker

Run only smoke tests (quick, critical tests):
```bash
pytest tests/ -m smoke
```

Run only UI tests:
```bash
pytest tests/ -m ui
```

Run regression tests:
```bash
pytest tests/ -m regression
```

### Run with Verbose Output
```bash
pytest tests/ -v
```

### Run with HTML Report
```bash
pytest tests/ --html=tests/report.html --self-contained-html
```

The report will be generated at `tests/report.html`.

### Run Tests with Visible Browser (for debugging)

By default, tests run in headless mode. To see the browser during test execution, modify the `conftest.py` fixture or use the `driver_visible` fixture in your tests.

## Test Structure

```
tests/
├── conftest.py              # Shared fixtures and configuration
├── requirements.txt         # Python dependencies
├── test_navigation.py       # Navigation between views
├── test_meal_logging.py     # Meal entry functionality
├── test_symptom_logging.py  # Symptom entry functionality
├── test_trends.py          # Trends chart and correlation analysis
└── test_data_management.py # Data export and persistence
```

## Test Coverage

### Navigation Tests (`test_navigation.py`)
- ✅ Initial view is dashboard
- ✅ Navigate to all views (Logs, Symptoms, Trends, Data Management)
- ✅ Multiple view navigation sequence
- ✅ Active navigation state

### Meal Logging Tests (`test_meal_logging.py`)
- ✅ Open/close meal modal
- ✅ Log basic meal
- ✅ Log meal with ingredients
- ✅ Meal name validation (required field)
- ✅ Multiple meals logging

### Symptom Logging Tests (`test_symptom_logging.py`)
- ✅ Open symptom modal
- ✅ Log basic symptom
- ✅ All symptom types (energy, passing_gas, acidity, burping, pain, headache, mood, constipation)
- ✅ Severity levels (1-10)
- ✅ Chest pain symptoms (left, right, middle)
- ✅ Rib pain symptoms (left, right)

### Trends Tests (`test_trends.py`)
- ✅ Trends view loads
- ✅ Symptom chart renders
- ✅ Root cause analyzer dropdown
- ✅ Correlation analysis with data
- ✅ Ingredient-level correlation
- ✅ Empty state handling
- ✅ No correlations found message

### Data Management Tests (`test_data_management.py`)
- ✅ Data management view loads
- ✅ Export button exists
- ✅ Export functionality
- ✅ Data persistence in localStorage
- ✅ Clear storage behavior
- ✅ Dashboard stats update

## Configuration

### Browser Options
Tests are configured to run in headless Chrome by default. You can modify the browser options in `conftest.py`:

```python
chrome_options = Options()
chrome_options.add_argument("--headless")  # Remove this line to see browser
chrome_options.add_argument("--window-size=1920,1080")
```

### Test Markers
Available markers (defined in `pytest.ini`):
- `@pytest.mark.smoke` - Quick smoke tests
- `@pytest.mark.regression` - Full regression tests
- `@pytest.mark.ui` - UI interaction tests

## Troubleshooting

### ChromeDriver Issues
If you encounter ChromeDriver issues, the `webdriver-manager` package should automatically download the correct version. If problems persist:

1. Update webdriver-manager:
```bash
pip install --upgrade webdriver-manager
```

2. Clear the webdriver cache:
```bash
python -c "from webdriver_manager.chrome import ChromeDriverManager; ChromeDriverManager().install()"
```

### Test Failures
- Check that the application files (`index.html`, `js/`, `style.css`) are in the correct location
- Ensure Chrome browser is installed and up to date
- Review the HTML test report for detailed error messages
- Run tests with `-v` flag for verbose output

### Slow Tests
If tests are running slowly:
- Reduce wait times in tests (currently using WebDriverWait with 10s timeout)
- Run tests in parallel using `pytest-xdist`:
  ```bash
  pip install pytest-xdist
  pytest tests/ -n auto
  ```

## Contributing

When adding new tests:
1. Follow the existing test structure and naming conventions
2. Use appropriate markers (`@pytest.mark.smoke`, `@pytest.mark.ui`, etc.)
3. Add proper docstrings to test functions
4. Use WebDriverWait for element interactions instead of hard-coded sleeps where possible
5. Clean up test data in teardown or use fixtures

## CI/CD Integration

These tests can be integrated into CI/CD pipelines. Example GitHub Actions workflow:

```yaml
name: Selenium Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Install dependencies
        run: pip install -r tests/requirements.txt
      - name: Run tests
        run: pytest tests/ --html=report.html --self-contained-html
      - name: Upload test report
        uses: actions/upload-artifact@v2
        if: always()
        with:
          name: test-report
          path: report.html
```

"""
Enhanced conftest.py with screenshot capture on test failure
"""
import pytest
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# Create screenshots directory
SCREENSHOT_DIR = os.path.join(os.path.dirname(__file__), "screenshots")
os.makedirs(SCREENSHOT_DIR, exist_ok=True)


@pytest.fixture(scope="session")
def base_url():
    """Base URL for the application"""
    # Get the absolute path to index.html
    current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(current_dir, "index.html")
    return f"file:///{index_path.replace(os.sep, '/')}"


@pytest.fixture(scope="function")
def driver(base_url, request):
    """Create and configure Chrome WebDriver"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--window-size=1920,1080")
    
    # Initialize the driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    # Navigate to the application
    driver.get(base_url)
    
    # Clear localStorage before each test
    driver.execute_script("localStorage.clear();")
    driver.refresh()
    
    yield driver
    
    # Capture screenshot on test failure
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved: {screenshot_path}")
    
    # Cleanup
    driver.quit()


@pytest.fixture(scope="function")
def driver_visible(base_url, request):
    """Create Chrome WebDriver with visible browser (for debugging)"""
    chrome_options = Options()
    chrome_options.add_argument("--window-size=1920,1080")
    
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)
    
    driver.get(base_url)
    driver.execute_script("localStorage.clear();")
    driver.refresh()
    
    yield driver
    
    # Capture screenshot on test failure
    if request.node.rep_call.failed:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        test_name = request.node.name
        screenshot_path = os.path.join(SCREENSHOT_DIR, f"{test_name}_{timestamp}.png")
        driver.save_screenshot(screenshot_path)
        print(f"\nScreenshot saved: {screenshot_path}")
    
    driver.quit()


@pytest.fixture
def clear_storage(driver):
    """Clear localStorage and sessionStorage"""
    driver.execute_script("localStorage.clear();")
    driver.execute_script("sessionStorage.clear();")
    driver.refresh()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Hook to capture test results for screenshot on failure"""
    outcome = yield
    rep = outcome.get_result()
    setattr(item, "rep_" + rep.when, rep)


def pytest_configure(config):
    """Create screenshots directory at test session start"""
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)

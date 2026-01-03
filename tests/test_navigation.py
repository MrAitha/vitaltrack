"""
Test navigation between different views in VitalTrack
"""
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.smoke
@pytest.mark.ui
class TestNavigation:
    """Test suite for navigation functionality"""
    
    def test_initial_view_is_dashboard(self, driver):
        """Verify that the application loads with dashboard view"""
        wait = WebDriverWait(driver, 10)
        title = wait.until(EC.presence_of_element_located((By.ID, "view-title")))
        assert title.text == "Dashboard", "Initial view should be Dashboard"
    
    def test_navigate_to_logs(self, driver):
        """Test navigation to Logs view"""
        wait = WebDriverWait(driver, 10)
        
        # Click on Logs navigation button
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Verify view changed
        title = driver.find_element(By.ID, "view-title")
        assert title.text == "Logs", "View should change to Logs"
    
    def test_navigate_to_symptoms(self, driver):
        """Test navigation to Symptoms view"""
        wait = WebDriverWait(driver, 10)
        
        symptoms_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_btn.click()
        
        title = driver.find_element(By.ID, "view-title")
        assert title.text == "Symptoms", "View should change to Symptoms"
    
    def test_navigate_to_trends(self, driver):
        """Test navigation to Trends view"""
        wait = WebDriverWait(driver, 10)
        
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        title = driver.find_element(By.ID, "view-title")
        assert title.text == "Trends", "View should change to Trends"
    
    def test_navigate_to_data_management(self, driver):
        """Test navigation to Data Management view"""
        wait = WebDriverWait(driver, 10)
        
        data_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="data"]'))
        )
        data_btn.click()
        
        title = driver.find_element(By.ID, "view-title")
        assert title.text == "Data", "View should change to Data"
    
    def test_navigation_between_multiple_views(self, driver):
        """Test navigating between multiple views in sequence"""
        wait = WebDriverWait(driver, 10)
        
        views = ["logs", "symptoms", "trends", "data", "dashboard"]
        expected_titles = ["Logs", "Symptoms", "Trends", "Data", "Dashboard"]
        
        for view, expected_title in zip(views, expected_titles):
            btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, f'[data-view="{view}"]'))
            )
            btn.click()
            
            title = driver.find_element(By.ID, "view-title")
            assert title.text == expected_title, f"View should be {expected_title}"
    
    def test_active_nav_state(self, driver):
        """Test that active navigation button has correct styling"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to logs
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Check that logs button has active class
        assert "active" in logs_btn.get_attribute("class"), \
            "Active navigation button should have 'active' class"

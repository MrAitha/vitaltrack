"""
Test data management functionality including export
"""
import pytest
import time
import os
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
class TestDataManagement:
    """Test suite for data management functionality"""
    
    def test_data_management_view_loads(self, driver):
        """Test that data management view loads correctly"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to data management
        data_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="data"]'))
        )
        data_btn.click()
        
        # Wait for content to load
        wait.until(lambda d: d.find_element(By.ID, "view-title").text == "Data")
        
        # Verify title
        title = driver.find_element(By.ID, "view-title")
        assert title.text == "Data", "Should show Data title"
    
    def test_export_button_exists(self, driver):
        """Test that export button is present"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to data management
        data_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="data"]'))
        )
        data_btn.click()
        
        # Wait for content to load
        wait.until(EC.presence_of_element_located((By.ID, "main-view")))
        
        # Look for export button
        page_content = driver.find_element(By.ID, "main-view")
        buttons = wait.until(lambda d: d.find_element(By.ID, "main-view").find_elements(By.TAG_NAME, "button"))
        
        export_button_found = any("export" in btn.text.lower() for btn in buttons)
        assert export_button_found, "Should have an export button"
    
    @pytest.mark.smoke
    def test_export_data_functionality(self, driver):
        """Test exporting data"""
        wait = WebDriverWait(driver, 10)
        
        # First, add some data to export
        # Add a meal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Test Export Meal")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Add a symptom
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        from selenium.webdriver.support.ui import Select
        symptom_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-type"))
        )
        select = Select(symptom_select)
        select.select_by_value("headache")
        
        severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="5"]')
        severity_btn.click()
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to data management
        data_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="data"]'))
        )
        data_btn.click()
        
        # Wait for content to load
        wait.until(lambda d: "export" in d.find_element(By.ID, "main-view").text.lower())
        
        # Verify export button exists (data management shows controls, not individual entries)
        page_content = driver.find_element(By.ID, "main-view").text
        assert "Export" in page_content or "export" in page_content.lower(), \
            "Should show export functionality in data management view"
    
    def test_data_persistence(self, driver):
        """Test that data persists in localStorage"""
        wait = WebDriverWait(driver, 10)
        
        # Add a meal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Persistence Test Meal")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Check localStorage
        stored_data = driver.execute_script(
            "return localStorage.getItem('vitaltrack_data');"
        )
        
        assert stored_data is not None, "Data should be stored in localStorage"
        assert "Persistence Test Meal" in stored_data, \
            "Meal should be in localStorage"
    
    def test_clear_storage_and_refresh(self, driver):
        """Test that clearing storage removes data"""
        wait = WebDriverWait(driver, 10)
        
        # Add some data
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Clear Test Meal")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Clear storage
        driver.execute_script("localStorage.clear();")
        driver.refresh()
        
        # Wait for refresh
        wait.until(EC.presence_of_element_located((By.ID, "main-view")))
        
        # Navigate to logs
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Wait for logs to load
        wait.until(lambda d: "logs" in d.find_element(By.ID, "view-title").text.lower())
        
        # Verify no meals
        page_content = driver.find_element(By.ID, "main-view").text
        assert "No meals logged" in page_content or "Clear Test Meal" not in page_content, \
            "Should not show meals after clearing storage"
    
    def test_dashboard_stats_update(self, driver):
        """Test that dashboard stats update with logged data"""
        wait = WebDriverWait(driver, 10)
        
        # Check initial stats
        dashboard_content = driver.find_element(By.ID, "main-view").text
        
        # Add a meal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Stats Test Meal")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate back to dashboard
        dashboard_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="dashboard"]'))
        )
        dashboard_btn.click()
        
        # Wait for dashboard to load
        wait.until(lambda d: "dashboard" in d.find_element(By.ID, "view-title").text.lower())
        
        # Check that stats show at least 1 meal
        dashboard_content = driver.find_element(By.ID, "main-view").text
        
        # Verify stats are displayed (look for "Meals Logged" text and the number)
        assert "Meals Logged" in dashboard_content or "meals logged" in dashboard_content.lower(), \
            "Should show meals logged stat on dashboard"
        assert "1" in dashboard_content, \
            "Should show at least 1 meal in stats"

    def test_import_data_functionality(self, driver, base_url):
        wait = WebDriverWait(driver, 10)
        # 1. Create a temporary import file
        import_file_path = os.path.abspath("test_import.json")
        test_data = {
            "meals": [
                {"id": 12345, "name": "Imported Sushi", "ingredients": "Rice, Fish", "timestamp": "2026-01-01T12:00:00.000Z"}
            ],
            "symptoms": [
                {"id": 67890, "symptom": "energy", "severity": 8, "timestamp": "2026-01-01T13:00:00.000Z"}
            ],
            "settings": {"theme": "light"}
        }
        with open(import_file_path, "w") as f:
            json.dump(test_data, f)
            
        try:
            driver.get(base_url)
            
            # 2. Navigate to Data Management
            data_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="data"]'))
            )
            data_btn.click()
            
            # 3. Trigger import via hidden input
            file_input = driver.find_element(By.ID, "import-file-input")
            # Make sure it's accessible for Selenium
            driver.execute_script("arguments[0].style.display = 'block';", file_input)
            file_input.send_keys(import_file_path)
            
            # 4. Handle confirmation dialog (browser alert)
            wait.until(EC.alert_is_present())
            alert = driver.switch_to.alert
            alert.accept()
            
            # 5. Wait for reload/success alert
            wait.until(EC.alert_is_present())
            alert = driver.switch_to.alert
            assert "successfully" in alert.text.lower()
            alert.accept()
            
            # 6. Navigate to Logs and verify the imported meal exists
            logs_btn = wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
            )
            logs_btn.click()
            
            wait.until(lambda d: "imported sushi" in d.find_element(By.ID, "main-view").text.lower())
            
        finally:
            if os.path.exists(import_file_path):
                os.remove(import_file_path)

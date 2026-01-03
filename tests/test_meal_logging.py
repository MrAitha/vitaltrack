"""
Test meal logging functionality
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@pytest.mark.ui
class TestMealLogging:
    """Test suite for meal logging functionality"""
    
    def test_open_meal_modal(self, driver):
        """Test opening the meal logging modal"""
        wait = WebDriverWait(driver, 10)
        
        # Click quick meal button
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        # Verify modal is visible
        modal = wait.until(
            EC.visibility_of_element_located((By.ID, "modal-container"))
        )
        assert "hidden" not in modal.get_attribute("class"), \
            "Modal should be visible"
        
        # Verify modal contains meal form
        assert "Log Meal" in modal.text, "Modal should contain meal form"
    
    def test_close_meal_modal(self, driver):
        """Test closing the meal modal"""
        wait = WebDriverWait(driver, 10)
        
        # Open modal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        # Click close button
        close_btn = wait.until(
            EC.element_to_be_clickable((By.CLASS_NAME, "close-btn"))
        )
        close_btn.click()
        
        # Verify modal is hidden
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        modal = driver.find_element(By.ID, "modal-container")
        assert "hidden" in modal.get_attribute("class"), \
            "Modal should be hidden after closing"
    
    @pytest.mark.smoke
    def test_log_meal_basic(self, driver):
        """Test logging a basic meal"""
        wait = WebDriverWait(driver, 10)
        
        # Open meal modal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        # Fill in meal name
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Test Pizza")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to logs to verify meal was saved
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Verify meal appears in logs
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "Test Pizza" in d.find_element(By.ID, "main-view").text)
        assert "Test Pizza" in main_view.text, "Logged meal should appear in logs"
    
    def test_log_meal_with_ingredients(self, driver):
        """Test logging a meal with ingredients"""
        wait = WebDriverWait(driver, 10)
        
        # Open meal modal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        # Fill in meal details
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Chicken Salad")
        
        ingredients_input = driver.find_element(By.ID, "meal-ingredients")
        ingredients_input.send_keys("Chicken, Lettuce, Tomato, Olive Oil")
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to logs
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Verify meal and ingredients appear in logs
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "Chicken Salad" in d.find_element(By.ID, "main-view").text)
        page_content = main_view.text
        assert "Chicken Salad" in page_content, "Meal name should appear in logs"
        assert "Chicken" in page_content or "Lettuce" in page_content, \
            "Ingredients should appear in logs"
    
    def test_meal_requires_name(self, driver):
        """Test that meal name is required"""
        wait = WebDriverWait(driver, 10)
        
        # Open meal modal
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        # Try to submit without entering name
        submit_btn = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#meal-form button[type='submit']"))
        )
        
        # Check if input has required attribute
        meal_name_input = driver.find_element(By.ID, "meal-name")
        assert meal_name_input.get_attribute("required") is not None, \
            "Meal name input should be required"
    
    def test_multiple_meals_logged(self, driver):
        """Test logging multiple meals"""
        wait = WebDriverWait(driver, 10)
        
        meals = ["Breakfast Oatmeal", "Lunch Sandwich", "Dinner Pasta"]
        
        for meal_name in meals:
            # Open modal
            meal_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
            )
            meal_btn.click()
            
            # Fill and submit
            meal_name_input = wait.until(
                EC.presence_of_element_located((By.ID, "meal-name"))
            )
            meal_name_input.send_keys(meal_name)
            
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
            submit_btn.click()
            
            # Wait for modal to close before next loop
            wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to logs
        logs_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="logs"]'))
        )
        logs_btn.click()
        
        # Wait for logs to load
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: all(m in d.find_element(By.ID, "main-view").text for m in meals))
        page_content = main_view.text
        
        # Verify all meals appear
        for meal_name in meals:
            assert meal_name in page_content, f"{meal_name} should appear in logs"

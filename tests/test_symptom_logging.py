"""
Test symptom logging functionality
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.mark.ui
class TestSymptomLogging:
    """Test suite for symptom logging functionality"""
    
    def test_open_symptom_modal(self, driver):
        """Test opening the symptom logging modal"""
        wait = WebDriverWait(driver, 10)
        
        # Click quick symptom button
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        # Verify modal is visible
        modal = wait.until(
            EC.visibility_of_element_located((By.ID, "modal-container"))
        )
        assert "hidden" not in modal.get_attribute("class"), \
            "Modal should be visible"
        
        # Verify modal contains symptom form
        assert "Log Symptom" in modal.text, "Modal should contain symptom form"
    
    @pytest.mark.smoke
    def test_log_symptom_basic(self, driver):
        """Test logging a basic symptom"""
        wait = WebDriverWait(driver, 10)
        
        # Open symptom modal
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        # Select symptom type
        symptom_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-type"))
        )
        select = Select(symptom_select)
        select.select_by_value("headache")
        
        # Select severity
        severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="7"]')
        severity_btn.click()
        
        # Submit form
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to symptoms view
        symptoms_view_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_view_btn.click()
        
        # Verify symptom appears in view
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "headache" in d.find_element(By.ID, "main-view").text.lower())
        assert "headache" in main_view.text.lower(), "Logged symptom should appear in symptoms view"
    
    def test_all_symptom_types(self, driver):
        """Test logging different symptom types"""
        wait = WebDriverWait(driver, 10)
        
        symptom_types = [
            "energy", "passing_gas", "acidity", "burping", 
            "pain", "headache", "mood", "constipation"
        ]
        
        for symptom_type in symptom_types:
            # Open modal
            symptom_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
            )
            symptom_btn.click()
            
            # Select symptom
            symptom_select = wait.until(
                EC.presence_of_element_located((By.ID, "symptom-type"))
            )
            select = Select(symptom_select)
            select.select_by_value(symptom_type)
            
            # Select severity
            severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="5"]')
            severity_btn.click()
            
            # Submit
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
            submit_btn.click()
            
            # Wait for modal to close before next loop
            wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to symptoms view
        symptoms_view_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_view_btn.click()
        
        # Wait for symptoms to load
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: any(st in d.find_element(By.ID, "main-view").text.lower() for st in symptom_types))
        page_content = main_view.text.lower()
        
        # Verify at least some symptoms appear
        symptom_count = sum(1 for st in symptom_types if st in page_content)
        assert symptom_count >= len(symptom_types) - 2, \
            "Most logged symptoms should appear in symptoms view"
    
    def test_severity_levels(self, driver):
        """Test different severity levels"""
        wait = WebDriverWait(driver, 10)
        
        severities = [1, 5, 10]
        
        for severity in severities:
            # Open modal
            symptom_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
            )
            symptom_btn.click()
            
            # Select symptom
            symptom_select = wait.until(
                EC.presence_of_element_located((By.ID, "symptom-type"))
            )
            select = Select(symptom_select)
            select.select_by_value("pain")
            
            # Select severity
            severity_btn = driver.find_element(By.CSS_SELECTOR, f'[data-val="{severity}"]')
            severity_btn.click()
            
            # Verify severity button is active
            assert "active" in severity_btn.get_attribute("class"), \
                f"Severity button {severity} should be active"
            
            # Submit
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
            submit_btn.click()
            
            # Wait for modal to close
            wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to symptoms view
        symptoms_view_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_view_btn.click()
        
        # Wait for badges to appear
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, ".severity-badge")))
        
        # Verify severity badges appear
        severity_badges = driver.find_elements(By.CSS_SELECTOR, ".severity-badge")
        assert len(severity_badges) >= 3, "Should have severity badges for logged symptoms"
    
    def test_chest_pain_symptoms(self, driver):
        """Test chest pain specific symptoms"""
        wait = WebDriverWait(driver, 10)
        
        chest_pain_types = ["chest_pain_left", "chest_pain_right", "chest_pain_middle"]
        
        for pain_type in chest_pain_types:
            # Open modal
            symptom_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
            )
            symptom_btn.click()
            
            # Select symptom
            symptom_select = wait.until(
                EC.presence_of_element_located((By.ID, "symptom-type"))
            )
            select = Select(symptom_select)
            select.select_by_value(pain_type)
            
            # Select severity
            severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="8"]')
            severity_btn.click()
            
            # Submit
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
            submit_btn.click()
            
            # Wait for modal to close
            wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to symptoms view
        symptoms_view_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_view_btn.click()
        
        # Wait for content
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "chest_pain" in d.find_element(By.ID, "main-view").text.lower())
        page_content = main_view.text.lower()
        
        # Verify chest pain symptoms appear
        assert "chest_pain" in page_content, "Chest pain symptoms should appear"
    
    def test_rib_pain_symptoms(self, driver):
        """Test rib pain specific symptoms"""
        wait = WebDriverWait(driver, 10)
        
        rib_pain_types = ["rib_pain_left", "rib_pain_right"]
        
        for pain_type in rib_pain_types:
            # Open modal
            symptom_btn = wait.until(
                EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
            )
            symptom_btn.click()
            
            # Select symptom
            symptom_select = wait.until(
                EC.presence_of_element_located((By.ID, "symptom-type"))
            )
            select = Select(symptom_select)
            select.select_by_value(pain_type)
            
            # Select severity
            severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="6"]')
            severity_btn.click()
            
            # Submit
            submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
            submit_btn.click()
            
            # Wait for modal to close
            wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to symptoms view
        symptoms_view_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="symptoms"]'))
        )
        symptoms_view_btn.click()
        
        # Wait for content
        main_view = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "rib_pain" in d.find_element(By.ID, "main-view").text.lower())
        page_content = main_view.text.lower()
        
        # Verify rib pain symptoms appear
        assert "rib_pain" in page_content, "Rib pain symptoms should appear"

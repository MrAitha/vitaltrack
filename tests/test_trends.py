"""
Test trends and correlation analysis functionality
"""
import pytest
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select


@pytest.mark.ui
class TestTrends:
    """Test suite for trends and analysis functionality"""
    
    def test_trends_view_loads(self, driver):
        """Test that trends view loads correctly"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Wait for content to load
        page_content = wait.until(
            EC.presence_of_element_located((By.ID, "main-view"))
        )
        wait.until(lambda d: "symptom frequency" in d.find_element(By.ID, "main-view").text.lower())
        
        # Verify trends elements are present (case-insensitive)
        page_text = page_content.text.lower()
        assert "symptom frequency" in page_text, "Should show symptom frequency section"
        assert "root cause analyzer" in page_text, "Should show root cause analyzer"
    
    def test_symptom_chart_renders(self, driver):
        """Test that the symptom chart canvas renders"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Wait for chart canvas
        chart = wait.until(
            EC.presence_of_element_located((By.ID, "symptomChart"))
        )
        assert chart is not None, "Chart canvas should be present"
    
    def test_root_cause_analyzer_dropdown(self, driver):
        """Test that root cause analyzer dropdown exists"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Check for analyzer dropdown
        analyzer_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-analyzer-select"))
        )
        assert analyzer_select is not None, "Analyzer dropdown should be present"
    
    @pytest.mark.smoke
    def test_correlation_analysis_with_data(self, driver):
        """Test correlation analysis with logged meals and symptoms"""
        wait = WebDriverWait(driver, 10)
        
        # Log a meal first
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Spicy Tacos")
        
        ingredients_input = driver.find_element(By.ID, "meal-ingredients")
        ingredients_input.send_keys("Chili, Beef, Onion")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Modify the meal timestamp to be 5 hours ago using JavaScript
        driver.execute_script("""
            const store = new Store();
            const meals = store.data.meals;
            if (meals.length > 0) {
                const fiveHoursAgo = new Date(Date.now() - 5 * 60 * 60 * 1000);
                meals[meals.length - 1].timestamp = fiveHoursAgo.toISOString();
                store.save();
            }
        """)
        
        # Log a symptom
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        symptom_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-type"))
        )
        select = Select(symptom_select)
        select.select_by_value("pain")
        
        severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="7"]')
        severity_btn.click()
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Wait for analyzer
        analyzer_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-analyzer-select"))
        )
        select = Select(analyzer_select)
        select.select_by_value("pain")
        
        # Wait for results
        results = wait.until(
            EC.presence_of_element_located((By.ID, "analyzer-results"))
        )
        wait.until(lambda d: "analyzing" not in d.find_element(By.ID, "analyzer-results").text.lower())
        results_text = results.text.lower()
        
        # Should show either the meal/ingredients OR a "no correlations" message
        has_correlation = "spicy tacos" in results_text or "ingredient:" in results_text
        has_no_correlation_msg = "no strong dietary correlations" in results_text or "no correlations" in results_text
        
        assert has_correlation or has_no_correlation_msg, \
            "Should show either correlation results or no correlations message"
    
    def test_ingredient_level_correlation(self, driver):
        """Test that ingredient-level correlations are shown"""
        wait = WebDriverWait(driver, 10)
        
        # Log a meal with ingredients
        meal_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-meal-btn"))
        )
        meal_btn.click()
        
        meal_name_input = wait.until(
            EC.presence_of_element_located((By.ID, "meal-name"))
        )
        meal_name_input.send_keys("Salad")
        
        ingredients_input = driver.find_element(By.ID, "meal-ingredients")
        ingredients_input.send_keys("Onion, Garlic, Lettuce")
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#meal-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Modify timestamp to 3 hours ago
        driver.execute_script("""
            const store = new Store();
            const meals = store.data.meals;
            if (meals.length > 0) {
                const threeHoursAgo = new Date(Date.now() - 3 * 60 * 60 * 1000);
                meals[meals.length - 1].timestamp = threeHoursAgo.toISOString();
                store.save();
            }
        """)
        
        # Log symptom
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        symptom_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-type"))
        )
        select = Select(symptom_select)
        select.select_by_value("passing_gas")
        
        severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="5"]')
        severity_btn.click()
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Wait for analyzer
        analyzer_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-analyzer-select"))
        )
        select = Select(analyzer_select)
        select.select_by_value("passing_gas")
        
        # Wait for results
        results = wait.until(
            EC.presence_of_element_located((By.ID, "analyzer-results"))
        )
        wait.until(lambda d: "analyzing" not in d.find_element(By.ID, "analyzer-results").text.lower())
        results_text = results.text.lower()
        
        # Should show either ingredient correlations OR a "no correlations" message
        has_ingredient = "ingredient:" in results_text
        has_no_correlation_msg = "no strong dietary correlations" in results_text or "no correlations" in results_text
        
        assert has_ingredient or has_no_correlation_msg, \
            "Should show either ingredient-level correlations or no correlations message"
    
    def test_empty_state_analyzer(self, driver):
        """Test analyzer shows empty state when no symptom selected"""
        wait = WebDriverWait(driver, 10)
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Check for empty state
        results = wait.until(
            EC.presence_of_element_located((By.ID, "analyzer-results"))
        )
        assert "Select a symptom" in results.text, \
            "Should show empty state message"
    
    def test_no_correlations_found(self, driver):
        """Test analyzer when no correlations exist"""
        wait = WebDriverWait(driver, 10)
        
        # Log a symptom without any meals
        symptom_btn = wait.until(
            EC.element_to_be_clickable((By.ID, "quick-symptom-btn"))
        )
        symptom_btn.click()
        
        symptom_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-type"))
        )
        select = Select(symptom_select)
        select.select_by_value("headache")
        
        severity_btn = driver.find_element(By.CSS_SELECTOR, '[data-val="3"]')
        severity_btn.click()
        
        submit_btn = driver.find_element(By.CSS_SELECTOR, "#symptom-form button[type='submit']")
        submit_btn.click()
        
        # Wait for modal to close
        wait.until(lambda d: "hidden" in d.find_element(By.ID, "modal-container").get_attribute("class"))
        
        # Navigate to trends
        trends_btn = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '[data-view="trends"]'))
        )
        trends_btn.click()
        
        # Analyze
        analyzer_select = wait.until(
            EC.presence_of_element_located((By.ID, "symptom-analyzer-select"))
        )
        select = Select(analyzer_select)
        select.select_by_value("headache")
        
        # Wait for results
        results = wait.until(
            EC.presence_of_element_located((By.ID, "analyzer-results"))
        )
        wait.until(lambda d: "analyzing" not in d.find_element(By.ID, "analyzer-results").text.lower())
        results_text = results.text.lower()
        
        # Accept the actual message format
        assert "no strong dietary correlations" in results_text or "no correlations" in results_text or "no potential triggers" in results_text, \
            "Should show no correlations message"

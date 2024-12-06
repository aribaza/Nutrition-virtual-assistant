import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Set up the WebDriver
def setup_driver():
    driver = webdriver.Chrome()  # Add the path to your ChromeDriver if necessary
    driver.maximize_window()
    return driver

def scrape_nutritional_info(item):
    driver = setup_driver()
    
    try:
        driver.get("https://www.tesco.com")
        
        # Wait for the search bar to become available
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "search-input-1"))
        )
        
        # Locate the search bar and input the search query
        search_bar = driver.find_element(By.ID, "search-input-1")  # Using the `id` attribute
        search_bar.clear()  # Clear any pre-filled text
        search_bar.send_keys(item)
        search_bar.send_keys(Keys.RETURN)  # Simulate pressing Enter
        
        time.sleep(2) 
        driver.refresh()
        driver.execute_script("window.scrollBy(0, 500);")
        
        # Wait for the search results to load and click the first search result
        # Get the link URL using JavaScript
        link_url = driver.execute_script(
            "return document.querySelector('h3:first-of-type > a').href;"
        )
        
        driver.get(link_url)

        time.sleep(2) 
        driver.refresh()
        driver.execute_script("window.scrollBy(0, 500);")

        # Extract nutritional information (type and percentage)
        WebDriverWait(driver, 1000).until(
            EC.presence_of_element_located(
                (By.CSS_SELECTOR, "div.styled__Item-sc-1qnv8z6-1.OGJz")
            )
        )
        nutritional_items = driver.find_elements(By.CSS_SELECTOR, "div.styled__Item-sc-1qnv8z6-1.OGJz")
        
        for item in nutritional_items:
            # Get the type (e.g., "Salt")
            type_of_nutrient = item.find_element(By.CSS_SELECTOR, "dt.styled__ItemTitle-sc-1qnv8z6-5.hceUwO").text
            
            # Get the percentage of the reference intake (e.g., "<1% of the reference intake")
            percentage = item.find_element(By.CSS_SELECTOR, "dd.styled__ItemValue-sc-1qnv8z6-6.jWYAjg").text
            
            print(f"{type_of_nutrient}: {percentage}")
    
    except Exception as e:
        print("An error occurred:", e)
    finally:
        driver.quit()

# Example usage
scrape_nutritional_info("Domio Bolognese")

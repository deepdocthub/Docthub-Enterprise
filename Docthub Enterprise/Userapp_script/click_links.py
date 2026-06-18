import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def main():
    # Setup Chrome WebDriver with desktop options
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://courses.docthub.com"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(5) # Initial load wait
        
        # 1. Sidebar/Tab Interaction
        tabs = ["All Courses", "Online Courses", "Fellowships"]
        selected_tab = random.choice(tabs)
        print(f"Selected tab to click: {selected_tab}")
        
        try:
            # Try to find the tab by text and click it
            tab_element = driver.find_element(By.PARTIAL_LINK_TEXT, selected_tab)
            tab_element.click()
            print(f"Clicked '{selected_tab}'")
        except Exception as e:
            print(f"Could not click tab '{selected_tab}': {e}")
            # Fallback to All Courses if specific one fails
            driver.get("https://courses.docthub.com/all-courses")
            
        print("Waiting 2000ms after tab click...")
        time.sleep(2)
        
        # 2. Filter Selection (Select 10 filters)
        print("Looking for filters...")
        try:
            # Find all checkboxes
            checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
            print(f"Found {len(checkboxes)} checkboxes.")
            
            if len(checkboxes) > 0:
                # Select up to 10 distinct checkboxes
                num_to_select = min(10, len(checkboxes))
                filters_to_click = random.sample(checkboxes, num_to_select)
                
                for i, checkbox in enumerate(filters_to_click):
                    try:
                        # Scroll into view
                        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", checkbox)
                        time.sleep(0.5) # Small pause after scroll
                        
                        # Click via JS to avoid interception
                        driver.execute_script("arguments[0].click();", checkbox)
                        print(f"[{i+1}/{num_to_select}] Selected a filter.")
                        
                        print("Waiting 2000ms after filter selection...")
                        time.sleep(2)
                    except Exception as e:
                        print(f"Failed to click filter {i+1}: {e}")
            else:
                print("No filters found to select.")
                
        except Exception as e:
            print(f"Error during filter selection: {e}")

        # 3. Link Clicking
        print("Starting link clicking phase...")
        
        # Re-find links to ensure we have the latest DOM state
        links = driver.find_elements(By.TAG_NAME, "a")
        hrefs = []
        for link in links:
            href = link.get_attribute("href")
            if href and href.startswith("http"):
                hrefs.append(href)
        
        print(f"Found {len(hrefs)} valid links.")
        
        for i, href in enumerate(hrefs):
            try:
                print(f"[{i+1}/{len(hrefs)}] Navigating to: {href}")
                
                # Navigate in the same tab
                driver.get(href)
                
                print("Waiting 6000ms...")
                time.sleep(6)
                
                # Optional: Go back to maintain "browsing" feel, though we are iterating a list
                # driver.back() 
                # time.sleep(2)
                
            except Exception as e:
                print(f"Failed to visit {href}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    main()

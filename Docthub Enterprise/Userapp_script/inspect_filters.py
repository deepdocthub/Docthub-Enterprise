from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument("window-size=1920,1080")
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://courses.docthub.com/all-courses"
        print(f"Navigating to {url}...")
        driver.get(url)
        time.sleep(5)
        
        # Print body text to see what's loaded
        body_text = driver.find_element(By.TAG_NAME, "body").text
        print(f"Body text start: {body_text[:500]}")

        # Try to find the sidebar or filter section
        try:
            # Look for elements containing "Stream"
            stream_elements = driver.find_elements(By.XPATH, "//*[contains(text(), 'Stream')]")
            print(f"Found {len(stream_elements)} elements with text 'Stream'")
            for el in stream_elements:
                print(f"Tag: {el.tag_name}, Class: {el.get_attribute('class')}, Text: {el.text}")
                # Get parent
                try:
                    parent = el.find_element(By.XPATH, "..")
                    print(f"  Parent Tag: {parent.tag_name}, Class: {parent.get_attribute('class')}")
                except:
                    pass
        except Exception as e:
            print(f"Error finding Stream elements: {e}")

        # Look for checkboxes
        checkboxes = driver.find_elements(By.CSS_SELECTOR, "input[type='checkbox']")
        print(f"Found {len(checkboxes)} checkboxes")
        for i, cb in enumerate(checkboxes[:5]): # Print first 5
            print(f"Checkbox {i}: ID={cb.get_attribute('id')}, Name={cb.get_attribute('name')}")
            # Try to find label
            try:
                parent = cb.find_element(By.XPATH, "..")
                print(f"  Parent text: {parent.text}")
            except:
                pass

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

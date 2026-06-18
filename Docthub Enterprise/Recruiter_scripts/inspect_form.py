import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LOGIN_URL = "https://enterprise.ibns.in/"
EMAIL = "new.enterprise@yopmail.com"
PASSWORD = "Test@123"

# --- SELECTORS ---
# If the script fails to find elements, update these selectors based on the website's HTML.
# You can find these by right-clicking the element in Chrome > Inspect.
SELECTORS = {
    # Try these common ID/Name/Class patterns for Email
    "email": [
        (By.ID, "email"),
        (By.NAME, "email"),
        (By.ID, "username"),
        (By.NAME, "username"),
        (By.CSS_SELECTOR, "input[type='email']"),
        (By.CSS_SELECTOR, "input[type='text']"),
    ],
    # Try these for Password
    "password": [
        (By.ID, "password"),
        (By.NAME, "password"),
        (By.CSS_SELECTOR, "input[type='password']"),
    ],
    # Try these for the Login Button
    "submit_button": [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.ID, "login-button"),
        (By.ID, "submit"),
        (By.XPATH, "//button[contains(text(), 'Login')]"),
        (By.XPATH, "//button[contains(text(), 'Sign In')]"),
    ],
    # Try these for the Recruiter Link/Button (SVG Arrow)
    "recruiter_card": [
        (By.CSS_SELECTOR, "body > div.min-h-screen.bg-gray-100 > div > div > main > div > div.grid.sm\:mt-0\.5.gap-4.sm\:grid-cols-2.lg\:grid-cols-3 > button:nth-child(1) > span > svg"),
        (By.CSS_SELECTOR, "svg.lucide-arrow-right"),
        (By.XPATH, "//*[name()='svg'][contains(@class, 'lucide-arrow-right')]"),
        (By.XPATH, "//*[name()='svg'][contains(@class, 'lucide-arrow-right')]/.."), # Parent of the SVG
        (By.XPATH, "//a[normalize-space()='Recruiter']"),
    ],
    # Try these for the Post a Job Button
    "post_job_button": [
        (By.XPATH, "//button[contains(text(), 'Post a Job')]"),
        (By.XPATH, "//a[contains(text(), 'Post a Job')]"),
        (By.XPATH, "//span[contains(text(), 'Post a Job')]"),
        (By.CSS_SELECTOR, "button.post-job"),
    ]
}

def find_element_robust(driver, selector_list, element_name):
    """
    Tries multiple selectors to find an element.
    """
    print(f"Looking for {element_name}...")
    for by, value in selector_list:
        try:
            element = WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((by, value))
            )
            print(f"  Found {element_name} using {by}='{value}'")
            return element
        except:
            continue
    raise Exception(f"Could not find {element_name} using any of the provided selectors.")

def main():
    print("Starting Login Script...")
    
    # Setup Chrome Driver
    # ChromeDriverManager().install() downloads the correct driver for your Chrome version
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)
    
    try:
        # 1. Navigate to the website
        print(f"Navigating to {LOGIN_URL}...")
        driver.get(LOGIN_URL)
        driver.maximize_window()
        
        # Allow page to load
        time.sleep(3)
        
        # Check if we need to click a "Login" link on the landing page
        # (Sometimes the main URL is a landing page, not the login form directly)
        current_url = driver.current_url
        if "login" not in current_url.lower():
            print("Not on login page yet. Checking for 'Login' link...")
            try:
                login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'login')]")
                login_link.click()
                print("Clicked Login link.")
                time.sleep(3)
            except:
                print("Could not find a 'Login' link. Assuming we are on the right page or it's a single-page app.")

        # 2. Enter Email
        email_input = find_element_robust(driver, SELECTORS["email"], "Email Input")
        email_input.clear()
        email_input.send_keys(EMAIL)
        print("Entered email.")
        
        # 3. Enter Password
        password_input = find_element_robust(driver, SELECTORS["password"], "Password Input")
        password_input.clear()
        password_input.send_keys(PASSWORD)
        print("Entered password.")
        
        # 4. Click Login
        submit_btn = find_element_robust(driver, SELECTORS["submit_button"], "Submit Button")
        # Sometimes buttons are obscured by overlays, so we use JavaScript click as a fallback
        try:
            submit_btn.click()
        except:
            print("Standard click failed, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", submit_btn)
            
        print("Clicked Login button.")
        
        # 5. Wait for Login to complete
        print("Waiting for login to complete...")
        time.sleep(5)
        
        # 6. Click Recruiter Card
        recruiter_card = find_element_robust(driver, SELECTORS["recruiter_card"], "Recruiter Card")
        try:
            recruiter_card.click()
        except:
            print("Standard click failed, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", recruiter_card)
        print("Clicked Recruiter Card.")
        
        # Wait for next view
        time.sleep(3)
        
        # 7. Click Post a Job Button
        post_job_btn = find_element_robust(driver, SELECTORS["post_job_button"], "Post a Job Button")
        try:
            post_job_btn.click()
        except:
            print("Standard click failed, trying JavaScript click...")
            driver.execute_script("arguments[0].click();", post_job_btn)
        print("Clicked Post a Job button.")
        
        # 8. Save page source and screenshot
        print("Saving page source and screenshot...")
        time.sleep(5) # Wait a bit for dynamic content
        with open("job_form.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
        driver.save_screenshot("job_form.png")
        print("Saved job_form.html and job_form.png")
        
        print("Done!")

    except Exception as e:
        print(f"\nERROR: {e}")
        print("\nTroubleshooting Tip: If an element wasn't found, inspect the webpage manually")
        print("and update the SELECTORS dictionary in this script with the correct ID or Class.")

    finally:
        # Close browser
        driver.quit()

if __name__ == "__main__":
    main()

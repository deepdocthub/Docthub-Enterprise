from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

def main():
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    driver = webdriver.Chrome(service=service, options=options)
    
    try:
        url = "https://courses.docthub.com/all-courses"
        driver.get(url)
        time.sleep(5) # Wait for dynamic content
        
        with open("page_source.html", "w", encoding="utf-8") as f:
            f.write(driver.page_source)
            
        print("Page source saved to page_source.html")
        
    finally:
        driver.quit()

if __name__ == "__main__":
    main()

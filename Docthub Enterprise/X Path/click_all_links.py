import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from urllib.parse import urljoin, urlparse
from collections import deque

def extract_links_from_page(driver, current_url, base_domain):
    """Extracts all internal links from the current page."""
    elements = driver.find_elements(By.TAG_NAME, "a")
    new_links = set()
    for element in elements:
        href = element.get_attribute("href")
        if href:
            full_url = urljoin(current_url, href)
            if urlparse(full_url).netloc == base_domain:
                clean_url = full_url.split('#')[0]
                new_links.add(clean_url)
    return new_links

def crawl_all_links(base_url):
    """Crawls all internal links starting from the base URL."""
    print("Initializing WebDriver...")
    service = Service(ChromeDriverManager().install())
    options = webdriver.ChromeOptions()
    
    # options.add_argument('--headless') 
    
    driver = webdriver.Chrome(service=service, options=options)
    base_domain = urlparse(base_url).netloc
    
    visited = set()
    to_visit = deque([base_url])
    
    try:
        driver.maximize_window()
        
        while to_visit:
            current_url = to_visit.popleft()
            
            if current_url in visited:
                continue
                
            print(f"[{len(visited) + 1}] Visiting: {current_url}")
            driver.get(current_url)
            time.sleep(2)  # Adjust sleep time based on site responsiveness
            visited.add(current_url)
            
            # Extract links from the newly loaded page
            found_links = extract_links_from_page(driver, current_url, base_domain)
            
            for link in found_links:
                if link not in visited and link not in to_visit:
                    to_visit.append(link)
                    
            print(f"   -> Found {len(found_links)} links on this page. Queue size: {len(to_visit)}")
            
    except Exception as e:
        print(f"An error occurred: {e}")
        
    finally:
        print(f"Finished crawling. Visited {len(visited)} unique internal pages.")
        driver.quit()

if __name__ == "__main__":
    target_url = "https://www.docthub.com/"
    crawl_all_links(target_url)

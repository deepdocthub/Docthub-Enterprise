import json
import time
from playwright.sync_api import sync_playwright

def main():
    # Load JSON file
    with open("link-xpath-report.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Extract unique XPaths
    xpaths = []
    for item in data:
        xpath = item.get("xpath")
        if xpath and xpath not in xpaths:
            xpaths.append(xpath)

    print(f"Found {len(xpaths)} unique XPaths to click.")

    with sync_playwright() as p:
        # Launch browser
        browser = p.chromium.launch(headless=False, slow_mo=500)
        context = browser.new_context()
        page = context.new_page()

        for i, xpath in enumerate(xpaths, 1):
            print(f"[{i}/{len(xpaths)}] Attempting to click: {xpath}")
            try:
                # Always start from the base URL before each click
                page.goto("https://www.docthub.com/", wait_until="networkidle")
                
                # Locate and wait for element
                locator = page.locator(f"xpath={xpath}").first
                locator.wait_for(state="attached", timeout=5000)
                locator.scroll_into_view_if_needed()
                
                # Visually show a pointer where it's about to click
                locator.evaluate("""(el) => {
                    const rect = el.getBoundingClientRect();
                    const x = rect.left + window.scrollX + rect.width / 2;
                    const y = rect.top + window.scrollY + rect.height / 2;
                    const pointer = document.createElement('div');
                    pointer.style.position = 'absolute';
                    pointer.style.left = x + 'px';
                    pointer.style.top = y + 'px';
                    pointer.style.width = '40px';
                    pointer.style.height = '40px';
                    pointer.style.backgroundColor = 'rgba(255, 0, 0, 0.5)';
                    pointer.style.border = '4px solid red';
                    pointer.style.borderRadius = '50%';
                    pointer.style.zIndex = '999999';
                    pointer.style.pointerEvents = 'none';
                    pointer.style.transform = 'translate(-50%, -50%)';
                    pointer.style.transition = 'transform 0.3s ease';
                    document.body.appendChild(pointer);
                    
                    // Animate click effect
                    setTimeout(() => { pointer.style.transform = 'translate(-50%, -50%) scale(0.3)'; }, 100);
                    setTimeout(() => { pointer.remove(); }, 1500);
                }""")
                time.sleep(0.5)
                
                # Keep track of tabs to check if click opens a new one
                pages_before = len(context.pages)
                
                # Click it
                locator.click(timeout=5000)
                print(f" -> Click successful.")
                time.sleep(2) # Give it some time to process navigation or new tab
                
                # Get the active page (new tab if created, or current page)
                active_page = context.pages[-1]
                active_page.bring_to_front()
                
                # Smoothly scroll down
                for _ in range(5):
                    active_page.mouse.wheel(0, 400)
                    time.sleep(0.3)
                    
                time.sleep(1) # Let user see the scrolled position
                
                # If a new tab was opened, close it to keep environment clean
                if len(context.pages) > pages_before:
                    active_page.close()
                
            except Exception as e:
                print(f" -> Failed to click. Error: {e}")

        print("Finished clicking all XPaths.")
        browser.close()

if __name__ == "__main__":
    main()

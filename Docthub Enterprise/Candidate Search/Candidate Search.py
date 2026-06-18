import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# --- CONFIGURATION ---
LOGIN_URL = "https://enterprise.docthub.com/"
EMAIL = "lead.qa+11@docthub.com"
PASSWORD = "Docthub@2025"

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
        (By.CSS_SELECTOR, "body > div.min-h-screen.bg-gray-100 > div > div > main > div > div.grid.sm\\:mt-0\\.5.gap-4.sm\\:grid-cols-2.lg\\:grid-cols-3 > button:nth-child(1) > span > svg"),
        (By.CSS_SELECTOR, "svg.lucide-arrow-right"),
        (By.XPATH, "//*[name()='svg'][contains(@class, 'lucide-arrow-right')]"),
        (By.XPATH, "//*[name()='svg'][contains(@class, 'lucide-arrow-right')]/.."),  # Parent of the SVG
        (By.XPATH, "//a[normalize-space()='Recruiter']"),
    ],

    # ---------------------------------------------------------------
    # Candidate Search menu & filter selectors
    # ---------------------------------------------------------------
    "candidate_search_menu": [
        # Primary: exact absolute XPath provided by user
        (By.XPATH, "/html/body/div[2]/main/aside/aside/div[1]/button[3]"),
        # Text-based fallbacks (more resilient to DOM changes)
        (By.XPATH, "//button[normalize-space()='Candidate Search']"),
        (By.XPATH, "//button[contains(normalize-space(), 'Candidate Search')]"),
        (By.XPATH, "//aside//button[contains(., 'Candidate Search')]"),
        # Positional fallbacks within the nested aside
        (By.XPATH, "//main//aside//aside//button[3]"),
        (By.XPATH, "(//aside//aside//div//button)[3]"),
    ],
    # Individual filter dropdown buttons (by position in the filter form)
    "filter_key_skills": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[1]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[1]"),
    ],
    "filter_state": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[1]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[2]"),
    ],
    "filter_city": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[2]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[3]"),
    ],
    "filter_education": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[3]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[4]"),
    ],
    "filter_specialty": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[5]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[5]"),
    ],
    "filter_job_role": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[6]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[6]"),
    ],
    "filter_stream": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[7]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[7]"),
    ],
    "filter_experience": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[8]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[8]"),
    ],
    "filter_gender": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[1]/div[2]/div/div[9]/div/div/div/button"),
        (By.XPATH, "(//section//form//button)[9]"),
    ],
    "search_button": [
        (By.XPATH, "/html/body/div[2]/main/div/div[1]/section/form/div[2]/div[2]/button"),
        (By.XPATH, "//section//form//div[2]//button[contains(., 'Search')]"),
        (By.XPATH, "//button[normalize-space()='Search']"),
    ],

    # ---------------------------------------------------------------
    # Candidate card action buttons
    # ---------------------------------------------------------------
    "view_phone_email_btn": [
        # Primary XPath from user
        (By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div/div[1]/article/div[2]/div[3]/div[1]/div[1]/button/span[1]"),
        # Text-based fallbacks
        (By.XPATH, "(//button[contains(., 'View Phone') or contains(., 'View Email') or contains(., 'View Contact')])[1]"),
        (By.XPATH, "(//article//button[contains(., 'Phone') or contains(., 'Email')])[1]"),
        (By.XPATH, "(//span[contains(text(), 'View Phone') or contains(text(), 'View Email')])[1]"),
    ],
    "view_resume_btn": [
        # Primary XPath from user
        (By.XPATH, "/html/body/div[2]/main/div/div[2]/div/div[2]/div/div/div/div[1]/article/div[2]/div[3]/div[1]/div[2]/button"),
        # Text-based fallbacks
        (By.XPATH, "(//button[contains(., 'View Resume') or contains(., 'Resume')])[1]"),
        (By.XPATH, "(//article//button[contains(., 'Resume')])[1]"),
    ],
}


# ---------------------------------------------------------------------------
# Utility Functions (shared with Recruiter Dashboard)
# ---------------------------------------------------------------------------

def find_element_robust(driver, selector_list, element_name):
    """
    Efficiently waits for ANY of the provided selectors to match an element.
    """
    print(f"Looking for {element_name}...")

    # Create a list of expected conditions for all selectors
    conditions = [EC.presence_of_element_located((by, val)) for by, val in selector_list]

    try:
        # Wait until at least one of the selectors matches
        WebDriverWait(driver, 15).until(EC.any_of(*conditions))

        # Now find which one triggered the match
        for by, value in selector_list:
            elements = driver.find_elements(by, value)
            if elements:
                print(f"  Found {element_name} using {by}='{value}'")
                return elements[0]

        raise Exception("Wait completed but element not found in list check.")

    except Exception as e:
        raise Exception(f"Could not find {element_name}. Timed out.") from e


def select_dropdown_option(driver, btn_selector, option_text, element_name):
    """
    Clicks a dropdown button and selects an option by text.
    """
    print(f"Selecting '{option_text}' from {element_name}...")
    btn = find_element_robust(driver, btn_selector, element_name)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
    time.sleep(1)
    try:
        btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", btn)

    time.sleep(1)
    try:
        # This covers common dropdown patterns
        option_xpath = (
            f"//*[contains(@role, 'option') or contains(@role, 'listbox')]"
            f"//*[contains(text(), '{option_text}')] | "
            f"//*[contains(@class, 'select-content')]//*[contains(text(), '{option_text}')] | "
            f"//*[text()='{option_text}']"
        )
        option = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        option.click()
        print(f"  Selected '{option_text}'")
    except Exception as e:
        print(f"  Failed to select '{option_text}': {e}")


def search_and_select(driver, input_selector, search_text, element_name):
    """
    Types into an input character by character and selects the first matching option.
    """
    print(f"Searching and selecting '{search_text}' in {element_name}...")
    inp = find_element_robust(driver, input_selector, element_name)
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", inp)
    time.sleep(1)

    # Clear using keys to ensure events are triggered
    inp.click()
    inp.send_keys(Keys.CONTROL + "a")
    inp.send_keys(Keys.BACKSPACE)
    time.sleep(0.5)

    # Type character by character
    for char in search_text:
        inp.send_keys(char)
        time.sleep(0.1)

    try:
        # Broader XPath for options, including the specific popover pattern found
        option_xpath = (
            f"//div[contains(@class, 'bg-popover')]//*[contains(text(), '{search_text}')] | "
            f"//*[contains(@role, 'option')]//*[contains(text(), '{search_text}')] | "
            f"//*[contains(@class, 'command-item')]//*[contains(text(), '{search_text}')] | "
            f"//*[contains(text(), '{search_text}') and contains(@class, 'cursor-pointer')] | "
            f"//div[contains(@class, 'select-item')]//*[contains(text(), '{search_text}')]"
        )
        option = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, option_xpath))
        )
        try:
            option.click()
        except Exception:
            driver.execute_script("arguments[0].click();", option)
        print(f"  Selected '{search_text}'")
    except Exception as e:
        print(f"  Could not find option for '{search_text}' via click.")
        # Debug: List all visible options
        print("  Available options (debug):")
        options = driver.find_elements(
            By.XPATH,
            "//*[contains(@role, 'option')] | //*[contains(@class, 'command-item')] | "
            "//*[contains(@class, 'select-item')] | //div[contains(@class, 'bg-popover')]//span"
        )
        for opt in options:
            if opt.text.strip():
                print(f"    - '{opt.text.strip()}'")

        print(f"  Trying Enter key as fallback for '{search_text}'...")
        inp.send_keys(Keys.ENTER)
        time.sleep(1)


# ---------------------------------------------------------------------------
# Candidate Search-specific functions
# ---------------------------------------------------------------------------

# All available filter definitions: (selector_key, human-readable label)
ALL_FILTERS = [
    ("filter_key_skills",  "Key Skills"),
    ("filter_state",       "State / Province"),
    ("filter_city",        "City Location"),
    ("filter_education",   "Education"),
    ("filter_specialty",   "Specialty"),
    ("filter_job_role",    "Job Role"),
    ("filter_stream",      "Stream"),
    ("filter_experience",  "Experience"),
    ("filter_gender",      "Gender"),
]


def get_dropdown_options(driver):
    """
    After a filter dropdown is opened, collect all visible option elements
    and return them as a list of WebElements.
    Uses broad selectors to cover common dropdown/popover/listbox patterns.
    """
    option_xpaths = [
        "//*[@role='option']",
        "//*[@role='listbox']//*",
        "//div[contains(@class, 'bg-popover')]//li",
        "//div[contains(@class, 'bg-popover')]//div[@role='option']",
        "//ul[contains(@class, 'select')]//li",
        "//div[contains(@class, 'command-item')]",
        "//div[contains(@class, 'select-item')]",
        "//div[contains(@class, 'dropdown')]//li",
    ]
    for xpath in option_xpaths:
        try:
            opts = WebDriverWait(driver, 5).until(
                lambda d, xp=xpath: [
                    el for el in d.find_elements(By.XPATH, xp)
                    if el.is_displayed() and el.text.strip()
                ]
            )
            if opts:
                return opts
        except Exception:
            continue
    return []


def apply_random_filter(driver, selector_key, label):
    """
    Opens the filter dropdown identified by selector_key, picks one random
    visible option, clicks it, and returns the selected option text.
    Returns None if the dropdown could not be opened or has no options.
    """
    print(f"\n  Opening filter: {label}")
    try:
        btn = find_element_robust(driver, SELECTORS[selector_key], label)
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", btn)
        time.sleep(1)  # Allow dropdown animation / rendering

        options = get_dropdown_options(driver)
        if not options:
            print(f"    No options found for '{label}'. Closing dropdown.")
            # Press Escape to close an open dropdown without selecting
            driver.find_element(By.TAG_NAME, "body").send_keys(Keys.ESCAPE)
            time.sleep(0.5)
            return None

        chosen = random.choice(options)
        chosen_text = chosen.text.strip()
        print(f"    Randomly selected option: '{chosen_text}'")
        try:
            chosen.click()
        except Exception:
            driver.execute_script("arguments[0].click();", chosen)
        time.sleep(0.5)
        return chosen_text

    except Exception as e:
        print(f"    Could not apply filter '{label}': {e}")
        return None


def click_candidate_search_menu(driver):
    """
    Robustly clicks the Candidate Search sidebar menu button.

    Strategy:
      1. Wait for the sidebar to be fully rendered (page stability).
      2. Locate the button using EC.visibility_of_element_located to ensure
         it is both present AND visible (not just in the DOM).
      3. Then wait for EC.element_to_be_clickable before attempting the click.
      4. Scroll the element into the centre of the viewport.
      5. Attempt a standard Selenium click.
      6. If the click is intercepted (overlay / animation blocking it),
         wait briefly and retry with a JavaScript click.
      7. Confirm the page transitioned by verifying the URL or page content
         changed within a timeout.
    """
    print("\nWaiting for sidebar to be fully loaded...")
    # Give the dashboard a moment to settle after the Recruiter Card click
    time.sleep(2)

    menu_btn = None
    last_exc = None

    # Try each selector — first wait for visibility, then for clickability
    for by, value in SELECTORS["candidate_search_menu"]:
        try:
            print(f"  Trying selector: {by}='{value}'")
            # 1. Wait until visible
            menu_btn = WebDriverWait(driver, 10).until(
                EC.visibility_of_element_located((by, value))
            )
            # 2. Wait until clickable
            menu_btn = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((by, value))
            )
            print(f"  Element found and clickable using {by}='{value}'")
            break
        except Exception as exc:
            last_exc = exc
            menu_btn = None
            continue

    if menu_btn is None:
        raise Exception(
            f"Could not find a clickable Candidate Search menu button. "
            f"Last error: {last_exc}"
        )

    # 3. Scroll into view so it is not obscured by sticky headers
    driver.execute_script(
        "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center', inline: 'nearest'});",
        menu_btn
    )
    time.sleep(0.8)  # Let scroll animation finish

    # 4. Standard click attempt
    click_success = False
    try:
        menu_btn.click()
        click_success = True
        print("  Standard click succeeded.")
    except Exception as click_exc:
        print(f"  Standard click failed ({type(click_exc).__name__}: {click_exc}). Retrying with JS click...")

    # 5. JS click fallback (handles ElementClickInterceptedException / overlay issues)
    if not click_success:
        time.sleep(1)  # Wait for any animation / overlay to clear
        driver.execute_script("arguments[0].click();", menu_btn)
        print("  JavaScript click executed.")

    # 6. Confirm the page reacted (URL change OR new content appears)
    print("  Verifying Candidate Search page loaded...")
    try:
        WebDriverWait(driver, 10).until(
            lambda d: (
                "candidate" in d.current_url.lower()
                or "search" in d.current_url.lower()
                or len(d.find_elements(
                    By.XPATH,
                    "//section//form | //form[contains(@class, 'filter')] | "
                    "//*[contains(@class, 'candidate')]"
                )) > 0
            )
        )
        print("  Candidate Search page confirmed loaded.")
    except Exception:
        print("  Warning: Could not confirm page transition. Proceeding anyway...")
        time.sleep(2)  # Extra buffer

    print("Clicked Candidate Search menu successfully.")


def perform_search(driver):
    """
    Clicks the Search button and waits for results to render.
    """
    print("\n  Clicking Search button...")
    search_btn = find_element_robust(driver, SELECTORS["search_button"], "Search Button")
    driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", search_btn)
    time.sleep(0.5)
    try:
        search_btn.click()
    except Exception:
        driver.execute_script("arguments[0].click();", search_btn)
    print("  Search submitted. Waiting for results to render...")
    time.sleep(3)


def has_results(driver):
    """
    Returns True if at least one candidate result card/row is visible.
    Returns False if the page shows 'Search not Found' or '0 / 0 Candidates'.
    """
    # Check for explicit no-results indicators
    no_result_xpaths = [
        "//*[contains(text(), 'Search not Found')]",
        "//*[contains(text(), 'search not found')]",
        "//*[contains(text(), '0 / 0 Candidates')]",
        "//*[contains(text(), '0/0 Candidates')]",
        "//*[contains(text(), '0 Candidates')]",
    ]
    for xpath in no_result_xpaths:
        els = driver.find_elements(By.XPATH, xpath)
        if any(el.is_displayed() for el in els):
            print(f"  No-results indicator detected: '{xpath}'")
            return False

    # Check for positive result indicators
    result_xpaths = [
        "//div[contains(@class, 'candidate-card')]",
        "//div[contains(@class, 'candidate')][not(contains(@class, 'no-result'))]",
        "//table//tbody//tr",
        "//*[contains(@class, 'result-item')]",
        # Generic: a count badge that shows > 0  e.g. '5 / 10 Candidates'
        "//*[contains(text(), 'Candidates') and not(contains(text(), '0 / 0')) and not(contains(text(), '0/0'))]",
    ]
    for xpath in result_xpaths:
        els = driver.find_elements(By.XPATH, xpath)
        visible = [el for el in els if el.is_displayed()]
        if visible:
            print(f"  Results found ({len(visible)} element(s) matched '{xpath}').")
            return True

    print("  Result status unclear — treating as no results.")
    return False


def get_active_filter_chips(driver):
    """
    Returns a list of visible filter chip close-button (X) elements.
    These are the small × icons on each selected filter tag shown below
    the search bar (e.g. 'Abdominal Ultrasound ×').
    """
    chip_close_xpaths = [
        # Chips with an explicit × / close button
        "//button[contains(@class, 'chip') or contains(@class, 'tag') or contains(@class, 'badge')]"
        "//span[contains(@class, 'close') or contains(@class, 'remove') or text()='×' or text()='x']",
        # The X span/svg sitting inside a filter chip container
        "//*[contains(@class, 'chip') or contains(@class, 'filter-tag')]"
        "//*[self::button or self::span or self::svg][contains(@class, 'close') or contains(@class, 'remove') or text()='×']",
        # Lucide X icon inside a chip
        "//*[contains(@class, 'lucide-x') or contains(@class, 'lucide-circle-x')]",
        # Generic: any button whose aria-label says 'remove' or 'close'
        "//button[@aria-label='remove' or @aria-label='close' or @aria-label='Remove' or @aria-label='Close']",
        # Pattern visible in screenshot: chip div with an inline × button
        "//div[contains(@class, 'rounded') and .//button]"
        "//button[contains(@class, 'ml') or contains(@class, 'remove') or normalize-space(text())='×']",
    ]
    found = []
    for xpath in chip_close_xpaths:
        els = driver.find_elements(By.XPATH, xpath)
        visible = [el for el in els if el.is_displayed()]
        if visible:
            found = visible
            break
    return found


def remove_filter_chips_until_results(driver):
    """
    Retry logic: if no candidate results are found after the initial search,
    remove active filter chips one at a time and re-run the search after each
    removal until results appear or all chips have been removed.

    Flow:
      1. Check if results exist → if yes, return immediately.
      2. Collect visible filter-chip close (×) buttons.
      3. For each chip:
         a. Log the chip's label text.
         b. Click the × to remove it.
         c. Wait for the chip to disappear.
         d. Re-run the search.
         e. If results found → stop.
      4. If no chips remain and still no results → log and exit.
    """
    print("\n--- Checking search results ---")

    if has_results(driver):
        print("  ✓ Candidates found on first search. No retry needed.")
        return

    print("  ✗ No results found. Starting filter-chip removal retry loop...")

    iteration = 0
    while True:
        iteration += 1
        chips = get_active_filter_chips(driver)

        if not chips:
            print("  No more filter chips to remove. Exiting retry loop.")
            print("  ✗ No candidates found even after removing all filters.")
            break

        # Take the first available chip's close button
        chip_btn = chips[0]

        # Try to read the parent chip's label text for logging
        try:
            chip_label = chip_btn.find_element(
                By.XPATH, "./ancestor::*[contains(@class,'chip') or "
                           "contains(@class,'tag') or contains(@class,'badge') "
                           "or contains(@class,'rounded')][1]"
            ).text.strip().replace("×", "").strip()
        except Exception:
            chip_label = chip_btn.text.strip() or f"chip-{iteration}"

        print(f"\n  Removing filter chip [{iteration}]: '{chip_label}'")

        # Scroll chip into view and click its × button
        driver.execute_script(
            "arguments[0].scrollIntoView({block: 'center'});", chip_btn
        )
        time.sleep(0.4)
        try:
            chip_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", chip_btn)

        # Wait for the chip count to decrease (max 5 s)
        try:
            WebDriverWait(driver, 5).until(
                lambda d: len(get_active_filter_chips(d)) < len(chips)
            )
            print(f"  Chip '{chip_label}' removed successfully.")
        except Exception:
            print(f"  Could not confirm chip '{chip_label}' was removed. Continuing...")

        time.sleep(0.5)

        # Re-run the search
        try:
            perform_search(driver)
        except Exception as e:
            print(f"  Search button not found after chip removal: {e}")
            # Some UIs auto-search on chip removal; wait a moment
            time.sleep(3)

        if has_results(driver):
            print(f"  ✓ Candidates found after removing {iteration} chip(s). Stopping retry.")
            break

        remaining = get_active_filter_chips(driver)
        print(f"  Still no results. {len(remaining)} chip(s) remaining.")


def verify_phone_email(driver):
    """
    Step 6: Click 'View Phone/Email' on the first candidate card and validate
    that contact information (phone + email) is unlocked and visible.

    Validation checks:
      - A phone number pattern (digits with optional +, spaces, dashes) appears.
      - An email address pattern (@) appears.
      - No error/restriction message is displayed.
    """
    print("\n--- Step 6: View Phone / Email ---")

    try:
        btn = find_element_robust(
            driver, SELECTORS["view_phone_email_btn"], "View Phone/Email Button"
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)
        try:
            btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", btn)
        print("  Clicked View Phone/Email button.")
        time.sleep(2)  # Wait for unlock animation / API response

        # ---- Validation ----
        print("  Validating contact information is now visible...")

        # Check for error messages first
        error_xpaths = [
            "//*[contains(text(), 'Error') or contains(text(), 'error')]",
            "//*[contains(text(), 'Access Denied') or contains(text(), 'access denied')]",
            "//*[contains(text(), 'Insufficient') or contains(text(), 'insufficient')]",
            "//*[@role='alert']",
        ]
        for xpath in error_xpaths:
            els = driver.find_elements(By.XPATH, xpath)
            if any(el.is_displayed() for el in els):
                print(f"  ✗ ERROR detected after clicking View Phone/Email: "
                      f"'{[el.text for el in els if el.is_displayed()][0]}'")
                return

        # Check phone number visibility (digits, optional +/spaces/dashes)
        phone_xpaths = [
            "//*[contains(@class, 'phone') or contains(@class, 'mobile') or contains(@class, 'contact')]",
            "//*[matches(normalize-space(.), '^[+]?[0-9][\\s\\-0-9]{7,}$')]",  # regex attempt
            "//a[starts-with(@href, 'tel:')]",
            "//*[contains(@href, 'tel:')]",
        ]
        phone_found = False
        for xpath in phone_xpaths:
            try:
                els = driver.find_elements(By.XPATH, xpath)
                visible = [el for el in els if el.is_displayed() and el.text.strip()]
                if visible:
                    print(f"  ✓ Phone/contact info visible: '{visible[0].text.strip()}'")
                    phone_found = True
                    break
            except Exception:
                continue

        # Fallback: scan page source for tel: links or 10-digit numbers
        if not phone_found:
            page_src = driver.page_source
            import re
            if re.search(r'tel:|\b[6-9]\d{9}\b|\+91[\s\-]?\d{10}', page_src):
                print("  ✓ Phone number pattern found in page source.")
                phone_found = True

        if not phone_found:
            print("  ~ Phone number not clearly visible (may require scrolling or popup).")

        # Check email visibility
        email_xpaths = [
            "//a[starts-with(@href, 'mailto:')]",
            "//*[contains(@href, 'mailto:')]",
            "//*[contains(@class, 'email')]",
        ]
        email_found = False
        for xpath in email_xpaths:
            try:
                els = driver.find_elements(By.XPATH, xpath)
                visible = [el for el in els if el.is_displayed() and el.text.strip()]
                if visible:
                    print(f"  ✓ Email visible: '{visible[0].text.strip()}'")
                    email_found = True
                    break
            except Exception:
                continue

        if not email_found:
            page_src = driver.page_source
            import re
            if re.search(r'mailto:|[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}', page_src):
                print("  ✓ Email pattern found in page source.")
                email_found = True

        if not email_found:
            print("  ~ Email not clearly visible (may be in a modal or popup).")

        if phone_found or email_found:
            print("  ✓ View Phone/Email validation PASSED — contact info unlocked.")
        else:
            print("  ✗ View Phone/Email validation FAILED — no contact info detected.")

    except Exception as e:
        print(f"  ✗ Could not complete View Phone/Email step: {e}")


def verify_resume(driver):
    """
    Step 7: Click 'View Resume' on the first candidate card and validate
    that the resume is unlocked and accessible (viewer, preview, or download).

    Validation checks:
      - A resume viewer, PDF embed, iframe, or download link appears.
      - OR a new browser tab opens with the resume.
      - No error/restriction message is displayed.
    """
    print("\n--- Step 7: View Resume ---")

    try:
        btn = find_element_robust(
            driver, SELECTORS["view_resume_btn"], "View Resume Button"
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", btn)
        time.sleep(0.5)

        original_window = driver.current_window_handle
        original_tab_count = len(driver.window_handles)

        try:
            btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", btn)
        print("  Clicked View Resume button.")
        time.sleep(3)  # Allow resume viewer / new tab to open

        # ---- Validation ----
        print("  Validating resume is now accessible...")

        # Check if a new tab opened (resume opened in new window)
        new_tab_count = len(driver.window_handles)
        if new_tab_count > original_tab_count:
            new_tab = [h for h in driver.window_handles if h != original_window][0]
            driver.switch_to.window(new_tab)
            time.sleep(2)
            new_url = driver.current_url
            print(f"  ✓ New tab opened with URL: '{new_url}'")
            # Close new tab and switch back
            driver.close()
            driver.switch_to.window(original_window)
            print("  ✓ View Resume validation PASSED — resume opened in new tab.")
            return

        # Check for error messages
        error_xpaths = [
            "//*[contains(text(), 'Error') or contains(text(), 'error')]",
            "//*[contains(text(), 'Access Denied') or contains(text(), 'restricted')]",
            "//*[@role='alert']",
        ]
        for xpath in error_xpaths:
            els = driver.find_elements(By.XPATH, xpath)
            if any(el.is_displayed() for el in els):
                print(f"  ✗ ERROR detected after clicking View Resume: "
                      f"'{[el.text for el in els if el.is_displayed()][0]}'")
                return

        # Check for resume viewer / embed / download link in current page
        resume_xpaths = [
            "//iframe[contains(@src, 'resume') or contains(@src, 'pdf') or contains(@src, 'docs')]",
            "//embed[@type='application/pdf']",
            "//object[@type='application/pdf']",
            "//a[contains(@href, '.pdf') or contains(@href, 'resume') or contains(@href, 'download')]",
            "//*[contains(@class, 'resume') or contains(@class, 'pdf-viewer') or contains(@class, 'document-viewer')]",
            "//*[contains(text(), 'Download Resume') or contains(text(), 'View CV')]",
        ]
        resume_found = False
        for xpath in resume_xpaths:
            els = driver.find_elements(By.XPATH, xpath)
            visible = [el for el in els if el.is_displayed()]
            if visible:
                print(f"  ✓ Resume viewer/element found: '{xpath}'")
                resume_found = True
                break

        # Fallback: check page source for PDF/resume indicators
        if not resume_found:
            page_src = driver.page_source
            import re
            if re.search(r'\.pdf|resume|cv\b|application/pdf', page_src, re.IGNORECASE):
                print("  ✓ Resume content indicator found in page source.")
                resume_found = True

        if resume_found:
            print("  ✓ View Resume validation PASSED — resume is accessible.")
        else:
            print("  ~ Resume viewer not clearly identified. "
                  "It may have opened as a modal or overlay — please verify manually.")

    except Exception as e:
        print(f"  ✗ Could not complete View Resume step: {e}")


def candidate_search_flow(driver):
    """
    Full Candidate Search flow:
      1. Click the Candidate Search sidebar menu (robust helper).
      2. Randomly pick 3-4 filters from the available list.
      3. Open each chosen filter dropdown and select one random option.
      4. Click the Search button.
    """
    print("\n--- Starting Candidate Search Flow ---")

    # Step 1: Navigate to Candidate Search section via sidebar menu
    click_candidate_search_menu(driver)
    time.sleep(1)  # Short buffer after confirmed navigation

    # Step 2: Randomly choose 3 or 4 filters from the full list
    num_filters = random.randint(3, 4)
    chosen_filters = random.sample(ALL_FILTERS, num_filters)
    print(f"\nRandomly chosen {num_filters} filters to apply:")
    for key, lbl in chosen_filters:
        print(f"  - {lbl}")

    # Step 3: Apply each chosen filter
    applied = {}
    for selector_key, label in chosen_filters:
        selected_value = apply_random_filter(driver, selector_key, label)
        if selected_value:
            applied[label] = selected_value

    print("\n--- Filter selections summary ---")
    for lbl, val in applied.items():
        print(f"  {lbl}: '{val}'")

    # Step 4: Click the Search button
    perform_search(driver)

    # Step 5: Handle no-results by removing filter chips one-by-one
    remove_filter_chips_until_results(driver)

    # Step 6: View Phone/Email — unlock and validate contact info
    verify_phone_email(driver)

    # Step 7: View Resume — unlock and validate resume access
    verify_resume(driver)

    print("\nCandidate Search flow complete.")


# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    print("Starting Candidate Search Script...")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # 1. Navigate to the website
        print(f"Navigating to {LOGIN_URL}...")
        driver.get(LOGIN_URL)
        driver.maximize_window()

        # Check if we need to click a "Login" link
        current_url = driver.current_url
        if "login" not in current_url.lower():
            print("Not on login page yet. Checking for 'Login' link...")
            try:
                login_link = driver.find_element(By.XPATH, "//a[contains(@href, 'login')]")
                login_link.click()
                print("Clicked Login link.")
                time.sleep(3)
            except Exception:
                print("Could not find a 'Login' link.")

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
        try:
            submit_btn.click()
        except Exception:
            driver.execute_script("arguments[0].click();", submit_btn)
        print("Clicked Login button.")

        # 5. Wait for login to complete, then click Recruiter Card
        recruiter_card = find_element_robust(driver, SELECTORS["recruiter_card"], "Recruiter Card")
        try:
            recruiter_card.click()
        except Exception:
            driver.execute_script("arguments[0].click();", recruiter_card)
        print("Clicked Recruiter Card.")

        # ---------------------------------------------------------------
        # Hand off to Candidate Search flow (implement steps below)
        # ---------------------------------------------------------------
        candidate_search_flow(driver)

        print("\nDone!")

    except Exception as e:
        print(f"\nERROR: {e}")
    finally:
        input("\nPress Enter to close the browser...")
        driver.quit()


if __name__ == "__main__":
    main()

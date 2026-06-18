import time
import re
import random
import string
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    ElementClickInterceptedException,
    TimeoutException,
    StaleElementReferenceException,
)
CHROMEDRIVER_PATH = r"C:\Users\DELL9\.wdm\drivers\chromedriver\win64\148.0.7778.97\chromedriver.exe"

# --- CONFIGURATION ---
LOGIN_URL = "https://enterprise.ibns.in/"
EMAIL     = "new.enterprise@yopmail.com"
PASSWORD  = "Test@123"

# --- SELECTORS ---
SELECTORS = {
    "email":   [(By.NAME, "email"), (By.ID, "email"), (By.CSS_SELECTOR, "input[type='email']")],
    "password": [(By.NAME, "password"), (By.ID, "password"), (By.CSS_SELECTOR, "input[type='password']")],
    "submit_button": [
        (By.CSS_SELECTOR, "button[type='submit']"),
        (By.XPATH, "//button[contains(text(),'Login')]"),
        (By.XPATH, "//button[contains(text(),'Sign In')]"),
    ],
    # Membership Management dashboard card
    "membership_management": [
        (By.XPATH, "/html/body/div[2]/div/div/main/div/div[3]/button[1]/div/div/p"),
    ],
    # New Membership button (header)
    "new_membership_button": [
        (By.XPATH, "/html/body/div[2]/header/div/div[2]/div[2]/button"),
    ],
    # New Membership form fields
    "new_membership_input_1":  [(By.XPATH, "/html/body/form/div[2]/div/section/div[2]/div/div[1]/div/input")],
    "new_membership_input_2":  [(By.XPATH, "/html/body/form/div[2]/div/section/div[2]/div/div[2]/div[1]/div/div[2]/div/input")],
    "new_membership_input_3":  [(By.XPATH, "/html/body/form/div[2]/div/section/div[2]/div/div[3]/div/div/div/input")],
    "new_membership_input_4":  [(By.XPATH, "/html/body/form/div[2]/div/section/div[2]/div/div[4]/div/div/div/input")],
    "dropdown_button":         [(By.XPATH, "/html/body/form/div[2]/div/section/div[2]/div/div[2]/div[2]/div/div/button/div/span")],
    "final_submit_button":     [(By.XPATH, "/html/body/form/div[3]/div/button")],
    "error_message":           [(By.XPATH, "/html/body/section/ol/li/div/div/div/div[1]/div[2]/p[2]")],

    # Members Directory sidebar + New Member
    "members_directory_button": [(By.XPATH, "/html/body/div[2]/main/aside/aside/div/button[2]")],
    "new_member_button":        [(By.XPATH, "/html/body/div[2]/header/div/div[2]/div[2]/button")],

    # Add New Member form — confirmed from live dump
    "member_full_name":          [(By.NAME, "FullName")],
    # Birth date: placeholder has double "Enter" — use the calendar button instead
    "member_birth_date_input":   [(By.XPATH, "//input[@placeholder='Enter Enter Birth Date']")],
    "member_birth_date_calendar": [(By.ID, "base-ui-_r_3s_"), (By.XPATH, "(//button[@aria-label='Open calendar'])[1]")],
    "member_gender_dropdown":    [(By.ID, "_r_3t_"), (By.XPATH, "//button[@role='combobox']")],
    "member_professional_title": [(By.NAME, "ProfessionalTitle")],
    "member_bio":                [(By.NAME, "Bio")],
    "member_membership_title":   [(By.XPATH, "//input[@placeholder='Select Membership Title']")],
    "member_member_id":          [(By.NAME, "MemberId")],
    "member_enrollment_date_input":  [(By.XPATH, "//input[@placeholder='Enter Enrollment Date']")],
    "member_enrollment_calendar":    [(By.ID, "base-ui-_r_4c_"), (By.XPATH, "(//button[@aria-label='Open calendar'])[2]")],
    "member_renewal_date_input":     [(By.XPATH, "//input[@placeholder='Enter Renewal Date']")],
    "member_renewal_calendar":       [(By.ID, "base-ui-_r_4f_"), (By.XPATH, "(//button[@aria-label='Open calendar'])[3]")],
    "member_payment_remarks":    [(By.NAME, "LastPaymentRemarks")],
    "member_reference":          [(By.NAME, "Reference")],
    "member_mobile":             [(By.NAME, "MobileNumber")],
    "member_whatsapp":           [(By.NAME, "WhatsAppNumber")],
    "member_use_whatsapp_checkbox": [(By.ID, "useMobileAsWhatsapp")],
    "member_email":              [(By.NAME, "Email")],
    "member_address":            [(By.NAME, "CorrespondenceAddress")],
    "member_postal_code":        [(By.NAME, "CorrespondencePostalCode")],
    "member_country":            [(By.XPATH, "(//input[@placeholder='Select Country'])[1]")],
    "member_state":              [(By.XPATH, "(//input[@placeholder='Select State'])[1]")],
    "member_city":               [(By.XPATH, "(//input[@placeholder='Select City'])[1]")],
    "member_use_permanent_checkbox": [(By.ID, "sameAsCorr")],
    "member_permanent_address":  [(By.NAME, "PermanentAddress")],
    "member_permanent_postal":   [(By.NAME, "PermanentPostalCode")],
    "member_qualifications":     [(By.XPATH, "//input[@placeholder='Select Educational Qualifications']")],
    "member_work_specialty":     [(By.XPATH, "/html/body/form/div[2]/section[4]/div[2]/div/div[2]/div/div/div/input")],
    "member_license_number":     [(By.NAME, "PracticingLicenseNumber")],
    "member_submit_button":      [(By.XPATH, "//button[text()='Submit']")],
    "go_to_members_directory_button": [(By.XPATH, "/html/body/div[2]/div[3]/div[2]/div/div/button")],
}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def safe_click(driver, element):
    try:
        element.click()
    except (ElementClickInterceptedException, Exception):
        driver.execute_script("arguments[0].click();", element)


def find_element_robust(driver, selector_list, element_name, timeout=15):
    print(f"  Looking for {element_name}...")
    conditions = [EC.presence_of_element_located((by, val)) for by, val in selector_list]
    try:
        WebDriverWait(driver, timeout).until(EC.any_of(*conditions))
        for by, value in selector_list:
            els = driver.find_elements(by, value)
            if els:
                print(f"    Found via {by}='{value}'")
                return els[0]
        raise Exception("Wait succeeded but element not found.")
    except TimeoutException:
        raise Exception(f"Timed out waiting for: {element_name}")


def select_gender(driver, gender_value="Male"):
    gender_btn = find_element_robust(driver, SELECTORS["member_gender_dropdown"], "Gender Dropdown")
    safe_click(driver, gender_btn)
    time.sleep(1.5)
    # Try several option patterns — the combobox may use listbox/option or custom divs
    option_xpaths = [
        f"//*[@role='option' and contains(., '{gender_value}')]",
        f"//li[contains(., '{gender_value}')]",
        f"//div[@role='listbox']//*[contains(., '{gender_value}')]",
        f"//*[contains(@class,'option') and contains(., '{gender_value}')]",
        f"//*[contains(@class,'item') and contains(., '{gender_value}')]",
        f"//*[text()='{gender_value}']",
    ]
    for xpath in option_xpaths:
        try:
            opts = [o for o in driver.find_elements(By.XPATH, xpath) if o.is_displayed()]
            if opts:
                safe_click(driver, opts[0])
                print(f"    Selected gender: {gender_value}")
                return
        except Exception:
            continue
    print(f"    Warning: could not select gender '{gender_value}' — trying first visible option")


def select_autocomplete_option(driver, input_element, option_text=None, trigger_key="a"):
    """Click autocomplete input, trigger list, pick first or matching option."""
    safe_click(driver, input_element)
    time.sleep(0.8)

    option_xpath = "//*[@role='option'] | //div[contains(@class,'option')] | //li[contains(@class,'option')]"
    visible = [o for o in driver.find_elements(By.XPATH, option_xpath) if o.is_displayed()]
    if not visible:
        input_element.send_keys(trigger_key)
        time.sleep(1.5)

    try:
        WebDriverWait(driver, 8).until(EC.presence_of_element_located((By.XPATH, option_xpath)))
    except TimeoutException:
        print("    Warning: autocomplete options not found.")
        return

    options = [o for o in driver.find_elements(By.XPATH, option_xpath) if o.is_displayed()]
    if not options:
        print("    Warning: no visible options.")
        return

    if option_text:
        for opt in options:
            try:
                txt = opt.text
            except StaleElementReferenceException:
                continue
            if option_text.lower() in txt.lower():
                safe_click(driver, opt)
                print(f"    Selected '{txt}'")
                return

    # Read text before clicking to avoid stale ref after DOM re-render
    try:
        first_text = options[0].text
    except StaleElementReferenceException:
        first_text = "(stale)"
    safe_click(driver, options[0])
    print(f"    Selected first option: '{first_text}'")


def fill_date_via_calendar(driver, calendar_btn_selector_key, day, month, year):
    """
    Open the calendar picker. Strategy:
    1. Click the month/year header to open year/decade view for fast navigation.
    2. If that fails, navigate month-by-month (capped at 60 steps).
    3. Click the target day.
    """
    MONTH_NAMES = ["January","February","March","April","May","June",
                   "July","August","September","October","November","December"]
    target_month_str = MONTH_NAMES[month - 1]

    cal_btn = find_element_robust(driver, SELECTORS[calendar_btn_selector_key], calendar_btn_selector_key)
    safe_click(driver, cal_btn)
    time.sleep(1.2)

    # --- Strategy 1: click caption/header to get year-picker ---
    caption_xpaths = [
        "//*[contains(@class,'rdp-caption_label')]",
        "//*[contains(@class,'calendar-caption')]",
        "//button[contains(@class,'year')]",
        "//div[contains(@class,'DayPicker-Caption')]//div",
        "//*[@role='heading' and @aria-live]",
    ]
    jumped = False
    for cx in caption_xpaths:
        try:
            els = [e for e in driver.find_elements(By.XPATH, cx) if e.is_displayed()]
            if els:
                safe_click(driver, els[0])
                time.sleep(0.8)
                # Try clicking the target year
                year_el = driver.find_elements(By.XPATH, f"//*[normalize-space(text())='{year}' and @role='option' or normalize-space(text())='{year}']")
                visible_year = [e for e in year_el if e.is_displayed()]
                if visible_year:
                    safe_click(driver, visible_year[0])
                    time.sleep(0.8)
                    # Then click target month
                    month_el = driver.find_elements(By.XPATH,
                        f"//*[normalize-space(text())='{target_month_str}' or normalize-space(text())='{target_month_str[:3]}']")
                    visible_month = [e for e in month_el if e.is_displayed()]
                    if visible_month:
                        safe_click(driver, visible_month[0])
                        time.sleep(0.8)
                        jumped = True
                        break
        except Exception:
            continue

    if not jumped:
        # --- Strategy 2: month-by-month navigation (max 60 steps) ---
        for _ in range(60):
            try:
                header_xpaths = [
                    "//*[contains(@class,'rdp-caption_label')]",
                    "//*[@role='heading']",
                    "//div[contains(@class,'month-year')]",
                    "//*[contains(@class,'calendar-header')]",
                ]
                header_text = ""
                for hx in header_xpaths:
                    els = [e for e in driver.find_elements(By.XPATH, hx) if e.is_displayed() and e.text.strip()]
                    if els:
                        header_text = els[0].text.strip()
                        break

                if target_month_str in header_text and str(year) in header_text:
                    break

                years_found  = re.findall(r'\d{4}', header_text)
                months_found = [m for m in MONTH_NAMES if m in header_text]
                current_year  = int(years_found[0])  if years_found  else year
                current_month = MONTH_NAMES.index(months_found[0]) + 1 if months_found else month

                go_forward = (current_year < year) or (current_year == year and current_month < month)

                next_xpaths = [
                    "//button[@aria-label='Go to next month']",
                    "//button[@aria-label='Next month']",
                    "//button[contains(@class,'next')]",
                    "//button[contains(@aria-label,'next')]",
                ]
                prev_xpaths = [
                    "//button[@aria-label='Go to previous month']",
                    "//button[@aria-label='Previous month']",
                    "//button[contains(@class,'prev')]",
                    "//button[contains(@aria-label,'prev')]",
                ]
                nav_xpaths = next_xpaths if go_forward else prev_xpaths
                clicked = False
                for nx in nav_xpaths:
                    btns = [b for b in driver.find_elements(By.XPATH, nx) if b.is_displayed()]
                    if btns:
                        safe_click(driver, btns[0])
                        clicked = True
                        time.sleep(0.3)
                        break
                if not clicked:
                    print(f"    Warning: can't navigate calendar. Header='{header_text}'")
                    break
            except Exception as nav_err:
                print(f"    Calendar nav error: {nav_err}")
                break

    # --- Click the target day ---
    day_xpaths = [
        f"//button[@aria-label and contains(@aria-label,'{day}') and contains(@aria-label,'{target_month_str}')]",
        f"//*[contains(@class,'day') and normalize-space(text())='{day}' and not(@disabled)]",
        f"//button[normalize-space(text())='{day}' and not(@disabled) and not(contains(@class,'outside'))]",
        f"//*[@role='gridcell' and normalize-space(text())='{day}' and not(@aria-disabled='true')]",
    ]
    clicked_day = False
    for dx in day_xpaths:
        try:
            days = [d for d in driver.find_elements(By.XPATH, dx)
                    if d.is_displayed() and not d.get_attribute("disabled")]
            if days:
                safe_click(driver, days[0])
                clicked_day = True
                print(f"    Selected date: {day:02d}-{month:02d}-{year}")
                break
        except Exception:
            continue

    if not clicked_day:
        print(f"    Warning: could not click day {day}. Falling back to JS injection...")
        # Fallback: JS inject into the hidden/read-only input
        try:
            inp_map = {
                "member_birth_date_calendar":   "member_birth_date_input",
                "member_enrollment_calendar":   "member_enrollment_date_input",
                "member_renewal_calendar":      "member_renewal_date_input",
            }
            inp_key = inp_map.get(calendar_btn_selector_key)
            if inp_key:
                el = find_element_robust(driver, SELECTORS[inp_key], inp_key)
                date_str = f"{day:02d}-{month:02d}-{year}"
                driver.execute_script(
                    """
                    var nv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    nv.call(arguments[0], arguments[1]);
                    arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                    arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
                    """, el, date_str)
                print(f"    JS-injected date: {date_str}")
            # close calendar
            driver.find_element(By.TAG_NAME, "body").click()
        except Exception as fb_err:
            print(f"    Fallback JS injection failed: {fb_err}")

    time.sleep(0.5)


def is_valid_option(text, max_len=60):
    """Filter out garbage test data — skip very long entries or entries starting with @@ or numbers."""
    t = text.strip()
    if not t:
        return False
    if len(t) > max_len:
        return False
    # Skip obvious test/junk entries
    if t.startswith("@@") or t.startswith("111") or t[:1].isdigit():
        return False
    return True


def pick_best_option(opts):
    """Return the best option from a list — prefer valid-looking entries, fall back to first."""
    for opt in opts:
        try:
            txt = opt.text.strip()
        except StaleElementReferenceException:
            continue
        if is_valid_option(txt):
            return opt, txt
    # fallback: first option regardless
    try:
        return opts[0], opts[0].text.strip()
    except StaleElementReferenceException:
        return opts[0], "(stale)"


def select_country_state_city(driver, country_name="India"):
    """
    Select country (exact match preferred), then state, then city.
    If city has no options after selecting a state, tries up to 5 other states.
    """
    opt_xpath = "//*[@role='option'] | //div[contains(@class,'option')] | //li[contains(@class,'option')]"

    # --- Country ---
    print("  Selecting Country...")
    country_el = find_element_robust(driver, SELECTORS["member_country"], "Country")
    safe_click(driver, country_el)
    time.sleep(0.5)
    driver.execute_script("arguments[0].value = '';", country_el)
    country_el.send_keys(country_name)
    time.sleep(2.5)

    opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
    selected_country = False
    if opts:
        # Exact match first
        for opt in opts:
            try:
                txt = opt.text.strip()
            except StaleElementReferenceException:
                continue
            if txt.lower() == country_name.lower():
                safe_click(driver, opt)
                print(f"    Country selected (exact): '{txt}'")
                selected_country = True
                break
        # Starts-with
        if not selected_country:
            for opt in opts:
                try:
                    txt = opt.text.strip()
                except StaleElementReferenceException:
                    continue
                if txt.lower().startswith(country_name.lower()) and is_valid_option(txt):
                    safe_click(driver, opt)
                    print(f"    Country selected (starts-with): '{txt}'")
                    selected_country = True
                    break
        # Contains fallback
        if not selected_country:
            for opt in opts:
                try:
                    txt = opt.text.strip()
                except StaleElementReferenceException:
                    continue
                if country_name.lower() in txt.lower():
                    safe_click(driver, opt)
                    print(f"    Country selected (contains): '{txt}'")
                    selected_country = True
                    break
    if not selected_country:
        print(f"    Warning: no country options for '{country_name}'")

    time.sleep(3)

    # --- State + City with retry ---
    # Collect all state options first, then iterate until city loads
    print("  Selecting State...")
    state_el = find_element_robust(driver, SELECTORS["member_state"], "State")
    safe_click(driver, state_el)
    time.sleep(1.5)
    all_state_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
    if not all_state_opts:
        for key in (" ", "a", "e"):
            state_el.send_keys(key)
            time.sleep(2)
            all_state_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
            if all_state_opts:
                break
            driver.execute_script("arguments[0].value = '';", state_el)

    if not all_state_opts:
        print("    Warning: no state options found at all")
        return

    # Try each state until city has options (max 5 attempts)
    city_found = False
    tried_states = 0
    for state_opt in all_state_opts[:5]:
        try:
            stxt = state_opt.text.strip()
        except StaleElementReferenceException:
            stxt = "(stale)"

        # Re-open state dropdown if not first attempt
        if tried_states > 0:
            state_el = find_element_robust(driver, SELECTORS["member_state"], "State")
            safe_click(driver, state_el)
            time.sleep(1.5)
            # Re-fetch options since DOM may have refreshed
            fresh_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
            if tried_states < len(fresh_opts):
                state_opt = fresh_opts[tried_states]
                try:
                    stxt = state_opt.text.strip()
                except StaleElementReferenceException:
                    stxt = "(stale)"

        safe_click(driver, state_opt)
        print(f"    State selected: '{stxt}'")
        tried_states += 1
        time.sleep(3)

        # Check city
        print("  Selecting City...")
        city_el = find_element_robust(driver, SELECTORS["member_city"], "City")
        safe_click(driver, city_el)
        time.sleep(1.5)
        city_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
        if not city_opts:
            for key in (" ", "a", "e"):
                city_el.send_keys(key)
                time.sleep(2)
                city_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
                if city_opts:
                    break
                driver.execute_script("arguments[0].value = '';", city_el)

        if city_opts:
            opt_el, ctxt = pick_best_option(city_opts)
            safe_click(driver, opt_el)
            print(f"    City selected: '{ctxt}'")
            city_found = True
            break
        else:
            print(f"    City not found for state '{stxt}', trying next state...")
            # Dismiss city dropdown
            try:
                driver.find_element(By.TAG_NAME, "body").click()
            except Exception:
                pass
            time.sleep(0.5)

    if not city_found:
        print("    Warning: could not find city options for any tried state")

def select_work_specialty(driver):
    """
    Robustly select Work Specialty (optional) with retries.
    Tries mouse selection first, then keyboard fallback.
    """
    print("  Selecting Work Specialty...")
    opt_xpath = "//*[@role='option'] | //div[contains(@class,'option')] | //li[contains(@class,'option')]"
    trigger_text = "a"

    for attempt in range(1, 4):
        try:
            spec_el = find_element_robust(driver, SELECTORS["member_work_specialty"], "Work Specialty")
            driver.execute_script("arguments[0].scrollIntoView({block:'center'});", spec_el)
            safe_click(driver, spec_el)
            time.sleep(0.8)

            # Trigger option loading in typeahead dropdowns
            driver.execute_script("arguments[0].focus();", spec_el)
            spec_el.send_keys(Keys.CONTROL, "a")
            spec_el.send_keys(Keys.BACKSPACE)
            spec_el.send_keys(trigger_text)
            time.sleep(1.6)

            spec_opts = [o for o in driver.find_elements(By.XPATH, opt_xpath) if o.is_displayed()]
            valid_opts = []
            for o in spec_opts:
                try:
                    t = o.text.strip()
                except StaleElementReferenceException:
                    continue
                # For Work Specialty, ignore tiny trigger-like text and obvious junk
                if is_valid_option(t) and len(t) > 1 and t.lower() != trigger_text:
                    valid_opts.append(o)

            if valid_opts:
                opt_el, stxt = pick_best_option(valid_opts)
                safe_click(driver, opt_el)
                time.sleep(0.8)
                selected_val = (spec_el.get_attribute("value") or "").strip()
                if selected_val and selected_val.lower() != trigger_text:
                    print(f"    Work Specialty selected: '{selected_val}'")
                    return True
                print(f"    Clicked specialty option '{stxt}', but input value is '{selected_val}'. Applying hard fallback.")
                # Hard fallback: set chosen option text directly and dispatch events
                driver.execute_script(
                    """
                    var nv = Object.getOwnPropertyDescriptor(window.HTMLInputElement.prototype,'value').set;
                    nv.call(arguments[0], arguments[1]);
                    arguments[0].dispatchEvent(new Event('input',{bubbles:true}));
                    arguments[0].dispatchEvent(new Event('change',{bubbles:true}));
                    arguments[0].dispatchEvent(new Event('blur',{bubbles:true}));
                    """,
                    spec_el,
                    stxt,
                )
                time.sleep(0.5)
                selected_val = (spec_el.get_attribute("value") or "").strip()
                if selected_val and selected_val.lower() != trigger_text:
                    print(f"    Work Specialty selected via hard fallback: '{selected_val}'")
                    return True

            # Keyboard fallback for custom listboxes
            spec_el.send_keys(Keys.ARROW_DOWN)
            time.sleep(0.3)
            spec_el.send_keys(Keys.ENTER)
            time.sleep(0.8)
            selected_val = (spec_el.get_attribute("value") or "").strip()
            if selected_val and selected_val.lower() != trigger_text:
                print(f"    Work Specialty selected via keyboard: '{selected_val}'")
                return True

            print(f"    Retry {attempt}/3: no selectable Work Specialty option yet.")
            time.sleep(1.0)
        except Exception as e:
            print(f"    Retry {attempt}/3 due to Work Specialty error: {e}")
            time.sleep(1.0)

    print("    Warning: no work specialty option selected (field is optional).")
    return False
def close_open_dropdowns(driver, max_tries=4):
    """
    Force-close any open combobox/listbox dropdowns before interacting with the next field.
    """
    option_xpath = "//*[@role='option'] | //div[contains(@class,'option')] | //li[contains(@class,'option')]"
    for _ in range(max_tries):
        visible = [o for o in driver.find_elements(By.XPATH, option_xpath) if o.is_displayed()]
        if not visible:
            return
        try:
            driver.find_element(By.TAG_NAME, "body").click()
        except Exception:
            pass
        try:
            active = driver.switch_to.active_element
            active.send_keys(Keys.ESCAPE)
        except Exception:
            pass
        time.sleep(0.4)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    print("=" * 60)
    print("  Membership Management Automation")
    print("=" * 60)

    service = Service(CHROMEDRIVER_PATH)
    driver  = webdriver.Chrome(service=service)

    try:
        # ── 1. Login ──────────────────────────────────────────────
        print("\n[1] Logging in...")
        driver.get(LOGIN_URL)
        driver.maximize_window()
        time.sleep(2)

        if "login" not in driver.current_url.lower():
            try:
                driver.find_element(By.XPATH, "//a[contains(@href,'login')]").click()
                time.sleep(2)
            except Exception:
                pass

        email_el = find_element_robust(driver, SELECTORS["email"], "Email")
        email_el.clear(); email_el.send_keys(EMAIL)

        pwd_el = find_element_robust(driver, SELECTORS["password"], "Password")
        pwd_el.clear(); pwd_el.send_keys(PASSWORD)

        safe_click(driver, find_element_robust(driver, SELECTORS["submit_button"], "Login Button"))
        time.sleep(4)
        print(f"  Logged in. URL: {driver.current_url}")

        # ── 2. Membership Management ──────────────────────────────
        print("\n[2] Opening Membership Management...")
        safe_click(driver, find_element_robust(driver, SELECTORS["membership_management"], "Membership Management"))
        time.sleep(3)

        # ── 3. New Membership ─────────────────────────────────────
        print("\n[3] Creating New Membership...")
        safe_click(driver, find_element_robust(driver, SELECTORS["new_membership_button"], "New Membership Button"))
        time.sleep(2)

        i1 = find_element_robust(driver, SELECTORS["new_membership_input_1"], "Membership Title")
        i1.send_keys("Test Entry 1")
        find_element_robust(driver, SELECTORS["new_membership_input_2"], "Input 2").send_keys("Test Entry 2")
        find_element_robust(driver, SELECTORS["new_membership_input_3"], "Input 3 (Amount)").send_keys("100")
        find_element_robust(driver, SELECTORS["new_membership_input_4"], "Input 4 (Description)").send_keys("Test Description")

        # Dropdown
        safe_click(driver, find_element_robust(driver, SELECTORS["dropdown_button"], "Dropdown Button"))
        time.sleep(1.5)
        option_xpath = "//*[contains(@role,'option')] | //li[contains(@class,'option')] | //div[contains(@class,'select-item')]"
        opts = [o for o in driver.find_elements(By.XPATH, option_xpath) if o.is_displayed()]
        if opts:
            try:
                opt_text = opts[0].text
            except StaleElementReferenceException:
                opt_text = "(stale)"
            safe_click(driver, opts[0])
            print(f"  Selected dropdown option: '{opt_text}'")
        else:
            print("  Warning: no dropdown options found.")

        # Submit
        safe_click(driver, find_element_robust(driver, SELECTORS["final_submit_button"], "Final Submit"))
        time.sleep(2)

        # Error / duplicate retry
        try:
            err_el = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, SELECTORS["error_message"][0][1]))
            )
            if err_el.is_displayed():
                print("  Duplicate detected — retrying with unique title...")
                title_el = find_element_robust(driver, SELECTORS["new_membership_input_1"], "Membership Title")
                title_el.clear()
                driver.execute_script("arguments[0].value = '';", title_el)
                new_title = f"Test Entry {int(time.time())}"
                title_el.send_keys(new_title)
                time.sleep(0.5)
                # Re-find submit button (avoid stale reference)
                safe_click(driver, find_element_robust(driver, SELECTORS["final_submit_button"], "Final Submit (retry)"))
                print(f"  Resubmitted with title: {new_title}")
        except TimeoutException:
            print("  No duplicate error. Continuing...")

        # ── 4. Members Directory ──────────────────────────────────
        print("\n[4] Navigating to Members Directory...")
        time.sleep(3)
        safe_click(driver, find_element_robust(driver, SELECTORS["members_directory_button"], "Members Directory"))
        time.sleep(3)

        # ── 5. New Member ─────────────────────────────────────────
        print("\n[5] Opening Add New Member form...")
        safe_click(driver, find_element_robust(driver, SELECTORS["new_member_button"], "New Member Button"))
        time.sleep(4)

        # ── 6. Fill Add New Member Form ───────────────────────────
        print("\n[6] Filling Add New Member form...")
        suffix = ''.join(random.choices(string.ascii_uppercase, k=6))

        # Full Name
        fn = find_element_robust(driver, SELECTORS["member_full_name"], "Full Name")
        fn.send_keys(f"Test Member {suffix}")

        # Birth Date — use calendar picker
        fill_date_via_calendar(driver, "member_birth_date_calendar", day=15, month=8, year=2000)

        # Gender
        select_gender(driver, "Male")

        # Professional Title
        find_element_robust(driver, SELECTORS["member_professional_title"], "Professional Title").send_keys("Healthcare Specialist")

        # Bio
        find_element_robust(driver, SELECTORS["member_bio"], "Bio").send_keys(
            "Healthcare consultant specializing in clinical operations and patient care management."
        )

        # Membership Title (autocomplete)
        mt = find_element_robust(driver, SELECTORS["member_membership_title"], "Membership Title")
        select_autocomplete_option(driver, mt)

        # Member ID
        find_element_robust(driver, SELECTORS["member_member_id"], "Member ID").send_keys(f"ID{suffix}")

        # Enrollment Date — use calendar picker
        fill_date_via_calendar(driver, "member_enrollment_calendar", day=1, month=6, year=2026)

        # Renewal Date — use calendar picker
        fill_date_via_calendar(driver, "member_renewal_calendar", day=1, month=6, year=2027)

        # Payment Remarks
        find_element_robust(driver, SELECTORS["member_payment_remarks"], "Payment Remarks").send_keys("Stripe TXN 549302")

        # Reference
        find_element_robust(driver, SELECTORS["member_reference"], "Reference").send_keys("Dr. Robert Chen")

        # Mobile
        find_element_robust(driver, SELECTORS["member_mobile"], "Mobile Number").send_keys("9876543210")

        # Use Mobile as WhatsApp checkbox
        try:
            chk = find_element_robust(driver, SELECTORS["member_use_whatsapp_checkbox"], "WhatsApp Checkbox")
            if not chk.is_selected():
                safe_click(driver, chk)
            print("  Checked: Use Mobile as WhatsApp")
        except Exception as e:
            print(f"  Checkbox fallback — filling WhatsApp directly: {e}")
            find_element_robust(driver, SELECTORS["member_whatsapp"], "WhatsApp Number").send_keys("9876543210")

        # Email
        find_element_robust(driver, SELECTORS["member_email"], "Email").send_keys(
            f"member.{int(time.time())}@yopmail.com"
        )

        # Correspondence Address
        find_element_robust(driver, SELECTORS["member_address"], "Correspondence Address").send_keys(
            "123 Test Residency, Corporate Road"
        )

        # Correspondence Postal Code
        find_element_robust(driver, SELECTORS["member_postal_code"], "Postal Code").send_keys("380015")

        # Country → State → City (cascading, with waits)
        select_country_state_city(driver, country_name="India")

        # "Same as Correspondence Address" checkbox for Permanent Address
        try:
            perm_chk = find_element_robust(driver, SELECTORS["member_use_permanent_checkbox"], "Permanent Address Checkbox")
            if not perm_chk.is_selected():
                safe_click(driver, perm_chk)
            print("  Checked: Same as Correspondence for Permanent Address")
        except Exception as e:
            print(f"  Could not check Permanent Address checkbox: {e}")
            # Fill permanent address manually as fallback
            try:
                find_element_robust(driver, SELECTORS["member_permanent_address"], "Permanent Address").send_keys(
                    "123 Test Residency, Corporate Road"
                )
                find_element_robust(driver, SELECTORS["member_permanent_postal"], "Permanent Postal").send_keys("380015")
            except Exception:
                pass

        # Dismiss any open dropdown by clicking form header
        time.sleep(0.5)
        try:
            hdr = driver.find_element(By.XPATH, "//h2 | //div[contains(text(),'Add New Member')]")
            hdr.click()
        except Exception:
            pass
        time.sleep(0.5)

        # Educational Qualifications (autocomplete)
        close_open_dropdowns(driver)
        qual_el = find_element_robust(driver, SELECTORS["member_qualifications"], "Educational Qualifications")
        select_autocomplete_option(driver, qual_el)
        # Ensure Education dropdown is fully closed before Work Specialty
        close_open_dropdowns(driver)
        time.sleep(0.5)

        # Work Specialty (optional)
        close_open_dropdowns(driver)
        select_work_specialty(driver)
        # Ensure Work Specialty dropdown is closed after selection
        close_open_dropdowns(driver)
        time.sleep(0.5)

        # License Number
        find_element_robust(driver, SELECTORS["member_license_number"], "License Number").send_keys("LIC98765432")

        # ── 7. Submit ─────────────────────────────────────────────
        print("\n[7] Submitting Add New Member form...")
        submit_btn = find_element_robust(driver, SELECTORS["member_submit_button"], "Member Submit Button")
        safe_click(driver, submit_btn)
        time.sleep(5)

        # After submit, click popup button: Go to Members Directory
        try:
            go_btn = find_element_robust(
                driver,
                SELECTORS["go_to_members_directory_button"],
                "Go to Members Directory Button",
                timeout=12
            )
            safe_click(driver, go_btn)
            time.sleep(2)
            print("  Clicked popup button: Go to Members Directory")
        except Exception as e:
            print(f"  Warning: could not click Go to Members Directory popup button: {e}")
        print("\n✓ Add New Member form submitted successfully!")
        print("Tasks complete!")

    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback; traceback.print_exc()
    finally:
        input("\nPress Enter to close the browser...")
        driver.quit()


if __name__ == "__main__":
    main()

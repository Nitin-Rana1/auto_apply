from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import random

# ===== Helper Wait Functions =====
def short_wait():
    print("⏳ Short wait...")
    time.sleep(random.uniform(1, 2.5))

def medium_wait():
    print("⏳ Medium wait...")
    time.sleep(random.uniform(3, 5.5))

def long_wait():
    print("⏳ Long wait...")
    time.sleep(random.uniform(6.5, 8.5))

# ===== Scroll Function =====
def scroll_page(driver, times=5):
    print(f"🔄 Scrolling page {times} times...")
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"   ➡ Scroll {i+1}/{times} done")
        short_wait()

# ===== Apply to Jobs =====
# ===== Apply to Jobs =====
def apply_to_jobs(driver, max_applications):
    print(f"🚀 Starting job application process (max {max_applications})...")
    
    # Get all "View »" buttons first
    view_buttons = driver.find_elements(
        By.XPATH,
        "//button[contains(@class, 'button-interested') and contains(text(), 'View')]"
    )

    total_jobs = len(view_buttons)
    print(f"🔍 Found {total_jobs} 'View »' buttons on the page.")

    applied = 0
    for i, view_button in enumerate(view_buttons):
        if applied >= max_applications:
            print("✅ Reached max applications limit.")
            break

        try:
            print(f"🟡 Opening job ({applied + 1}/{max_applications})...")
            highlight_element(driver, view_button)
            driver.execute_script("arguments[0].scrollIntoView(true);", view_button)
            driver.execute_script("arguments[0].click();", view_button)
            medium_wait()

            # Find and click Apply button
            apply_buttons = driver.find_elements(By.XPATH, "//button[text()='Apply']")
            if not apply_buttons:
                print("⚠️ No 'Apply' button found in job details.")
                driver.find_element(By.XPATH, "//button[@class='back-button-modal-close']").click()
                continue

            highlight_element(driver, apply_buttons[0])
            driver.execute_script("arguments[0].click();", apply_buttons[0])
            applied += 1
            print("✅ Application submitted.")

            # Close job details popup
            close_button = driver.find_element(By.XPATH, "//button[@class='back-button-modal-close']")
            highlight_element(driver, close_button)
            driver.execute_script("arguments[0].click();", close_button)

            long_wait()

        except Exception as e:
            print(f"⚠️ Error applying to job {i+1}: {e}")
            short_wait()
            continue

    print(f"✅ Done: Applied to {applied} jobs out of {total_jobs} found.")

# ===== Highlight Element (for debugging) =====
def highlight_element(driver, element):
    try:
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
    except Exception as e:
        print(f"⚠️ Could not highlight element: {e}")

# ===== Step 3: Fill Experience =====
def fill_experience_and_search(driver, exp):
    try:
        print("🔍 Waiting for experience input field (#years)...")
        exp_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "years"))
        )
        highlight_element(driver, exp_input)
        driver.execute_script("arguments[0].scrollIntoView(true);", exp_input)
        short_wait()

        print("📝 Clearing and entering experience value: 1")
        exp_input.clear()
        exp_input.send_keys(exp)
        print("✅ Experience value entered.")

        print("🔍 Waiting for 'Show Results' button (#show-results)...")
        show_results_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.ID, "show-results"))
        )
        highlight_element(driver, show_results_btn)
        driver.execute_script("arguments[0].click();", show_results_btn)
        print("✅ 'Show Results' button clicked.")
        long_wait()

    except Exception as e:
        print(f"⚠️ Error setting experience: {e}")

# ===== Chrome Setup =====
def set_up_headless_chrome(background_run=False):
    print("🔹 Setting up Chrome driver...")
    options = Options()
    if background_run:
        print("   Running in headless mode.")
        options.add_argument("--headless=new")
        options.add_argument("--disable-gpu")
        options.add_argument("--window-size=1920,1080")
    else:
        print("   Running in visible mode.")
        options.add_argument("--start-maximized")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("✅ Chrome driver ready.")
    return driver

# ===== Login Function =====
def loginInto(driver, website_login_page, email, password):
    print(f"🔍 Navigating to login page: {website_login_page}")
    driver.get(website_login_page)
    medium_wait()

    print("📝 Entering email...")
    driver.find_element(By.NAME, "email").send_keys(email)
    short_wait()

    print("📝 Entering password...")
    driver.find_element(By.NAME, "password").send_keys(password)
    short_wait()

    print("🔘 Clicking login button...")
    login_btn = driver.find_element(By.XPATH, "//button[@type='submit' and normalize-space(text())='Login']")
    highlight_element(driver, login_btn)
    login_btn.click()
    long_wait()
    print("✅ Login complete.")

# ===== Navigate to Job Page =====
def goToJobPage(driver, job_page):
    print(f"🔍 Navigating to {job_page['url']}...")
    driver.get(job_page["url"])
    long_wait()
    print("✅ Job page loaded.")

# # ===== MAIN SCRIPT =====
# if __name__ == "__main__":
#     load_dotenv()
#     email = os.getenv("EMAIL")
#     password = os.getenv("PASSWORD")

#     if not email or not password:
#         print("❌ EMAIL or PASSWORD not set in .env file. Exiting.")
#         exit()

#     job_page = {
#         "url": "https://www.instahyre.com/candidate/opportunities/?matching=true",
#         "max_applications": 50
#     }

#     driver = set_up_headless_chrome(background_run=False)
#     loginInto(driver, "https://www.instahyre.com/login/", email, password)
#     goToJobPage(driver, job_page)
#     fill_experience_and_search(driver)
#     apply_to_jobs(driver, job_page["max_applications"])

#     print("\n🎉 Script complete. Closing browser.")
#     driver.quit()

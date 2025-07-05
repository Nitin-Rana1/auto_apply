from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import random


# Load .env from current directory
load_dotenv()

# Read credentials
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")

# Debug print
print("EMAIL:", repr(email))
print("PASSWORD:", repr(password))


# Job types and their URLs
job_pages = [
    {
        "name": "Full-Time Jobs",
        "url": "https://cuvette.tech/app/student/jobs/fulltimeJobs/filters?sortByDate=true",
        "max_applications": 50
    },
    {
        "name": "Internships",
        "url": "https://cuvette.tech/app/student/jobs/internships/filters?sortByDate=true",
        "max_applications": 50
    }
]

# --- Helper Functions ---
def short_wait():
    time.sleep(random.uniform(1, 2.5))

def long_wait():
    time.sleep(random.uniform(3, 5.5))

def scroll_page(driver, times=5):
    for _ in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        short_wait()

def apply_to_jobs(driver, max_applications):
    applied = 0
    while applied < max_applications:
        try:
            apply_buttons = driver.find_elements(By.XPATH, "//button[text()='Apply Now']")
            if not apply_buttons:
                print("✅ No more Apply Now buttons found.")
                break

            print(f"🟡 Applying ({applied + 1}/{max_applications})...")

            first_button = apply_buttons[0]
            driver.execute_script("arguments[0].scrollIntoView(true);", first_button)
            short_wait()
            driver.execute_script("arguments[0].click();", first_button)
            applied += 1
            long_wait()

            # Go back if redirected
            if "jobs" not in driver.current_url:
                driver.back()
                long_wait()

        except Exception as e:
            print(f"⚠️ Error during click: {e}")
            short_wait()
            continue

    print(f"✅ Done: Applied to {applied} jobs.")

# --- Setup Headless Chrome ---
background_run = False  # ✅ Set this to True for headless (background), False to show browser

options = Options()

if background_run:
    options.add_argument("--headless=new")       # Run without UI
    options.add_argument("--disable-gpu")        # Recommended for headless
    options.add_argument("--window-size=1920,1080")  # Ensure full-size rendering
else:
    options.add_argument("--start-maximized")    # Open full-screen for visual automation

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# --- Step 1: Login ---
driver.get("https://cuvette.tech/app/student/login")
short_wait()
driver.find_element(By.NAME, "email").send_keys(email)
short_wait()
driver.find_element(By.NAME, "password").send_keys(password)
short_wait()
driver.find_element(By.XPATH, "//button[@type='submit' and .//span[text()='Login']]").click()
long_wait()

# --- Step 2: Go through each job page ---
for job in job_pages:
    print(f"\n🔁 Now applying for: {job['name']}")
    driver.get(job["url"])
    long_wait()
    scroll_page(driver, times=5)
    apply_to_jobs(driver, job["max_applications"])

# --- Done ---
print("\n🎉 Script complete. Closing browser.")
driver.quit()
# --- End of Script ---
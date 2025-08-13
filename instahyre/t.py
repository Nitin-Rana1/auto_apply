from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
import os
import time
import random
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from helper import *


# Load .env from current directory
load_dotenv()

# Read credentials
email = os.getenv("EMAIL")
password = os.getenv("PASSWORD")


# Job types and their URLs
job_page_info = {
        "url": "https://www.instahyre.com/candidate/opportunities/?matching=true",
        "max_applications": 50
    }

background_run = False  # ✅ Set this to True for headless (background), False to show browser

# --- Setup Headless Chrome ---
driver = set_up_headless_chrome(background_run)

# --- Step 1: Login ---


loginInto(driver, "https://www.instahyre.com/login/", email, password)

# --- Step 2: Go to job page ---
goToJobPage(driver, job_page_info)





total_jobs = fill_exp_and_apply_all_pages_jobs(driver)

print(f"Total jobs applied: {total_jobs}")


# --- Done ---
print("\n🎉 Script complete. Closing browser.")
driver.quit()
# --- End of Script ---
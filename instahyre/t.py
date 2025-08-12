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
job_page = {
        "url": "https://www.instahyre.com/candidate/opportunities/?matching=true",
        "max_applications": 50
    }

background_run = False  # ✅ Set this to True for headless (background), False to show browser

# --- Setup Headless Chrome ---
driver = set_up_headless_chrome(background_run)

# --- Step 1: Login ---


loginInto(driver, "https://www.instahyre.com/login/", email, password)

# --- Step 2: Go to job page ---
goToJobPage(driver, job_page)


fill_experience_and_search(driver, "0")


apply_to_jobs(driver, job_page["max_applications"])

# --- Done ---
print("\n🎉 Script complete. Closing browser.")
driver.quit()
# --- End of Script ---
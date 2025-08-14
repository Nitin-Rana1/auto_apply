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

# ===== Scroll Function =====
def scroll_page(driver, times=5):
    print(f"🔄 Scrolling page {times} times...")
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        print(f"   ➡ Scroll {i+1}/{times} done")
        short_wait()

# ===== Highlight Element (for debugging) =====
def highlight_element(driver, element):
    try:
        driver.execute_script("arguments[0].style.border='3px solid red'", element)
    except Exception as e:
        print(f"⚠️ Could not highlight element: {e}")

# ===== Helper Wait Functions =====
def short_wait():
    print("⏳ Short wait...")
    time.sleep(random.uniform(1, 2.5))

def medium_wait():
    print("⏳ Medium wait...")
    time.sleep(random.uniform(3, 5))

def long_wait():
    print("⏳ Long wait...")
    time.sleep(random.uniform(5, 7))

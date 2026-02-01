


from random import random
import time

from helper_methods import *


class AutoApply:
    driver = None
    background_run = False
    total_jobs = 0

    email = None
    password = None
    website_login_page = None
    
    # Job types and their URLs
    job_page_info = None
    
    def __init__(self, email, password, website_login_page, job):
        self.email = email
        self.password = password
        self.website_login_page = website_login_page
        self.job_page_info = job

        print("🔹 Setting up Chrome driver...")
        options = Options()
        if self.background_run:
            print("   Running in headless mode.")
            options.add_argument("--headless=new")
            options.add_argument("--disable-gpu")
            options.add_argument("--window-size=1920,1080")
        else:
            print("   Running in visible mode.")
            options.add_argument("--start-maximized")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        print("✅ Chrome driver ready.")
    
        self.driver = driver
        self.total_jobs = 0
     # ===== Chrome Setup =====
       


    def step_1_login(self, website_login_page, email, password):
        loginInto(self.driver, website_login_page, email, password)

    def step_2_go_to_job_page(self, job_page):
        goToJobPage(self.driver, job_page)

    def step_3_fill_experience_and_apply(self):
        try:
            print("🔍 Waiting for experience input field (#years)...")
            exp_input = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.ID, "years"))
            )
            highlight_element(self.driver, exp_input)
            self.driver.execute_script("arguments[0].scrollIntoView(true);", exp_input)
            short_wait()

            print("📝 Clearing and entering experience value: 1")
            exp_input.clear()
            exp_input.send_keys('1')
            print("✅ Experience value entered.")

            print("🔍 Waiting for 'Show Results' button (#show-results)...")
            show_results_btn = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "show-results"))
            )
            highlight_element(self.driver, show_results_btn)
            self.driver.execute_script("arguments[0].click();", show_results_btn)
            print("✅ 'Show Results' button clicked.")
            long_wait()

        except Exception as e:
            print(f"⚠️ Error setting experience: {e}")


        while True:
            print("\n📄 Processing new page...")
            
            # Apply to jobs on this page
            applied_this_page = self.apply_to_jobs()

            # Try to find the Next » button
            try:
                next_btn = self.driver.find_element(
                    By.XPATH,
                    "//li[contains(@ng-click, 'nextPage') and not(contains(@class,'hidden'))]"
                )
                print("➡️ Clicking 'Next »' to go to next page...")
                self.driver.execute_script("arguments[0].scrollIntoView(true);", next_btn)
                self.driver.execute_script("arguments[0].click();", next_btn)
                long_wait()  # wait for next page jobs to load
            except:
                print("✅ No 'Next »' button found. Reached last page.")
                break

    
    def step_4_finalize(self):
        print("🔚 Finalizing...")
        self.driver.quit()

    # ===== Apply to Jobs =====
    def apply_to_jobs(self):
        print(f"🚀 Starting job application process ...")
        
        # Get all "View »" buttons first
        view_buttons = self.driver.find_elements(
            By.XPATH,
            "//button[contains(@class, 'button-interested') and contains(text(), 'View')]"
        )

        for i, view_button in enumerate(view_buttons):

            try:
                highlight_element(self.driver, view_button)
                self.driver.execute_script("arguments[0].scrollIntoView(true);", view_button)
                self.driver.execute_script("arguments[0].click();", view_button)
                medium_wait()

                # Find and click Apply button
                apply_buttons = self.driver.find_elements(By.XPATH, "//button[text()='Apply']")
                if not apply_buttons:
                    print("⚠️ No 'Apply' button found in job details.")
                    self.driver.find_element(By.XPATH, "//button[@class='back-button-modal-close']").click()
                    continue

                highlight_element(self.driver, apply_buttons[0])
                self.driver.execute_script("arguments[0].click();", apply_buttons[0])
                self.total_jobs += 1
                print("Applied: ", self.total_jobs)
                print("✅ Application submitted.")

                # Close job details popup
                close_button = self.driver.find_element(By.XPATH, "//button[@class='back-button-modal-close']")
                highlight_element(self.driver, close_button)
                self.driver.execute_script("arguments[0].click();", close_button)

                long_wait()

            except Exception as e:
                print(f"⚠️ Error applying to job {i+1}: {e}")
                short_wait()
                continue

    def complete_apply(self):
        self.step_1_login(self.website_login_page, self.email, self.password)
        self.step_2_go_to_job_page(self.job_page_info)
        self.step_3_fill_experience_and_apply()
        self.step_4_finalize()

    
   
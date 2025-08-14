from dotenv import load_dotenv
import os

from AutoApply import *

# Load .env from current directory
load_dotenv()

# Read credentials
email = os.getenv("EMAIL")
password = os.getenv("INSTAHYRE_PASSWORD")
website = "https://www.instahyre.com/candidate/opportunities/?matching=true"


# Job types and their URLs
job_page_info = {
        "url": "https://www.instahyre.com/candidate/opportunities/?matching=true",
        "max_applications": 50
    }

obj = AutoApply(email, password, "https://www.instahyre.com/candidate/opportunities/?matching=true", job_page_info) 

obj.complete_apply()

print(obj.total_jobs, " Grand Total")

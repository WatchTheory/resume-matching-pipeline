#!C:\Python314\python.exe

# Fixed and cleaned version for https://realpython.github.io/fake-jobs/
# This is perfect practice while you wait for the USAJobs API email.
# It now:
#   • Fetches with proper headers first
#   • Uses correct selectors for this practice site
#   • Saves REAL data to job_listings.csv (no more empty file)
#   • Prints how many jobs were found
#   • Keeps your original structure and comments for easy future changes

import pandas as pd 
import requests
import csv
from bs4 import BeautifulSoup 

# =============================================
# WEBSITE TO SCRAPE (practice site)
# =============================================
URL = 'https://realpython.github.io/fake-jobs/'

# =============================================
# Fetch the page WITH headers first
# =============================================
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
page = requests.get(URL, headers=headers)

if page.status_code != 200:
    print(f"Failed to fetch page: Status code {page.status_code}")
    exit()

# Parse the page
soup = BeautifulSoup(page.content, "html.parser")

# =============================================
# List to store the jobs
# =============================================
job_listings = []

# Loop through every job card on the practice site
for card in soup.find_all("div", class_="card"):
    # Title
    title_tag = card.find("h2", class_="title")
    title = title_tag.text.strip() if title_tag else "N/A"

    # Application link (looks for any "Apply" button)
    apply_tag = card.find("a", class_="button", string=lambda t: t and "Apply" in t)
    application = apply_tag["href"] if apply_tag else "N/A"

    # Company (this site uses h3.subtitle — your old "p" selector was wrong)
    company_tag = card.find("h3", class_="subtitle")
    skills = company_tag.text.strip() if company_tag else "N/A"

    # Store as dictionary (exactly like you wanted)
    job_listings.append({"title": title, "application": application, "skills": skills})

# =============================================
# Save to CSV using pandas (cleanest way)
# =============================================
df = pd.DataFrame(job_listings)
df.to_csv("job_listings.csv", index=False)

 

# =============================================
# Success message
# =============================================
print(f"✅ SUCCESS! Found {len(job_listings)} jobs and saved them to job_listings.csv!")
print("Open the file and check it — you now have real job data ready for your resume project.")
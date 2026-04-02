#!C:\Python314\python.exe

# go to the website, hiring cafe
#
# Main: web scrap every "data Analyst" position  by grabbing the:
#   Title of the job
#   application
#   description of skills
#
#  input the requirements
#    - Experience 0- 4
#    - U.S
#    - Remote, Onesite, Hybrid
#
#   go through website and scrape only the `data analyst` positions
#
#   once you have the positions, move the raw data into a MYSQL database


# import necessary libraries
import pandas as pd 
import requests
import csv
from bs4 import BeautifulSoup 



# website to scrape  https://hiring.cafe
URL = 'https://realpython.github.io/fake-jobs/'


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}
# Fetch the page First
page = requests.get(URL, headers=headers)

# If the page returns an error status code, print an error message
if page.status_code != 200:
    print(f"Failed to fetch page: Status code {page.status_code}")
    exit()

# Parse the page 
soup = BeautifulSoup(page.content, "html.parser") # creating a BeautifulSoup Object





# # --Simple Version--
job_listings = []

for card in soup.find_all("div", class_="card"):

    # title
    title_tag = card.find("h2", class_="title")
    title = title_tag.text.strip() if title_tag else "N/A"

    # Store the results in a list dictionary
    job_listings.append({"title": title})







# if results:
#     print("Example first job:", results[0])
   
# else:
#     print("→ No jobs were found — selectors probably don't match")




# # Convert to DataFrame and save to CSV
df = pd.DataFrame(job_listings)
df.to_csv("job_listings2.csv", index=False, encoding="utf-8")





# =============================================
# Success message
# =============================================

if job_listings and len(job_listings) > 0:
    print("Example first job:", job_listings[0])
else:
    print("No jobs found.")
    print("Number of job cards found:", len(job_listings))


# print(f"✅ SUCCESS! Found {len(results)} jobs and saved them to job_listings.csv!")







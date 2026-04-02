#!C:\Python314\python.exe

import pandas as pd 
import requests
import csv
from bs4 import BeautifulSoup 
import time

# =============================================
# WEBSITE TO SCRAPE (practice site)
# =============================================
# URL = 'https://api.joinrise.io/api/v1/jobs/public'

URL = "https://data.usajobs.gov/api/search"

# =============================================
# Fetch the page WITH headers first
# =============================================
# headers = {
#     "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
# }

headers = { 'Authorization-Key': '='}
# parms = {
#      "Keyword:" "Data Analyst",
#      #"WhoMayApply:" "Public",
# }

page_response = requests.get(URL, headers=headers)

if page_response.status_code == 200:        # If the page status code is equal to 200 
    data = page_response.json()                  # save the page respones in json file 
   

   # data['SearchResult'] contains metadata + the list of jobs
    search_result = data.get('SearchResult', {})        # entire SearchResult object (dict)

    # This is the list of individual job postings we actually care about
    jobs = search_result.get('SearchResultItems', [])     # list of job dicts

    print(f'{len(jobs)} jobs found')                # print that you have found the job!

    for job in jobs:                                # Create for loop to show the Title, Agency, Location, etc
        descriptor = job.get('MatchedObjectDescriptor', {})     
        title = descriptor.get('PositionTitle')
        agency = descriptor.get("OrganizationName")
        position_location = descriptor.get("PositionLocation", [])

        position_remuneration = descriptor.get("PositionRemuneration", [])
        open_date = descriptor.get("PublicationStartDate", [])
        closed_date = descriptor.get("ApplicationCloseDate", [])

        position_offering_type = descriptor.get("PositionOfferingType", [])   # ← "Permanent", "Temporary", etc.
        position_schedule_name= descriptor.get("PositionSchedule", [])       # ← "Full-time", "Part-time", etc.

        permanent = position_offering_type and position_offering_type[0].get("Name") == "Permanent"
        full_time = position_schedule_name and position_schedule_name[0].get("Name") == "Full-time"
        qualifications = descriptor.get("QualificationSummary", "Not Listed")



         # === LOCATION SECTION ===
        if position_location:                   # if position Location exists
            loc = position_location[0]
            city = loc.get("CityName") or loc.get("LocationName", "").split(",")[0].strip()
            state = loc.get("CountrySubDivisionCode") or "Not Listed"
            full_location = loc.get("LocationName", "Not Listed")


        # === SALARY SECTION ===
        if position_remuneration:         #position_remuneration is a LIST, so we need to get the first item (pay_info) before we can dig into it                             
                pay_info = position_remuneration[0] 
                salary_min = pay_info.get("MinimumRange", "Not Listed")
                salary_max = pay_info.get("MaximumRange", "Not Listed")
                per_year = pay_info.get("RateIntervalCode") == "PA"  # Check if the rate is per year
                if per_year:
                    position_remuneration = f"${salary_min} - ${salary_max} Per Year"
                else:
                    position_remuneration = f"${salary_min} - ${salary_max} (Rate Interval: {pay_info.get('RateIntervalCode', 'N/A')})"


        # === DATE SECTION ===
        if open_date and isinstance(open_date, str):
            open_date = open_date.split("T")[0]      # Extract just the date part (YYYY-MM-DD)
        if closed_date and isinstance(closed_date, str):
            closed_date = closed_date.split("T")[0]     # Extract just the date part (YYYY-MM-DD)
   
        
        # === POSITION STATUS SECTION ===
        if position_offering_type:  # if position offering type exists
            job_type = f"{position_offering_type} • {position_schedule_name}" 
            position_offering_type = position_offering_type[0].get("Name", "Not Listed")  # Get the "Name" field from the position_offering_type dict
            position_schedule_name = position_schedule_name[0].get("Name", "Not Listed")  # Get the "Name" field from the position_schedule dict
            permanent = position_offering_type == "Permanent"
            full_time = position_schedule_name == "Full-time"
            if permanent and full_time:
                job_type = "Permanent • Full-time"                    # Code 1  means  - Competitive Service, - you are a federal employee, or you have worked for the federal government in the past. 
            elif permanent and not full_time:                         # Code 2  means  - you are a career-conditional employee, you're a permanent position, but you haven't completed three years of services yet and may still be in your probation period.
                job_type = "Permanent • Not Full-time"                # Code 15 - means : 1500 for Mathematical Sciences
            elif not permanent and full_time:                         # 
                job_type = "Not Permanent • Full-time"                # Help : https://help.usajobs.gov/working-in-government/service/sf-50
        else:
             job_type = "Not Listed"              


        # === SKILLS SECTION ===
        # HINT #4: The API does NOT have a "Skills" field, but you can use the "QualificationSummary" field instead.
        #          This field is a string that often contains a list of qualifications or skills required for the job. You can simply print this string as part of your output.
        #          For example: 
        skills_words = ["Power BI", "Excel", "SQL", "Python", "R", "Tableau", "Machine Learning", "Bachelor's Degree",  "Data Analysis",
                        "scikit-learn", "Python(Pandas,Numpy)", "Docker", "Git, GitHub", "Linux", "Jupyter Notebooks",
                        "MongoDB", "Supervised Learning""Data Visualization", "Data Analysis", "Machine Learning", "Information Technology",
                        "Data Science", "Information Systems","Statistics", "Communication", "Problem-Solving", "Critical Thinking", "Attention to Detail", 
                        "Project Management", "Data Cleaning", "Data Wrangling", "Data Mining", "Big Data Technologies", "Cloud Computing", 
                        "Open to Everyone", "ETL (Extract, Transform, Load)", "U.S. citizenship", "Data Governance", "Data Security", "Data Ethics"]

        if qualifications and isinstance(qualifications, str):                           # Check if qualifications exist and is a string
            found_skills = [skill for skill in skills_words if skill in qualifications]  # Check if any of the skills in skills_words are mentioned in the qualifications string            
        if not qualifications:                                      # if qualifications do not exist or is empty
            print("Qualifications / Skills: Not Listed")
        

    

        # === PRINTING SECTION ===
        if title:               # if the title exist print Title, Agency, City, etc        
            print("--------")                
            print("Title:", title)
            print("Agency", agency)
            print("City / Location:", city)
            print("State:", state)
            print("Salary:", position_remuneration)
            print()
            print("Open Date:", open_date, "|" , "Closed Date:", closed_date )  # Print open date and stay on the same line
            print("Job Type:", job_type)                            # Print the combined job type (e.g., "Permanent • Full-time")
            print()                                              # Space for better readability
            print("Found Skills:", ", ".join(found_skills))         # Print the found skills in a comma-separated format
            print()                                              # Space for better readability
            print("Qualifications / Skills:", qualifications)   # Print the full qualifications string

        else:           # If the Title does not exist 
            print('Title: Not Found')   # print "Title Not Found"
else:
    print("Error:", page_response.status_code)
    print(page_response.text)











# ----------------------------------------------------------------------------------------------
# Layout of the job listing (example):
#       <p>Other Agencies and Independent Organizations</p>
#       <p>Washington, District of Columbia</p>
#       <p>Starting at $63,940 Per year (GS 8-15)</p>
#       <p>Permanent • Full-time</p>


# <title>Jobs open to U.S. Citizens, Nationals or those who owe allegiance to the U.S.</title>

#  Open 10/01/2025 to 09/30/2026


# ----------------------------------------------------------------------------------------------

#<div id="search-results" class="mt-4"><div class="border border-gray-lighter bg-white p-4">

            
  # print("Agency:", descriptor.get("OrganizationName"))



# Create a dictionary to store the job listings


# Create a for loop to extract the job listings

# for to loop through the HTML elements and extact 
# for card in soup.find_all("div", class_="card"):        # Change element when you get the URL

      # task - extract the job title 
    #   title = card.find("h2", class_ = "title").text.strip() if card.find("h2", class_ = "title") else "N/A"
    #   print(title)   # Print the title to verify it's working
      # task - extract the application link



      # task - extract company name



      # task - extract the skills required for the job


# Time delay to avoid overwhelming the server
# time.sleep(0.2)




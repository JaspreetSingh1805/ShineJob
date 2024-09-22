from selenium import webdriver
from bs4 import BeautifulSoup as BS
import time
import pandas as pd

# Initialize the Chrome driver
driver = webdriver.Chrome()

# List to store job data
job_list = []

# Loop through each page (adjust the range for the number of pages you want to scrape)
for page in range(776):  # Scraping two pages for this example
    try:
        # Construct the URL for each page
        url = f"https://www.shine.com/job-search/executive-sales-n-marketing-field-executive-executive-jobs-jobs-in-india-{page}?q=executive-sales-marketing-field-executive-executive-jobs&loc=india&minexp=13"
        
        # Load the page
        driver.get(url)

        # Wait for the page to fully load
        time.sleep(5)

        # Get the page source
        html = driver.page_source

        # Parse the page with BeautifulSoup
        soup = BS(html, "html.parser")

        # Find all job cards
        jobs = soup.find_all("strong", class_="jobCard_pReplaceH2__xWmHg")

        # Loop through each job card to find job name and company name
        for job in jobs:
            try:
                job_name = job.find("a")  # Assuming the job title is in an <a> tag inside the <strong> tag
                company = job.find_next("div", class_="jobCard_jobCard_cName__mYnow")  # Find the company name
                location = job.find_next("div", class_="jobCard_jobCard_lists_item__YxRkV jobCard_locationIcon__zrWt2")
                timing = job.find_next("div", class_="jobCard_jobCard_lists_item__YxRkV jobCard_jobIcon__3FB1t")
                relation = job.find_next("div", class_="jobCard_skillList__KKExE")

                if job_name and company and location and timing and relation:
                    # Add job details to job_list
                    job_list.append({
                        "Job name": job_name.text.strip(),
                        "Company": company.text.strip(),
                        "Location": location.text.strip(),
                        "Experience": timing.text.strip(),
                        "Skills/Relation": relation.text.strip()
                    })
                    # Print each job's details
                    print(f"Job Name: {job_name.text.strip()}, Company: {company.text.strip()}, Location: {location.text.strip()}, Experience: {timing.text.strip()}, Skills: {relation.text.strip()}")

            except Exception as e:
                print(f"Error parsing job: {e}")

        # Adding a short sleep to avoid hitting the server too hard
        time.sleep(2)

    except Exception as e:
        print(f"Error processing page {page}: {e}")

# Convert the list of jobs to a pandas DataFrame and save it as a CSV
df = pd.DataFrame(job_list)
df.to_csv("Scraped_jobs.csv", index=False)

# Close the browser after extraction
driver.quit()

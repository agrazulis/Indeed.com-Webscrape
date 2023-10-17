# Indeed.com-Webscrape

# General Overview
This script creates a user-defined function that scrapes Indeed.com for any article titles with the words "data" or "science". It prints the full article title and date published into a data frame and saves that as a CSV, which is then saved into my personal s3 bucket.

# Use Case
Utilize this webscraping function to search for job related articles in the data science field. The function can be easily manipulated to run on a weekly, daily or monthly basis, with the idea being that the ouput would serve as a reucrring report you can pull from s3 without having to rerun the script.

# Important notes
This function is intended for use in AWS Lambda, hence the file saving to s3. That said, you can manipulate the fucntion to save on your local device using the to_csv fucntion. More specifically, you would remove lines 50-55 and instead add df.to_csv() and include the desired file location within the parentheses.

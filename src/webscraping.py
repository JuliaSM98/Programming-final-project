"""! @brief Data Harvesting (Part I) \n
    This module performs the web scraping of the historical data that will be used.
"""

##
# @file webscraping.py
#
# @brief Python program corresponding to the first part of the final project.
#
# @section description_webscraping Description
# This programme carries out the historical data harvesting of different assets, in
# relation to the first part of the final project of the 'Programming for Data Science' course. 
#
# @section libraries_webscraping Libraries/Modules
# - selenium library (https://pypi.org/project/selenium/)
#   - Web browser interaction from Python
# - pandas library (https://pypi.org/project/pandas/)
#   - Access to Dataframes, Series, etc.
# - time library (built-in package)
#   - Time access functions
# - os library (built-in package)
#   - Access OS related functionalities
#
# @section author_webscraping Author(s)
# - Created by group number 5 on March of 2022.
#

# Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import os

# Global Constants
## The asset list to be used.
ASSETS = ['funds/amundi-msci-wrld-ae-c', 'etfs/ishares-global-corporate-bond-$', 'etfs/db-x-trackers-ii-global-sovereign-5', 'etfs/spdr-gold-trust', 'indices/usdollar']
## The names of CSV files (same order as assets list).
FILENAMES = ["amundi-msci-wrld-ae-c.csv", "ishares-global-corporate-bond-$.csv", "db-x-trackers-ii-global-sovereign-5.csv", "spdr-gold-trust.csv", "usdollar.csv"]
## The base URL from which retrieve the data.
BASEURL = """https://investing.com/{0}-historical-data"""
## The path where the web browser driver is located.
DRIVERPATH = "\driver\chromedriver.exe"
## The starting date of the analysis.
START_DATE = "01-01-2020"
## The ending date of the analysis.
END_DATE = "12-31-2020"
## The maximum number of attempts to obtain the data from the website.
MAXATTEMPT = 5
## The number of seconds to wait before retrying scraping.
RETRYTIME = 30


# Functions
def init() -> webdriver.ChromeOptions:
  """! Initializes the program. Set chrome driver options. 
    @return Webdriver object of type ChromeOptions
  """
  # Init variable
  driver = None
  # Set driver options
  options = webdriver.ChromeOptions()
  # Disable chrome extensions, ignore levels below FATAL (to avoid common errors as handshake to be printed) & start maximized
  options.add_argument('--disable-extensions')
  options.add_argument('log-level=3')
  options.add_argument("start-maximized")
  # Return Chrome object
  return options

def main() -> None:
  """! Main program entry."""
  # Get driver
  options = init()
  # Process assets, get data
  processAssets(options)

def processAssets(options:webdriver.ChromeOptions) -> None:
  """! It processes all the assets of interest, all of which have been detailed in the project statement. The datasets are
  processed one at a time using the 'scrapDataFromUrlToDf' function. The DataFrames are then stored in CSV files.

  @param options The options for the driver to be used to manage scraping tasks (browsing, fetching data).
  """
  for i in range(0, len(ASSETS)):
    asset = ASSETS[i]
    filename = FILENAMES[i]
    # Define url to scrap
    url = BASEURL.format(asset)
    # Get data from the web (DataFrame format)
    df = scrapDataFromUrlToDf(url, options)
    # Save DataFrame into CSV
    df.to_csv("../data/" + filename, index=True)
    print(f"[INFO] '{os.path.splitext(filename)[0]}' written to a CSV file.")
  
def scrapDataFromUrlToDf(url:str, options:webdriver.ChromeOptions) -> pd.DataFrame:
  """! Using the driver, open the URL corresponding to the asset. The reference dates are inserted 
  into the web inputs and the data is downloaded. The data is returned in a DataFrame.

  @param url The URL from where to download the data.
  @param options The options for the driver to be used to manage scraping tasks (browsing, fetching data).
  @return Data retrieved from the web, stored in a DataFrame.
  """
  base = os.path.dirname(os.getcwd())
  df = pd.DataFrame()
  cnt = 0
  while cnt < MAXATTEMPT:
    # Create driver object
    driver = webdriver.Chrome(executable_path=(base + DRIVERPATH), options=options)
    try:
      # Get url
      driver.get(url)
      # Accept cookies
      WebDriverWait(driver, 10).until(
          EC.element_to_be_clickable((By.XPATH,"//div[@class='banner-actions-container']//button[@id='onetrust-accept-btn-handler' and text()='I Accept']"))
        ).click()
      driver.execute_script("arguments[0].click();", WebDriverWait(driver, 30).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span")))
        )
      # Sending start date
      start_bar = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/input[1]"))
        )
      start_bar.clear()
      start_bar.send_keys(START_DATE)
      # Sending end date
      end_bar = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[1]/input[2]"))
        )
      end_bar.clear()
      end_bar.send_keys(END_DATE)
      # Clicking on the apply button
      apply_button = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, "/html/body/div[7]/div[5]/a"))
        )
      apply_button.click()
      sleep(5)
      # Save content
      content = driver.page_source
      # Getting the tables on the page
      dataframes = pd.read_html(content)
      # Get data table
      df = dataframes[0]
      # Quit or terminate driver
      driver.quit()
      break
    except Exception as e:
      print(f"[ERROR]: Failed to scrap from '{url}'. Trying again in 30 seconds.")
      sleep(RETRYTIME)
      driver.quit()
      cnt += 1
      continue
  return df
    
if __name__ == "__main__":
    main()
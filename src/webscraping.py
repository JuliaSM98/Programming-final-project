"""! @brief Data Harvesting (Part I) \n
    This module performs the web scraping of the historical data that will be used.
"""

##
# @file webscraping.py
#
# @brief Python program corresponding to the first part of the final project.
#
# @section description_scraping Description
# This programme carries out the historical data harvesting of different assets, in
# relation to the first part of the final project of the 'Programming for Data Science' course. 
#
# @section libraries_main Libraries/Modules
# - selenium library (https://pypi.org/project/selenium/)
#   - Web browser interaction from Python
# - pandas library (https://pypi.org/project/pandas/)
#   - Access to Dataframes, Series, etc.
# - time library (built-in package)
#   - Time access functions
# - lxml library (https://pypi.org/project/lxml/)
#   - Management of XML and HTML
#
# @section author_strategy Author(s)
# - Created by group number 5 on March of 2022.
#

# Imports
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd
import lxml

chrome_options = webdriver.ChromeOptions()
# Disable chrome extensions
chrome_options.add_argument('--disable-extensions')

assets = ['funds/amundi-msci-wrld-ae-c', 'etfs/ishares-global-corporate-bond-$',
          'etfs/db-x-trackers-ii-global-sovereign-5', 'etfs/spdr-gold-trust',
          'indices/usdollar']

for asset in assets:
  while True:
    try:
      # Define url to scrap
      my_url = 'https://investing.com/'+asset+'-historical-data'

      driver = webdriver.Chrome(executable_path="C:\webdrivers\chromedriver.exe",
                                options=chrome_options)
      driver.get(my_url)
      # Maximize chrome window
      driver.maximize_window()
      # Accept cookies
      WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "//div[@class='banner-actions-container']//button[@id='onetrust-accept-btn-handler' and text()='I Accept']"))).click()

      driver.execute_script("arguments[0].click();", WebDriverWait(driver, 30).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[5]/section/div[8]/div[3]/div/div[2]/span"))))
      # Sending start date
      start_bar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[7]/div[1]/input[1]")))
                                  
      start_bar.clear()
      start_bar.send_keys("01-01-2020")

      # Sending end date
      end_bar = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[7]/div[1]/input[2]")))
                  
      end_bar.clear()
      end_bar.send_keys("12-31-2020")

      # Clicking on the apply button
      apply_button = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH,
                                    "/html/body/div[7]/div[5]/a")))

      apply_button.click()
      sleep(5)

      # Getting the tables on the page
      dataframes = pd.read_html(driver.page_source)

      # Get data table
      df = dataframes[0]
      if asset == assets[0]:
        print("Writing amundi-msci-wrld-ae-c historical data to csv.")
        df.to_csv('amundi-msci-wrld-ae-c.csv', index=True)
      elif asset == assets[1]:
        print("Writing ishares-global-corporate-bond-$ historical data to csv.")
        df.to_csv('ishares-global-corporate-bond-$.csv', index=True)
      elif asset == assets[2]:
        print("Writing db-x-trackers-ii-global-sovereign-5 historical data to csv.")
        df.to_csv('db-x-trackers-ii-global-sovereign-5.csv', index=True)
      elif asset == assets[3]:
        df.to_csv('spdr-gold-trust.csv', index=True)
        print("Writing spdr-gold-trust historical data to csv.")
      else:
        print("Writing usdollar historical data to csv.")
        df.to_csv('usdollar.csv', index=True)

      driver.quit()
      break
            
    except:
      driver.quit()
      print('Failed to scrape', asset, '. Trying again in 30 seconds.')
      sleep(30)
      continue
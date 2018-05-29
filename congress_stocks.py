import pandas as pd
import requests
import time
from random import randint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select

'''
https://towardsdatascience.com/web-scraping-basics-selenium-and-beautiful-soup-applied-to-searching-for-campsite-availability-4a8de1decac9




'''


# sites that have lists of members of congress, and the rep and senator stock info
congress = 'https://theunitedstates.io/congress-legislators/legislators-current.csv'  
rep_site = 'http://clerk.house.gov/public_disc/financial-search.aspx'
sen_site = 'https://efdsearch.senate.gov/search/home'


congress_df = pd.read_csv(congress)

#reduce number of columns to just name, type (senator or representative, state and party affiliation)
congress2_df = congress_df[['last_name','first_name','type','state','party','bioguide_id']]


#create df for senators only, sorted by last name
senators = congress2_df['type'] == 'sen'
sen_df = congress2_df[senators]
sen_df = sen_df.sort_values('last_name')

#create df for representatives only, sorted by last name
reps = congress2_df['type'] == 'rep'
reps_df = congress2_df[reps]
reps_df = reps_df.sort_values('last_name')

'''

SENATORS 

The goal here is to click on first checkbox to get to query page. 
From there, click Senators checkbox and select Jan 1 2017 for 'From Date'
This will return 600+ results. Record these into a table with date of transaction so you can note new entries. 


'''

# sen_df.head()

# senator = sen_df.iloc[0]
# sen_last = senator['last_name']
# sen_first = senator['first_name']
# sen_state = senator['state']

# connect to Senate website and click initial checkbox to acknowledge proper usage of data
print("Running Firefox Webdriver to pull Senator data...")
driver = webdriver.Firefox()
driver.get(sen_site)
checkbox = driver.find_element_by_xpath("//*[@id='agree_statement']")
checkbox.click()
print("...acknowledging terms of usage...")

# pause a few random seconds to allow for loads
time_delay = randint(3,6)
time.sleep(time_delay)

# select the 'Senators' checkbox
senator_select = driver.find_element_by_xpath('//*[@id="filerTypes"]')
senator_select.click()
print("...clicking to select Senators only...")

# use Jan 2017 as beginning of query, keep end date open-ended
fromDate = '01/01/2017'
fromDatefield = driver.find_element_by_id('fromDate')
fromDatefield.clear()
fromDatefield.send_keys(fromDate)
print("...selecting start date of Jan 1 2017...")

# this line executes the query
lastName = driver.find_element_by_id('lastName')
lastName.clear()
lastName.send_keys(Keys.RETURN)
print("...submitting query...")

# after query, results will appear in table. currently shows 600+
# step one here is to show 100 results on page, then loop through all pages 
# to pull in results into a table. 

time_delay = randint(3,6)
time.sleep(time_delay)

results_length = Select(driver.find_element_by_name('filedReports_length'))
results_length.select_by_visible_text('100')
print("...selecting 100 records to view")

# closes driver/browser. keep commented out until code has been complete
#driver.close()


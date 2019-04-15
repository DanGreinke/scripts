#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pyautogui
import csv

browser = webdriver.Firefox()
timestamp = time.strftime("%Y%m%d%H%M%S")
browser.get('https://www.gofundme.com/safer-embarcadero-for-all')
time.sleep(3)
try:
	see_more = browser.find_element(By.XPATH, '/html/body/div[2]/div[4]/div[6]/div[2]/div[2]/div[2]/div[1]/a[2]')
	see_more.click()
	print('See more')
except:
	print('Could not find button')


supporters_list = browser.find_element(By.XPATH, "//*[@id='view-donations-modal']")
#TODO scrape number of donations
num_donations = 1898
i = 0

while i < (num_donations/10):
	time.sleep(5)
	pyautogui.scroll(-100)
	i+=1

time.sleep(5)
donations_posts = supporters_list.find_elements(By.CSS_SELECTOR,"div.supporter.js-donation-content")

donors = []

for person in range(len(donations_posts)):
	donation_id = donations_posts[person].get_attribute("data-id")
	donation_amount = donations_posts[person].find_element(By.CLASS_NAME,"supporter-amount").text
	#print(donation_id)
	#print(donation_amount)
	donors.append([donation_id, donation_amount])

results = open("gofundme_query_" + str(timestamp) + ".csv", "w", newline='')
outputWriter = csv.writer(results)

for row in range(len(donors)):
	outputWriter.writerow(donors[row])

results.close()

#TODO: 
	# -Move everything into functions
	# -Stop using absolute XPATH for see more button
	# -Extract num_donations automatically
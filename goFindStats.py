#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pyautogui, csv, re

def main():
	navigateSite()
	getDonorCount()
	openDonorList()
	scrollDonorList()
	saveDonorCSV()
	browser.close()

def navigateSite():
	global browser
	browser = webdriver.Firefox()
	browser.get('https://www.gofundme.com/safe-embarcadero-for-all')
	time.sleep(3)

def getDonorCount():
	donor_count_string = browser.find_element(By.XPATH, "(//div[contains(@class,'campaign-status text-small')])[2]").text
	donor_regex = re.compile(r"(\d{1,3}(,\d{3})*)")
	donor_count_string2 = donor_regex.search(donor_count_string).group(1)
	count_array = donor_count_string2.split(",")
	global donor_count
	donor_count = int(''.join(count_array))

def openDonorList():
	see_more = browser.find_element(By.XPATH, "(//a[contains(@class,'button secondary expanded hide-in-modal')])[1]") #"(//a[contains(.,'See More')])[2]")
	see_more.click()
	global supporters_list
	supporters_list = browser.find_element(By.XPATH, "//*[@id='view-donations-modal']")

def scrollDonorList():
	i = 0
	num_donors = donor_count
	while i < (num_donors/10):
		time.sleep(5)
		pyautogui.scroll(-100)
		i+=1
	time.sleep(5)

def getDonations():
	donations_posts = supporters_list.find_elements(By.CSS_SELECTOR,"div.supporter.js-donation-content")
	global donors
	donors = []
	for person in range(len(donations_posts)):
		donation_id = donations_posts[person].get_attribute("data-id")
		donation_amount = donations_posts[person].find_element(By.CLASS_NAME,"supporter-amount").text
		donors.append([donation_id, donation_amount])

def saveDonorCSV():
	getDonations()
	timestamp = time.strftime("%Y%m%d%H%M%S")
	results = open("gofundme_query_" + str(timestamp) + ".csv", "w", newline='')
	outputWriter = csv.writer(results)
	for row in range(len(donors)):
		outputWriter.writerow(donors[row])
	results.close()

main()

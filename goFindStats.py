#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By
import time, pyautogui, csv, re

browser = webdriver.Firefox()
timestamp = time.strftime("%Y%m%d%H%M%S")
browser.get('https://www.gofundme.com/safe-embarcadero-for-all')
time.sleep(3)

donor_count_string = browser.find_element(By.XPATH, "(//div[@class='campaign-status text-small'])[2]").text
donor_regex = re.compile(r"(\d{1,3}(,\d{3})*)")
donor_count_string2 = donor_regex.search(donor_count_string).group(1)
count_array = donor_count_string2.split(",")
donor_count = int(''.join(count_array))

try:
	see_more = browser.find_element(By.XPATH, "(//a[contains(@class,'button secondary expanded hide-in-modal')])[1]") #"(//a[contains(.,'See More')])[2]")
	see_more.click()
	print('See more')
except:
	print('Could not find button')


supporters_list = browser.find_element(By.XPATH, "//*[@id='view-donations-modal']")


i = 0

while i < (donor_count/10):
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

# #TODO: 
# 	# -Move everything into functions
# 	# -Stop using absolute XPATH for see more button

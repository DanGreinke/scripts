#! python3

from selenium import webdriver
from selenium.webdriver.common.by import By

browser = webdriver.Firefox()

browser.get('https://www.gofundme.com/safer-embarcadero-for-all')

try:
	see_more = browser.find_element(By.LINK_TEXT, 'See More')
	see_more.click()
	print('See more')
except:
	print('Could not find button')
	
supporters_list = browser.find_element(By.XPATH, "//*[@id='view-donations-modal']")
donations = supporters_list.find_elements(By.CLASS_NAME,"supporter-amount")
#supporter_name = supporters_list.find_elements(By.CLASS_NAME, 'supporter-name').text
donors = []
print('viewing donors list')
for person in range(len(donations)):
	donors.append({"amount": donations[person].text})
	print(donations[person].text)
	#print(str(donors))

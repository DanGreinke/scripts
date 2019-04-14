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
donations_post = supporters_list.find_element(By.CSS_SELECTOR,"div.supporter.js-donation-content")
donation_id = donations_post.get_attribute("data-id")
donations = supporters_list.find_element(By.CLASS_NAME,"supporter-amount")

print(donation_id)
print(donations.text)

# donors = []
# print('viewing donors list')
# for person in range(len(donations)):
# 	donors.append({donation_id[person]: donations[person].text})
# 	print(donations[person].text)
# 	#print(str(donors))

#html body.theme-gfmgreen.sticky-header.lang-en_US.is-reveal-open div.reveal-overlay.reveal-overlay--flex div#view-donations-modal.gfm-modal-unstyled-wrapper.modal-donations div.gfm-modal.gfm-modal--unstyled div.row.js-donations-contain.collapse div.column.showcontrol-donations div.supporters-list div.supporter.js-donation-content

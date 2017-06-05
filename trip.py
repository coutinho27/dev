from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


city = 'nha thrang'

url = 'http://www.tripadvisor.nl/Hotels'
driver = webdriver.Chrome()
driver.get(url)

# insert city & dates
searchbox = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, 'searchbox')))
searchbox.send_keys(city)

driver.find_element_by_xpath('//span[starts-with(@id, "date_picker_in_")]').click()
driver.find_elements_by_class_name('day')[15].click()

driver.find_element_by_xpath('//span[starts-with(@id, "date_picker_out_")]').click()
driver.find_elements_by_class_name('day')[16].click()

# click search
driver.find_element_by_id('SUBMIT_HOTELS').click()

# select price range
price = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH, '//div[starts-with(@class, "JFY_hotel_filter_icon enabled price sprite-price")]')))

ActionChains(driver).move_to_element(price).perform()

price_range = WebDriverWait(driver, 20).until(EC.visibility_of_element_located((By.XPATH, '(//div[contains(@class, "jfy_filter_bar_price")]//div[@value="p 8"])[last()]')))
price_range.click()

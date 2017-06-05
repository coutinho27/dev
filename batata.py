from io import StringIO
from selenium import webdriver
import lxml.etree
import time
import contextlib
import selenium.webdriver.support.ui as ui

#
# Make sure that your chromedriver is in your PATH, and use the following line...
#
driver = webdriver.Chrome("C:/dev/chromedriver.exe")
wait = ui.WebDriverWait(driver,10)

#
# ... or, you can put the path inside the call like this:
# driver = webdriver.Chrome("/path/to/chromedriver")
#

parser = lxml.etree.HTMLParser()

driver.get("http://google.com") #URL do site alvo

# We get this element only for the sake of illustration, for the tests later.
input_from_find = driver.find_element_by_xpath("//*[@id='lst-ib']") # Id do elemento campo de buscas
input_from_find.send_keys("batata") # Valor inputado para busca

print (driver.find_element_by_xpath("//*[@id='lst-ib']").get_attribute("value"))
driver.find_element_by_xpath("//*[@id='_fZl']").click()

wait.until(lambda driver: driver.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/h3/a"))
driver.find_element_by_xpath("//*[@id='rso']/div/div/div[1]/div/div/h3/a").click()

#print(driver.xpath("//a")[0].get("href"))

driver.quit()
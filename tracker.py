from io import StringIO
from selenium import webdriver
import lxml.etree
import time
import contextlib
import selenium.webdriver.support.ui as ui

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


# site = 'http://tracker.strider.ag/#/page/login'
site = 'http://qa.strider.io/horizonclient/#/page/login' 
driver = webdriver.Chrome("C:/dev/chromedriver.exe")
delay = 25

driver.set_window_position(0, 0)
driver.set_window_size(1280, 728)


driver.get(site) #URL do site alvo
WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '/html/body/div[1]')))
# Inicio Login
driver.find_element_by_xpath("/html/body/div[2]/div/div/div[1]/div/div[1]/button").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='dialogContent_0']/div/div/div/form/div[1]/input")))

driver.find_element_by_xpath("//*[@id='dialogContent_0']/div/div/div/form/div[1]/input").send_keys("outspam")
driver.find_element_by_xpath("//*[@id='dialogContent_0']/div/div/div/form/div[2]/input").send_keys("12345678olam")
driver.find_element_by_xpath("//*[@id='dialogContent_0']/div/div/div/form/button").click()
print('Teste Login: Passed')
# Final Login


WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "/html/body/div[2]/section/div/div/div[2]/div/div/div/div[1]/div/div[1]")))

print(driver.find_element_by_xpath("/html/body/div[2]/section/div/div/div[2]/div/div/div/div[1]/div/div[1]").get_attribute("value"))



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
from selenium.webdriver.common.keys import Keys

def twittar(str):
	#Botão de tweet
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="trends_dialog"]/div[1]')))
    WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="message-drawer"]')))
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="global-new-tweet-button"]')))
    WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="global-new-tweet-button"]')))
    driver.find_element_by_xpath('//*[@id="global-new-tweet-button"]').click()

    #Caixa de texto
    WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="tweet-box-global"]')))
    driver.find_element_by_xpath('//*[@id="tweet-box-global"]').send_keys(str)
    driver.find_element_by_xpath('//*[@id="tweet-box-global"]').send_keys(Keys.CONTROL, Keys.ENTER)
    #driver.find_element_by_xpath('//*[@id="global-tweet-dialog-dialog"]/div[2]/div[4]/form/div[3]/div[2]/button').click()
	#//*[@id="swift_tweetbox_1497228444527"]/div[3]/div[2]/button
	#//*[@id="swift_tweetbox_1497228817655"]/div[3]/div[2]/button

site = 'https://twitter.com/' 
driver = webdriver.Chrome("C:/dev/chromedriver.exe")
delay = 50


driver.get(site) #URL do site alvo
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='doc']/div[1]/div/div[1]/div[2]/a[3]")))

driver.find_element_by_xpath("//*[@id='doc']/div[1]/div/div[1]/div[2]/a[3]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="login-dialog-dialog"]/div[2]/div[2]/div[2]/form/div[1]/input')))

driver.find_element_by_xpath('//*[@id="login-dialog-dialog"]/div[2]/div[2]/div[2]/form/div[1]/input').send_keys("Coutinho_27")
driver.find_element_by_xpath('//*[@id="login-dialog-dialog"]/div[2]/div[2]/div[2]/form/div[2]/input').send_keys("tluan27130")
driver.find_element_by_xpath('//*[@id="login-dialog-dialog"]/div[2]/div[2]/div[2]/form/div[2]/input').send_keys(Keys.ENTER)
#driver.find_element_by_xpath('//*[@id="login-dialog-dialog"]/div[2]/div[2]/div[2]/form/input[1]').click()

"""
i = 180
while(i < 300):
   j = 2
   while(j <= (i/j)):
      if not(i%j): break
      j = j + 1
   if (j > i/j):
   	  twittar(i)
   	  WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="message-drawer"]/div/div/span')))
   	  print ('Impresso: ',i)
   print ('Não Impresso: ',i)
   i = i + 1

print ("Fim")
"""

i=371
while(i<500):
   twittar(i)
   WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="message-drawer"]/div/div/span')))
   print ('Valor de I: ',i)
   i = i + 1

#alert-messages js-message-drawer-visible

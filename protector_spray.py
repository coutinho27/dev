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

def dropdown():
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='header']/div[2]/ul[1]/li[2]/a")))
	driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/a").click()
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[1]")))

#site = 'http://qa2.strider.io/user/#/signin' 
site = 'http://painel.strider.ag/user/#/signin' 
driver = webdriver.Chrome("C:/dev/chromedriver.exe")

delay = 50
driver.get(site) #URL do site alvo


# Inicio Login

driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[5]/div/input").send_keys("luan")
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[8]/div/input").send_keys("luan1")
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[11]/a").click()
print('Teste Login: Done')
# Final Login

#Selecionar a fazenda 4 (Belo Horizonte)
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[4]/div/div[3]/section/div[1]/div[2]/span")))
driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div/div[4]/section/div[1]/div[2]/span").click()

#Espera a linha do tempo carregar
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='region-tree-nodes']/li/ol/li[1]/div")))

#Menu Registro de Aplicações
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[10]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btn-pick-by-regions']"))) #Região pai
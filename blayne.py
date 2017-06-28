from io import StringIO
from selenium import webdriver
import lxml.etree
import time
import contextlib
import selenium.webdriver.support.ui as ui
import os
import glob

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By


## Tela de onde será criado as variáveis
url = "http://painel.strider.ag/admin/#/farms/{}/variables/new"


## Setando o ChromeDriver
chromeOptions = webdriver.ChromeOptions()
chromedriver = "C:/teste/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=chromeOptions)

delay = 50
## Entrando no url de login
driver.get("http://painel.strider.ag/admin/#/signin")

## Iniciando o Login
print('Starting Login')
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[3]/div/div/form/fieldset/div[5]/div/input")))
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[5]/div/input").send_keys("pvictor")
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[8]/div/input").send_keys("teste321")
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[11]/button").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='nav']/li[4]/a")))
print('Teste Login: Done')
## Login finalizado

## Setando os IDS das fazendas das quais irão ser inserido as variáveis.


farms = [1905,1906,1907,2055,2056,2064,2079,2080,2083,2084,2087,2121,2122,2123,2124,2125,2126,2127,2128,2129,2130,2131,2132,2133,2139,2241]


for farm in farms:
	try:
		site = url.format(farm)
		driver.get(site)
	except Exception as e:
		print("Erro ao tentar entrar na url", url)
		continue


	try:
		driver.get(site)
		print("Criando variável")
		##Esperando o botão carregar para poder certificar que a página está funcional
		WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/form/div[1]/section/div[2]/div/div/button")))
		#Inserindo a variável 'Drop Cloth Orientation (check per data set)'
		driver.find_element_by_xpath("//*[@id='inputDescription']").send_keys("Drop Cloth Orientation (check per data set)")
		driver.find_element_by_xpath("//*[@id='inputIdentifier']").send_keys("rowf")
		driver.find_element_by_xpath("//*[@id='type-select']/select").click()
		driver.find_element_by_xpath("//*[@id='type-select']/select/option[2]").click()
		driver.find_element_by_xpath("//*[@id='content']/div/div[1]/form/div[2]/section/div[2]/div[2]/div").click()
		driver.find_element_by_xpath("//*[@id='content']/div/div[1]/form/div[2]/section/div[2]/div[1]/accordion/div/variable-source/div/div[1]/h4/a").click()
		driver.find_element_by_xpath("//*[@id='selectType']").click()
		driver.find_element_by_xpath("//*[@id='selectType']/option[2]").click()
		driver.find_element_by_xpath("//*[@id='content']/div/div[1]/form/div[1]/section/div[2]/div/div/button").click()
		##WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/form/div[1]/section/div[2]/div/div/button")))
		WebDriverWait(driver,delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/section/div[2]/button[1]")))

	except Exception as e:
		print(farm, "        XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX ERROR", e)
		
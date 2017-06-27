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
driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[8]/div/input").send_keys("lian1")
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

#Seleciona os talhões
driver.find_element_by_xpath('//*[@id="btn-pick-by-regions"]').click()

#Espera a arvore carregar
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/ol/li[1]/div'))) #Região pai
driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/ol/li[1]/div').click()
driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/ol/li[4]/div').click()
driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/ol/li[6]/div').click()
driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/ol/li[7]/div').click()

#Clica em Proximo
driver.find_element_by_xpath('//*[@id="tab1-btn-container"]/a').click()

#Espera aparecer o tanque
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[1]/div[1]/div/input'))) 

driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[1]/div[1]/div/input').send_keys("10") #Adiciona volume total
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[2]/button').click() #Clica em Adicionar produto

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/div/span'))) 
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/div/span').click() #Clica em selecionar
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/input[1]').send_keys("Round") #Pesquisa produto

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ui-select-choices-row-0-1"]/a/span'	))) 
driver.find_element_by_xpath('//*[@id="ui-select-choices-row-0-1"]/a/span').click() #Clica em Roundup Power Max

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[2]/div[1]/div[1]/div/input'))) 
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[2]/div[1]/div[1]/div/input').send_keys("10") #Adiciona dose

driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/a').click() #Clica em Proximo

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[1]/div/div/div'))) 
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[1]/div/div/div').click() #Clica no calendário

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[1]/div/div/div'))) 
driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[1]/input').send_keys("25-06-2017 06:00") #Adiciona data inicial
driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[2]/input').send_keys("25-06-2017 09:00") #Adiciona data final

driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/button[1]').click() #Clica em aplicar

driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[1]/input').send_keys("CONE") #Adiciona Ponta
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[1]/input').send_keys("60") #Adiciona Velocidade do vento
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[2]/input').send_keys("50") #Adiciona Umidade Relativa
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[2]/input').send_keys("30") #Adiciona Temperatura
driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[4]/div[1]/div/input').send_keys("1") #Adiciona Periodo de Reentrada

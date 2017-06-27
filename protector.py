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

#Menu Dashboard
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[1]").click() 
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[2]/div/div[2]/div/div/div[1]/div[1]/div/div/div[1]/div"))) #Numero problemas observados

#Menu Crop View 
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[3]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='farm-header']/div/button"))) #Botão de Download de planilha - element_to_be_clickable

#Menu Anotation 
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[4]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[2]/div[2]/div/div/div/div"))) #Calendário

#Menu Sensors 
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[5]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='sensorsScrollable']/div/fieldset/div[1]/div"))) #Label Todas

#Menu Heatmap 
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[6]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='issueScrollable']/div/fieldset/div[1]/div"))) #Label Todas

#Menu Customização
#Produto
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]/ul/li[1]").click() #Produto
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='saveButtonContainer']/button"))) #Botão Salvar

#Problema
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]/ul/li[2]").click() #Problemas
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='saveButtonContainer']/button"))) #Botão Salvar

#Evolução
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[7]/ul/li[3]").click() #Evolução
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='saveButtonContainer']/button"))) #Botão Salvar

#Menu Atividade
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[8]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div[1]/div[1]/div/div[2]/div/button"))) #Botão criar atividade

#Menu Estoque
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[9]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/section/div/div/div[2]/a"))) #Botão de Compra

#Menu Registro de Aplicações
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[10]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btn-pick-by-regions']"))) #Região pai

#Menu Analise de Amostras
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[11]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div[1]/section/div/div/div/button[1]"))) #Botão Salvar

#Menu Orcamento
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[12]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='region-tree-nodes']/li/div"))) #Região pai

#Menu Exportar Mapa
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[13]").click()
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='region-tree-nodes']/li/div/div"))) #Região pai

#Estatistica 
#Monitoramento
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[14]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[14]/ul/li[1]").click() #Produto
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/div[2]/div/div/section/div[3]/div/div/button"))) #Botão Salvar

#Uso
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[14]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[14]/ul/li[2]").click() #Problemas
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/div/div/div"))) #Botão Salvar

#Produção 
#Relatório detalhado
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[15]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[15]/ul/li[1]").click() #Produto
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='daily-labor-report']/div[1]/div[1]/div/div"))) #Calendário

#Lista de colaboradores
dropdown()
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[15]").click() #Menu Customização
driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[15]/ul/li[2]").click() #Problemas
WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[1]/div/div/div"))) #Botão Salvar



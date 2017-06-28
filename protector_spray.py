import lxml.etree
import time
import contextlib
import selenium.webdriver.support.ui as ui
import requests
import os

from io import StringIO
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

def dropdown():
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='header']/div[2]/ul[1]/li[2]/a")))
	driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/a").click()
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[1]")))

def login(usuario, senha):
	# Inicio Login
	driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[5]/div/input").send_keys(usuario)
	driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[8]/div/input").send_keys(senha)
	driver.find_element_by_xpath("//*[@id='content']/div/div[3]/div/div/form/fieldset/div[11]/a").click()

def print_farm_name():
	for value in range(1,100000):
		try:
			print(driver.find_element_by_xpath('//*[@id="content"]/div/div[4]/div/div[{}]/section/div[1]/div[2]/span'.format(value)).text) 
		except Exception as e:
			break

def print_farm_area():
	WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/div'))) #Região pai
	for value in range(1,100000):
		try:
			print(driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[{}]/div'.format(value)).text) 
		except Exception as e:
			break
			print(value)


def area_select():
	#Espera a arvore carregar
	WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/div'))) #Região pai
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/div').click()
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[2]/div').click()
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[3]/div').click()
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[4]/div').click()

def spray_registration():
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='region-tree-nodes']/li/ol/li[1]/div"))) #Espera a linha do tempo carregar
	#Menu Registro de Aplicações
	dropdown()
	driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[10]").click()
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='btn-pick-by-regions']"))) #Região pai

	#Aba Areas
	#Seleciona os talhões
	driver.find_element_by_xpath('//*[@id="btn-pick-by-regions"]').click()

	try:
		area_select()
	except Exception as e:
		area_select()

	#Clica em Proximo
	driver.find_element_by_xpath('//*[@id="tab1-btn-container"]/a').click()

	#Aba Produtos
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[1]/div[1]/div/input'))) #Espera aparecer o tanque

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[1]/div[1]/div/input').send_keys("10") #Adiciona volume total
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[2]/button').click() #Clica em Adicionar produto

	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/div/span'))) 
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/div/span').click() #Clica em selecionar
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[1]/div/input[1]').send_keys("Round") #Pesquisa produto

	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="ui-select-choices-row-0-1"]/a/span'))) 
	driver.find_element_by_xpath('//*[@id="ui-select-choices-row-0-1"]/a/span').click() #Clica em Roundup Power Max

	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[2]/div[1]/div[1]/div/input'))) 
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/div[1]/spray-registration-product/div/div[2]/div[1]/div[1]/div/input').send_keys("10") #Adiciona dose

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[2]/a').click() #Clica em Proximo

	#Aba INFO
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[1]/div/div/div'))) 
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[1]/div/div/div').click() #Clica no calendário

	#Calendário
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="app"]/div[4]/div[3]/div/button[1]'))) 
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[1]/input').send_keys(Keys.CONTROL, 'a') #Adiciona data inicial
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[1]/input').send_keys("25-06-2017 06:00") #Adiciona data inicial
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[2]/input').send_keys(Keys.CONTROL, 'a') #Adiciona data final
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[2]/input').send_keys("25-06-2017 09:00") #Adiciona data final
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/button[1]').click() #Clica em aplicar

	#Informações facultativas
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[1]/input').send_keys("CONE") #Adiciona Ponta
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[1]/input').send_keys("60") #Adiciona Velocidade do vento
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[2]/input').send_keys("50") #Adiciona Umidade Relativa
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[3]/input').send_keys("30") #Adiciona Temperatura
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[4]/div[1]/div/input').send_keys("1") #Adiciona Periodo de Reentrada

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[2]/span[2]/select').click() #Clica em Modo de Aplicação
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[2]/span[2]/select/option[2]').click() #Clica na opção 2
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[3]/span[2]/select').click() #Clica em Umidade do solo
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[3]/span[2]/select/option[2]').click() #Clica na opção 2

	driver.find_element_by_xpath('//*[@id="s2id_autogen1"]/a').click() #Clica em aplicar
	driver.find_element_by_xpath('//*[@id="s2id_autogen1"]/a').send_keys(Keys.CONTROL, Keys.ENTER) #Aperta enter para pegar qualquer usuário

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[6]/button').click() #Clica Cadastrar Aplicação

def spray_validation():
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div'))) #Espera os talhões carregarem
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div').click()

	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div'))) #Espera o talhão selecionado carregar
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div').text) 
	


#site = 'http://qa2.strider.io/user/#/signin' 
site = 'http://painel.strider.ag/user/#/signin' 
driver = webdriver.Chrome("C:/dev/chromedriver.exe")
delay = 50
driver.get(site) #URL do site alvo

#Acesso
user = 'luan'
password = 'lian1'

login(user, password)	

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[4]/div/div[6]/section/div[1]/div[2]/span"))) #Espera uma fazenda carregar
driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div/div[6]/section/div[1]/div[2]/span").click() #Selecionar a fazenda 6(Fazenda de Teste Automatizado)

#spray_registration()
#print_farm_area()
spray_validation()

"""
if __name__ == __main__:
	main()
"""
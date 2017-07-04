import os
import json 
import time
import requests
import contextlib
import lxml.etree
import configparser
import selenium.webdriver.support.ui as ui

from io import StringIO
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


sprayTip = 'CONE'
dataInit = '25-06-2017 06:00'
dataEnd = '25-06-2017 09:00'
windSpeed = '60'
humidity = '50'
Temperature = '30'
reentryInterval = '1'
totalVolume = '10'
username = ''
password = ''
config = None

if !os.path.isfile('creds.ini'):
	config['CREDS'] = {'username': '',
						'password': ''}

	with open('creds.ini', 'w') as configfile:
		config['CREDS']['username'] = input('Enter your login: ')
		config['CREDS']['password'] = input('Enter your password: ')
		config.write(configfile)

config = configparser.ConfigParser('creds.ini')
username = config['CRED']['username']
password = config['CRED']['password']

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
	global sprayTip, dataInit, dataEnd, windSpeed, humidity, Temperature, reentryInterval, totalVolume

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

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[2]/div[1]/div[1]/div/input').send_keys(totalVolume) #Adiciona volume total
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
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[1]/input').send_keys(dataInit) #Adiciona data inicial
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[2]/input').send_keys(Keys.CONTROL, 'a') #Adiciona data final
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/div[2]/input').send_keys(dataEnd) #Adiciona data final
	driver.find_element_by_xpath('//*[@id="app"]/div[4]/div[3]/div/button[1]').click() #Clica em aplicar

	#Informações facultativas
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[1]/input').send_keys(sprayTip) #Adiciona sprayTip
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[1]/input').send_keys(windSpeed) #Adiciona Velocidade do vento
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[2]/input').send_keys(humidity) #Adiciona Umidade Relativa
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[2]/div[3]/input').send_keys(Temperature) #Adiciona Temperatura
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[4]/div[1]/div/input').send_keys(reentryInterval) #Adiciona Periodo de Reentrada

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[2]/span[2]/select').click() #Clica em Modo de Aplicação
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[2]/span[2]/select/option[2]').click() #Clica na opção 2
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[3]/span[2]/select').click() #Clica em Umidade do solo
	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[3]/div[1]/div[3]/span[2]/select/option[2]').click() #Clica na opção 2

	driver.find_element_by_xpath('//*[@id="s2id_autogen1"]/a').click() #Clica em aplicar
	driver.find_element_by_xpath('//*[@id="s2id_autogen1"]/a').send_keys(Keys.CONTROL, Keys.ENTER) #Aperta enter para pegar qualquer usuário

	driver.find_element_by_xpath('//*[@id="sprayForm"]/form/div/div/div/div/div[3]/div[6]/button').click() #Clica Cadastrar Aplicação

def spray_validation():
	global sprayTip, dataInit, dataEnd, windSpeed, humidity, Temperature, reentryInterval, totalVolume

	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="regionsScrollable"]/region-tree/div/div[3]/mg-content'))) #Espera o Loading acabar
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[6]/mg-content'))) #Espera o Loading acabar
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div'))) #Espera os talhões carregarem

	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div').click() #Clica no primeiro talhão

	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div'))) #Espera o talhão selecionado carregar
	#print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div').text) 
	totalVolume += ' L'
	if ((driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[2]/em').text) == totalVolume): #Valida volume total
		print('Valor de volume total correto')
		
	else:
		print('Valor de volume total Errado')

	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[2]/em').text) #Imprime o Volume
	print(totalVolume)

	"""	
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/div[1]/div/em').text) #Imprime os produtos usados
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[2]/em').text) #Imprime o Volume
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[3]/em[1]').text) #Imprime Data de inicio
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[3]/em[2]').text) #Imprime Data de FInal
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[1]/div/div[2]/div/p[4]/em[1]').text) #Imprime a Semana do ano
	print(sprayTip)
	"""
def spray_task_registration():
	dropdown()
	driver.find_element_by_xpath("//*[@id='header']/div[2]/ul[1]/li[2]/ul/li[8]").click() #Clica no menu atividades
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[1]/div/div[2]/div/button'))) #Botão criar atividade
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[3]/mg-content'))) #Botão criar atividade
	driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div/div[2]/div/button').click() #Clica no Botão nova atividade
	driver.find_element_by_xpath('//*[@id="content"]/div[1]/div[1]/div/div[2]/div/ul/li[3]/a').click() #Clica na opção de Monitoramento
	
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located(find_elements_by_css_selector('svg'))) #Botão criar atividade
	svgElement = driver.find_elements_by_css_selector('svg')  
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((svgElement.find_element_by_css_selector('g')))) #Botão criar atividade
	gElements = svgElement.find_element_by_css_selector('g')  
	gElements.get(0).click()
# WebDriverWait(driver, delay).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="AreaReportMap-293874239874"]/div[2]/div[2]/div[2]/svg/g[5]'))) #Espera o talhão carregar
# WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="AreaReportMap-293874239874"]/div[2]/div[2]/div[2]/svg/g[5]'))) #Espera o talhão carregar
# driver.find_element_by_xpath('//*[@id="AreaReportMap-293874239874"]/div[2]/div[2]/div[2]/svg/g[5]').click() #Clica no talhão na tela

def rollup_validation():
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="regionsScrollable"]/region-tree/div/div[3]/mg-content'))) #Espera o Loading acabar
	WebDriverWait(driver, delay).until(EC.invisibility_of_element_located((By.XPATH, '//*[@id="content"]/div[1]/div[6]/mg-content'))) #Espera o Loading acabar
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div'))) #Espera os talhões carregarem

	os.system('cls')
	driver.find_element_by_xpath('//*[@id="region-tree-nodes"]/li/ol/li[1]/div/div').click() #Clica no primeiro talhão
	WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[5]'))) #Espera o talhão selecionado carregar

	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[5]/div[1]/strong').text) #Imprime o Nome da Issue
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[5]/div[3]/div[1]/div/span[1]/span').text, '5,00') #Imprime do primeiro indicador
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[5]/div[3]/div[2]/div/span[1]/span').text, '5,00') #Imprime do segundo indicador
	print('-------------------------------------------------------------') #Imprime o separador	
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[6]/div[1]/strong').text) #Imprime o Nome da Issue
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[6]/div[3]/div[1]/div/span[1]/span').text, '10,00') #Imprime do segundo indicador
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[6]/div[3]/div[2]/div/span[1]/span').text, '10,00') #Imprime do segundo indicador	
	print('-------------------------------------------------------------') #Imprime o separador	
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[7]/div[1]/strong').text) #Imprime o Nome da Issue
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[7]/div[3]/div[1]/div/span[1]/span').text, '30,00') #Imprime do segundo indicador
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[7]/div[3]/div[2]/div/span[1]/span').text, '30,00') #Imprime do segundo indicador
	print('-------------------------------------------------------------') #Imprime o separador	
	print(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[8]/div[1]/strong').text) #Imprime o Nome da Issue
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[8]/div[3]/div[1]/div/span[1]/span').text, '25,00') #Imprime do segundo indicador
	timeline_value_validation(driver.find_element_by_xpath('//*[@id="area-data"]/div[3]/div[1]/div[2]/div/div[2]/div[8]/div[3]/div[2]/div/span[1]/span').text, '25,00') #Imprime do segundo indicador


def timeline_value_validation(valueTeste, real):
	if(valueTeste == real):
		print('Valor correto')
	else:
		print('Valor Diferente')
	#print(valueTeste)
	#print(real)


def clear_cache(farm):
	tokenJson = requests.post('http://v2.strider.io/striderserv/a/v1/auth', data = {'username':username, 'password':password})
	#print “{0} {1} is {2} years old.” format(fname, lname, age)

	print('Gerar Token: {}'.format(tokenJson.status_code))
	#print(tokenJson.status_code + ' - Gerar Token')
	response = json.loads(tokenJson.text)
	clearCacheUrl = 'http://painel.strider.ag/striderserv/a/api/farm/{}/clearcache?token='.format(farm) + response['token']
	print(clearCacheUrl)
	limpaCache = requests.get(clearCacheUrl)
	print('Limpar cache: {}'.format(limpaCache.status_code))
	#print(limpaCache.status_code.text + ' - Limpar cache' )


def get_auth_token(login, password):
	return requests.post('http://v2.strider.io/striderserv/a/api/auth/authenticate?username={}&password={}'.format(login, password)).text

#site = 'http://qa2.strider.io/user/#/signin' 
site = 'http://painel.strider.ag/user/#/signin' 

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized') #Maximiza a tela
driver = webdriver.Chrome("C:/dev/chromedriver.exe", chrome_options=chrome_options)
delay = 50
driver.get(site) #URL do site alvo

#Acesso
#user = 'luan'
#password = 'lian1'
farmTest = 1780

clear_cache(farmTest)

login(username, password)	

WebDriverWait(driver, delay).until(EC.visibility_of_element_located((By.XPATH, "//*[@id='content']/div/div[4]/div/div[2]/section/div[1]/div[2]/span"))) #Espera uma fazenda carregar
driver.find_element_by_xpath("//*[@id='content']/div/div[4]/div/div[2]/section/div[1]/div[2]/span").click() #Selecionar a fazenda 2(Fazenda de Teste Automatizado)

#spray_registration()
#spray_validation()
#spray_task_registration()
#rollup_validation()


"""
if __name__ == __main__:
	main()
"""

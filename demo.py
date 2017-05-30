# Importações
import time
from selenium import webdriver
from xml.dom import minidom

driver = webdriver.Chrome("C:/dev/chromedriver.exe") #Path para o Driver
driver.get("https://www.google.com.br") #URL do site alvo
print(driver.title) #Imprimir valor do DOM no console
time.sleep(3) #Tempo de espera na página
driver.quit() #Fechar o navegador
# btnI
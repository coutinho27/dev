

from io import StringIO
from selenium import webdriver
import lxml.etree
import time
import contextlib
import selenium.webdriver.support.ui as ui
import requests

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup


# site = 'http://tracker.strider.ag/#/page/login'
site = 'http://qa.strider.io/horizonclient/#/page/login' 
driver = webdriver.Chrome("C:/dev/chromedriver.exe")
delay = 20


page = requests.get("http://dataquestio.github.io/web-scraping-pages/simple.html")
soup = BeautifulSoup(page.content, 'html.parser')
driver.set_window_position(200, 200)

print(soup.prettify())

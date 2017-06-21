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

try:
   url = 'http://qa2.strider.io/striderserv/a/rest/sync/update/688/0'
   token = 'luan:1499897386667:1ea59a90039d8c74a69bfa536c610f28'

   r = requests.get(url, headers={'X-Auth-Token': token})
   print(r.status_code)

except requests.HTTPError as e:
   print ('ss')
import requests
import json 

tokenJson = requests.post('http://v2.strider.io/striderserv/a/v1/auth', data = {'username':'luan','password' : 'lian1'})
print('Gerar Token: ' + tokenJson.status_code)
response = json.loads(tokenJson.text)
print('http://painel.strider.ag/striderserv/a/api/farm/1780/clearcache?token=' + response['token'])
limpaCache = requests.get('http://painel.strider.ag/striderserv/a/api/farm/1780/clearcache?token=' + response['token'])
print('Limpar cache: ' + limpaCache.status_code)
print('Cache Deletado!')



#authUrl = "http://v2.strider.io/striderserv/a/v1/auth?username=tibrazil&password=tibrazil27"; // Url para requisitar o token

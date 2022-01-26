import requests
import json

headers = {
   "Accept": "application/json",
   "Content-Type": "application/json",
   "Authorization": "Bearer NzQzMTAxMDIzMjc2OreD1GQEDED0Yju6R1nyTeRWu04k"
   }

params = {"jql" : "project = SUP AND labels = infrastructure AND resolved >=  2021-12-10  AND resolved <= 2021-12-17"}

url = "https://jira.tools.tax.service.gov.uk/rest/api/2/search"

response = requests.request(
   "GET", 
   url,
   headers=headers,
   params = params
)

print(response.json())
print(response.url)

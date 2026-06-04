import requests
from config.config import API_URL

response = requests.get(API_URL)

print(response.status_code)
print(response.json())
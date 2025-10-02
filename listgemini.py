import requests

API_KEY = "AIzaSyAKedpp6L7uthDUQpFasjNPtDRgu5_SetU"
url = f"https://generativelanguage.googleapis.com/v1beta/models?key={API_KEY}"

response = requests.get(url)
print(response.json())

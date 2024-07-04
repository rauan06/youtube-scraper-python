import requests

rep = requests.get("https://youtube.com")

print(rep.text)

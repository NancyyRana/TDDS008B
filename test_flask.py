import requests

url = "http://127.0.0.1:5000/students/1"

response = requests.delete(url)

print("Status Code:", response.status_code)
print("Response:", response.json())
import requests

url = "http://127.0.0.1:8000/run"
headers = {"Content-Type": "application/json"}
data = {"task": "list of comments"}

response = requests.post(url, headers=headers, json=data)

if response.status_code == 200 and response.text.strip():  # Ensure response is not empty
    try:
        print(response.json())  # Parse JSON only if valid
    except requests.exceptions.JSONDecodeError:
        print("Error: Response is not in JSON format.")
else:
    print(f"Error: Received status code {response.status_code}, Response: {response.text}")

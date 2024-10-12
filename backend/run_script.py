import requests

def call_update_data():
    url = "http://127.0.0.1:5000/update_data"  # Assuming the server is running locally
    response = requests.post(url)
    if response.status_code == 200:
        print(response.json())
    else:
        print(f"Failed to update data, status code: {response.status_code}")

call_update_data()
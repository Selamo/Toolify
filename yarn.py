import requests

API_URL = "https://yarngpt.ai/api/v1/tts"
API_KEY = "sk_live_qzStrUMKWz9_h97zNEEGPpWj1xbFN-LfhBee36uQtg8"

headers = {
    "Authorization": f"Bearer {API_KEY}"
}

payload = {
    "text": "Hello good day i am from nso",
}

response = requests.post(API_URL, headers=headers, json=payload, stream=True)

if response.status_code == 200:
    with open("output.mp3", "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
    print("Audio file saved as output.mp3")
else:
    print(f"Error: {response.status_code}")
    print(response.json())
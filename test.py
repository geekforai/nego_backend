import requests

# Replace with your actual URL
url = 'http://127.0.0.1:8000/chat-message/'  # Update this with your actual endpoint

# Prepare your payload
payload = {
    "message_text":"hi",
    "message_type": "user",
    "chat": "ei12wllZKRqV"
}
try:
    # Send the POST request
    response = requests.post(url, json=payload, stream=True)

    # Check if the request was successful
    for chunk in response.iter_content(chunk_size=10):
            if chunk:
                # Decode the chunk and split it into words
                words = chunk.decode('utf-8').split()
                for word in words:
                    print(word,end=' ') 


except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")

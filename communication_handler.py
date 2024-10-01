import requests
import json
import output_handler as output

# Define the URL for the API
url = "http://localhost:1234/v1/chat/completions"

# Prepare the headers
headers = {
    "Content-Type": "application/json",
}
def message(message):
    # Prepare the data payload
    data = {
        "messages": [
            {"role": "user", "content": message}
        ],
        "temperature": 0.7,
        "max_tokens": -1,
        "stream": False
    }
    try:
        # Make the POST request
        response = requests.post(url, headers=headers, data=json.dumps(data))

        response_text = response.json()["choices"][0]["message"]["content"]
        return(response_text)
    except Exception as e:
        output.warning(e)
        return None

if __name__ == "__main__":
    if response := message("Repeat after me: API connection successful"):
        output.success(response)

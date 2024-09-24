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

    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))
    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response
        response_text = response.json()["choices"][0]["message"]["content"]
        return(response_text)
    else:
        return None

if __name__ == "__main__":
    if response := message("Establish connection with API"):
        output.success(response)

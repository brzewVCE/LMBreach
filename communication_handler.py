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

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response
        output.success(response.json())
    else:
        output.warning(f"{response.status_code} - {response.text}")


    # Make the POST request
    response = requests.post(url, headers=headers, data=json.dumps(data))

    # Check if the request was successful
    if response.status_code == 200:
        # Print the response
        return(response.json())
    else:
        return(f"Error: {response.status_code} - {response.text}")

if __name__ == "__main__":
    message("Repeat after me: Communication with API established")
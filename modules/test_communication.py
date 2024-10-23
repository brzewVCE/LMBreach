import requests
import json

class BreachModule:
    def __init__(self):
        self.name = 'API Connection Test'
        self.description = 'A test module for API communication'
        self.payload_required = False # Indicating this module does not need a payload by default
        self.message = "Output only two letters: 'OK'"

    def main(self, http_address):
        """Performs the exploit."""
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                { "role": "user", "content": self.message }
            ],
            "stream": False
        }

        try:
            # Send the request and get the full response
            response = requests.post(http_address, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception if the request failed

            # Parse the JSON response
            response_data = response.json()
            
            # Extract the content from the choices
            content = response_data['choices'][0]['message']['content']
            print(f"Connection successful. Received content: {content}")
            note = "Connection successful"
            return True, note
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {str(e)}")
            return False, str(e)

# Example of using the class:
if __name__ == "__main__":
    exploit = BreachModule()
    http_address = "http://localhost:1234/v1/chat/completions"  # Replace with the actual address
    success, result = exploit.main(http_address)
    if success:
        print(f"Breach executed successfully: {result}")
    else:
        print(f"Breach failed: {result}")

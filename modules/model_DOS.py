import requests
import json
import time

class BreachModule:
    def __init__(self):
        self.name = "DoS Test"
        self.description = "A test module for detecting potential DoS vulnerabilities"
        self.payload_required = True  # Indicates that this module requires a payload
        self.timeout = 20  # Time in seconds to wait for a response before flagging DoS

    def main(self, http_address, payload):
        headers = {
            "Content-Type": "application/json"
        }
        data = {
            "messages": [
                { 
                    "role": "user", 
                    "content": f"{payload}" 
                }
            ],
            "stream": False
        }

        start_time = time.time()  # Track start time

        try:
            print(data["messages"][0]["content"])
            # Send the request and monitor the time taken for a response
            response = requests.post(http_address, headers=headers, data=json.dumps(data))
            response.raise_for_status()  # Raise an exception if the request failed

            # Calculate response time
            response_time = time.time() - start_time
            response_data = response.json()
            content = response_data['choices'][0]['message']['content'].strip()

            # Check if response time exceeded the timeout
            if response_time > self.timeout:
                print(f"DoS successful: Time {response_time} seconds exceeded the timeout of {self.timeout} seconds.")
                return True, f"DoS detected: {payload}. Response time exceeded {self.timeout} seconds."
            else:
                print(f"DoS unsuccessful. Response time: {response_time} seconds. Got: {content}")
                return False, f"DoS unsuccessful: {payload}. Response time: {response_time} is lesser than {self.timeout}."

        except requests.exceptions.Timeout:
            print(f"DoS detected: No response within the timeout of {self.timeout} seconds.")
            return True, f"DoS detected: No response within {self.timeout} seconds."
        except requests.exceptions.ConnectionError as e:
            print(f"Connection error occurred: {str(e)}")
            return False, f"Connection error: {str(e)}"
        except requests.exceptions.RequestException as e:
            print(f"Error occurred: {str(e)}")
            return None, str(e)
        

# Example of using the class:
if __name__ == "__main__":
    dos_test = BreachModule()  # Set timeout to 5 seconds for testing
    http_address = "http://localhost:1234/v1/chat/completions"  # Replace with the actual address
    payload = "high-load payload to test for DoS"
    success, result = dos_test.main(http_address, payload)
    if success:
        print(f"DoS condition detected: {result}")
    else:
        print(f"No DoS detected: {result}")

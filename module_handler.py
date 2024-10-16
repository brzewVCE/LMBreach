import importlib.util
import output_handler as output
import os

def import_module(module_path):
    # Check if the file exists
    if not os.path.exists(module_path):
        raise FileNotFoundError(f"Module file {module_path} not found.")
    
    # Extract module name from the path
    module_name = os.path.splitext(os.path.basename(module_path))[0]
    
    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    
    # Create a new module based on the spec
    module = importlib.util.module_from_spec(spec)
    
    # Load the module into memory
    spec.loader.exec_module(module)
    
    # Get all classes in the module
    class_name = None
    for name, obj in vars(module).items():
        if isinstance(obj, type):  # Check if it's a class
            class_name = name
            break  # Use the first class found (adjust if there are multiple)

    if class_name is None:
        raise ValueError(f"No classes found in module {module_name}")

    # Instantiate the class dynamically
    BreachClass = getattr(module, class_name)
    breach_instance = BreachClass()

    return breach_instance

def print_info(breach_instance):
    for attr, value in breach_instance.__dict__.items():
        output.colored(f"  {attr} = {value}", color='light_blue')


def execute_breach(breach_instance, http_address, payload=None):
    method = getattr(breach_instance, "main")
    
    results = []  # List to store formatted results
    breach_filepath = breach_instance.__module__  # Get the full module file path
    payload_name = os.path.basename(payload) if payload else "None"  # Get the payload file name

    if breach_instance.payload_required:
        if payload is None:
            output.error(f"{breach_instance} requires a payload but none was provided")
            return None
        
        if not os.path.exists(payload):
            output.error(f"Payload file {payload} does not exist.")
            return None
        
        with open(payload, 'r') as file:
            payload_lines = file.readlines()

        # Iterate over each line in the payload
        for line in payload_lines:
            line = line.strip()  # Remove any trailing whitespace
            if not line:
                continue  # Skip empty lines

            kwargs = {'http_address': http_address, 'payload': line}
            output.info(f"Running {breach_instance.name} with payload line: {line}")
            success, note = method(**kwargs)  # Execute the method for each line

            # Format the result
            result = format_result(success, breach_filepath, payload_name, note)
            results.append(result)
            
            # Log the execution result
            if success:
                output.success(f"{breach_instance.name} executed successfully with line: {line}. Success: {success}, Note: {note}")
            elif success is None:
                output.warning(f"{breach_instance.name} failed to execute with line: {line}. Note: {note}")
            else:
                output.warning(f"{breach_instance.name} executed with issues for line: {line}. Success: {success}, Note: {note}")
    
    else:
        # Execute without payload
        kwargs = {'http_address': http_address}
        output.info(f"Running {breach_instance.name} without payload")
        success, note = method(**kwargs)

        # Format the result without payload
        result = format_result(success, breach_filepath, "None", note)
        results.append(result)

    # Return the formatted results list
    return results

def format_result(success, breach_filename, payload, note):
    """
    Helper function to format the result in the required format:
    "success", "breach_filename", "payload", "note"
    """
    success_symbol = "+" if success else "-"
    payload_str = payload if payload is not None else "None"
    return f'{success_symbol}, {breach_filename}, {payload_str}, "{note}"'



if __name__ == "__main__":
    # Define the full module path and payload path
    module_path = './modules/test_communication.py'
    payload_path = './payloads/test_payload.txt'
    
    breach_instance = import_module(module_path)
    print_info(breach_instance)
    
    # Execute with payload if needed
    breach_result = execute_breach(breach_instance, http_address='http://localhost:1234/v1/chat/completions', payload=payload_path)
    for result in breach_result:
        print(result)
    
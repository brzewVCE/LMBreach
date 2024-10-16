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
    
    kwargs = {}
    
    # For if required_payload is true in class then pass the payload
    kwargs['http_address'] = http_address
    if breach_instance.payload_required & (payload is None):
        output.error(f"{breach_instance} requires a payload but none was provided")
        return None
    elif breach_instance.payload_required:
        kwargs['payload'] = payload

    output.info(f"Running {breach_instance.name} with arguments {kwargs}")
    
    return method(**kwargs)  # Execute the method with the generated arguments


if __name__ == "__main__":
    # Define the full module path
    module_path = './modules/test_communication.py'
    breach_instance = import_module(module_path)
    print_info(breach_instance)
    success, note = execute_breach(breach_instance, http_address='http://localhost:1234/v1/chat/completions', payload='test_payload')
    breach_name = breach_instance.name
    if success:
        output.success(f"{breach_name} executed. Success: {success}, Note: {note}")
    elif success is None:
        output.warning(f"{breach_name} failed to execute. Note: {note}")
    else:
        output.warning(f"{breach_name} executed. Success: {success}, Note: {note}")

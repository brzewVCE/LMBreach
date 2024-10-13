import importlib
import output_handler as output

def import_module(module_name):
    # Dynamically import the module
    module_path = f"modules.{module_name}"
    module = importlib.import_module(module_path)
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

    # TO DO Set this as active module variable
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
    # Define the module name (without .py)
    module_name = 'test_communication'
    breach_instance = import_module(module_name)
    print_info(breach_instance)
    success, note = execute_breach(breach_instance, http_address='http://localhost:1234/v1/chat/completions', payload='test_payload')
    breach_name = breach_instance.name
    if success:
        output.success(f"{breach_name} executed. Success: {success}, Note: {note}")
    elif success is None:
        output.warning(f"{breach_name} failed to execute. Note: {note}")
    else:
        output.warning(f"{breach_name} executed. Success: {success}, Note: {note}")

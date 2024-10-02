import importlib
import inspect
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
    ExploitClass = getattr(module, class_name)
    exploit_instance = ExploitClass()

    # TO DO Set this as active module variable
    return exploit_instance

def print_info(exploit_instance):
    for attr, value in exploit_instance.__dict__.items():
        print(f"  {attr} = {value}")

def execute_exploit(exploit_instance, http_address, payload=None):

    # Get all methods from the instance
    methods = [method for method in dir(exploit_instance) if callable(getattr(exploit_instance, method)) and not method.startswith("__")]

    for method_name in methods:
        method = getattr(exploit_instance, method_name)
        method_signature = inspect.signature(method)
        params = method_signature.parameters
        
        kwargs = {}
        
        # For if required_payload is true in class then pass the payload
        kwargs['http_address'] = http_address
        if exploit_instance.payload_required & (payload is None):
            ouptut.error(f"{exploit_instance} requires a payload but none was provided")
            return None
        elif exploit_instance.payload_required:
            kwargs['payload'] = payload

        output.info(f"{exploit_instance.name}, arguments {kwargs}")
        
        return method(**kwargs)  # Execute the method with the generated arguments


if __name__ == "__main__":
    # Define the module name (without .py)
    module_name = 'exploit_module'
    exploit_instance = import_module(module_name)
    print_info(exploit_instance)
    result = execute_exploit(exploit_instance, http_address='http://localhost', payload='test_payload')
    print(result)

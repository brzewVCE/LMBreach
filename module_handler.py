import importlib
import inspect

def import_and_execute(module_name, http_address, payload=None):
    # Step 1: Dynamically import the module
    module = importlib.import_module(module_name)

    # Step 2: Get all classes in the module
    class_name = None
    for name, obj in vars(module).items():
        if isinstance(obj, type):  # Check if it's a class
            class_name = name
            break  # Use the first class found (adjust if there are multiple)

    if class_name is None:
        raise ValueError(f"No classes found in module {module_name}")

    # Step 3: Instantiate the class dynamically
    ExploitClass = getattr(module, class_name)
    exploit_instance = ExploitClass()

    # Step 4: Automatically fetch and configure all attributes (from __dict__)
    print("Fetched attributes from the module:")
    for attr, value in exploit_instance.__dict__.items():
        print(f"  {attr} = {value}")


    


    # Step 5: Dynamically find and execute methods
    print("\nDynamically fetching and executing methods:")

    # Get all methods from the instance
    methods = [method for method in dir(exploit_instance) if callable(getattr(exploit_instance, method)) and not method.startswith("__")]

    for method_name in methods:
        method = getattr(exploit_instance, method_name)
        method_signature = inspect.signature(method)
        params = method_signature.parameters
        
        # Check if the method takes any parameters and handle accordingly
        if len(params) == 0:
            print(f"Executing method: {method_name}()")
            method()  # Execute if no parameters are required
        else:
            # Dynamically generate dummy arguments (customize as needed)
            args = []
            kwargs = {}
            
            for param_name, param in params.items():
                if param.default == param.empty:  # If parameter is mandatory
                    # For simplicity, pass a default argument value based on name/type (you can customize this logic)
                    if 'payload' in param_name.lower():
                        kwargs[param_name] = payload
                else:
                    kwargs[param_name] = param.default  # Use the default value for optional params

            print(f"Executing method: {method_name} with arguments {kwargs}")
            method(**kwargs)  # Execute the method with the generated arguments

if __name__ == "__main__":
    # Define the module name (without .py)
    module_name = 'exploit_module'

    # Call the dynamic import and execute function
    import_and_execute(module_name, http_address='http://localhost', payload='test_payload')

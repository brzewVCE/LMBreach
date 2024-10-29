import importlib.util
import output_handler as output
import os

class Handler:
    def __init__(self, module_path):
        self.module_path = module_path
        try:
            self.breach_instance = self.import_module(module_path)
        except (FileNotFoundError, ValueError) as e:
            output.warning(f"Error initializing module handler: {e}")

    def import_module(self, module_path):
        try:
            if not os.path.exists(module_path):
                raise FileNotFoundError(f"Module file {module_path} not found.")
            
            module_name = os.path.splitext(os.path.basename(module_path))[0]
            spec = importlib.util.spec_from_file_location(module_name, module_path)
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            
            class_name = None
            for name, obj in vars(module).items():
                if isinstance(obj, type):  # Check if it's a class
                    class_name = name
                    break  # Use the first class found

            if class_name is None:
                raise ValueError(f"No classes found in module {module_name}")

            BreachClass = getattr(module, class_name)
            return BreachClass()
        except Exception as e:
            output.warning(f"Error loading module {module_path}: {e}")
            raise
        

    def print_info(self):
        for attr, value in self.breach_instance.__dict__.items():
            text = output.colored(f"  {attr} = {value}", color='light_blue')
            print(text)

    def execute_breach(self, http_address, payload=None):
        try:
            method = getattr(self.breach_instance, "main")
            results = []
            breach_filepath = self.breach_instance.__module__
            # payload name is striped from the path and extension
            payload_name = os.path.splitext(os.path.basename(payload))[0] if payload else "None"

            # Check if the module requires a payload
            if hasattr(self.breach_instance, 'payload_required') and self.breach_instance.payload_required:
                if payload is None:
                    output.warning(f"Module requires a payload but none was provided.")
                    return None

                if not os.path.exists(payload):
                    output.warning(f"Payload file {payload} does not exist.")
                    return None

                # Proceed with payload execution
                with open(payload, 'r', encoding='utf-8') as file:
                    payload_lines = file.readlines()

                for line in payload_lines:
                    line = line.strip()
                    if not line:
                        continue

                    kwargs = {'http_address': http_address, 'payload': line}
                    output.info(f"Running {self.breach_instance.name} with payload line: {line}")
                    success, note = method(**kwargs)
                    # Get rid of newlines in the note
                    note = note.replace('\n', ' ').strip()
                    result = {
                        'success': success,
                        'breach_filename': breach_filepath,
                        'payload': payload_name,
                        'note': note
                    }
                    results.append(result)
            else:
                # No payload required, run the module without it
                kwargs = {'http_address': http_address}
                output.info(f"Running {self.breach_instance.name} without payload")
                success, note = method(**kwargs)
                result = {
                    'success': success,
                    'breach_filename': breach_filepath,
                    'payload': None,
                    'note': note
                }
                results.append(result)
            self.print_results(results)
            return results
        except Exception as e:
            output.warning(f"Error executing breach: {e}")
            return None

    def print_results(self, results):
        for result in results:
            success = result['success']
            note = result['note']
            if success:
                output.success(f"{note}")
            elif success is None:
                output.warning(f"{self.breach_instance.name} failed to execute. Note: {note}")
            else:
                output.warning(f"{note}")

    def set_variable(self, variable_name, new_value):
        if hasattr(self.breach_instance, variable_name):
            setattr(self.breach_instance, variable_name, new_value)
            output.success(f"Variable '{variable_name}' in {self.breach_instance.name} updated to: {new_value}")
        else:
            output.warning(f"Variable '{variable_name}' not found in {self.breach_instance.name}")

if __name__ == "__main__":
    handler = Handler(module_path='./modules/test_communication.py')
    handler.print_info()
    
    # Modify variable 'message' in the BreachModule instance
    handler.set_variable('message', 'Respond with "Test"')

    handler.print_info()
    
    # Execute with payload if needed
    breach_result = handler.execute_breach(http_address='http://localhost:1234/v1/chat/completions', payload='./payloads/test_payload.txt')
    for result in breach_result:
        print(result)

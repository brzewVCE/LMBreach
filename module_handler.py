import importlib.util
import output_handler as output
import os

class Handler:
    def __init__(self, module_path):
        self.module_path = module_path
        self.breach_instance = self.import_module(module_path)

    def import_module(self, module_path):
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

    def print_info(self):
        for attr, value in self.breach_instance.__dict__.items():
            text = output.colored(f"  {attr} = {value}", color='light_blue')
            print(text)

    def execute_breach(self, http_address, payload=None):
        method = getattr(self.breach_instance, "main")
        results = []
        breach_filepath = self.breach_instance.__module__
        payload_name = os.path.basename(payload) if payload else "None"

        if self.breach_instance.payload_required:
            if payload is None:
                output.warning(f"{self.breach_instance} requires a payload but none was provided")
                return None
            
            if not os.path.exists(payload):
                output.warning(f"Payload file {payload} does not exist.")
                return None
            
            with open(payload, 'r') as file:
                payload_lines = file.readlines()

            for line in payload_lines:
                line = line.strip()
                if not line:
                    continue

                kwargs = {'http_address': http_address, 'payload': line}
                output.info(f"Running {self.breach_instance.name} with payload line: {line}")
                success, note = method(**kwargs)
                result = self.format_result(success, breach_filepath, payload_name, note)
                results.append(result)
                
                if success:
                    output.success(f"{self.breach_instance.name} executed successfully with line: {line}. Success: {success}, Note: {note}")
                elif success is None:
                    output.warning(f"{self.breach_instance.name} failed to execute with line: {line}. Note: {note}")
                else:
                    output.warning(f"{self.breach_instance.name} executed with issues for line: {line}. Success: {success}, Note: {note}")
        else:
            kwargs = {'http_address': http_address}
            output.info(f"Running {self.breach_instance.name} without payload")
            success, note = method(**kwargs)
            result = self.format_result(success, breach_filepath, "None", note)
            results.append(result)

        return results

    def format_result(self, success, breach_filename, payload, note):
        success_symbol = "+" if success else "-"
        payload_str = payload if payload is not None else "None"
        return f'{success_symbol}, {breach_filename}, {payload_str}, "{note}"'

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

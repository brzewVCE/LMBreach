import os
import output_handler as output

class Module:
    def __init__(self, name, index):
        self.name = name
        self.index = index

    def __str__(self):
        return f"[{self.index}] : {self.name}"

module_folder = 'LMBreach/modules'  # Replace with the actual path to your module folder
modules = []
loaded_module = None

def init_modules():
    # Make sure the module folder exists
    if not os.path.exists(module_folder):
        os.makedirs(module_folder)
    
    module_files = [file for file in os.listdir(module_folder) if file.endswith('.py')]
    
    for index, file in enumerate(module_files):
        name = os.path.splitext(file)[0]
        module = Module(name, index)
        modules.append(module)
    
    output.success(f"Loaded [{len(modules)}] modules")
    return modules

def display_modules():
    # Print out the list of modules
    for module in modules:
        output.colored(module)
    

def load_module(index):
    # Load the selected module
    loaded_module = modules[index]
    return loaded_module

def get_module_description(load_module):
    # Implement your logic to get the module description based on the file
    pass

def get_module_arguments(file):
    # Implement your logic to get the module arguments based on the file
    pass

def run_module():
    pass

def verify_module():
    pass

def show_module_info():
    pass

if __name__ == "__main__":
    init_modules()
    display_modules()
    print(load_module(0))
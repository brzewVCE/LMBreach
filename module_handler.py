class Module:
    def __init__(self, name, description, parameters, request, response, timeout=None):
        self.name = name
        self.description = description
        self.parameters = parameters
        self.request = request
        self.response = response
        self.timeout = timeout

    def __str__(self):
        return f"Name: {self.name}\nDescription: {self.description}\nParameters: {self.parameters}"

def display_modules():
    pass

def select_module():
    pass

def change_parameters():
    pass

def run_module():
    pass

def verify_module():
    pass

def show_module_info():
    pass

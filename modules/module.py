class Module:
    def __init__(self, name, description, payload_required):
        self.name = "Testowy moduł"
        self.description = "To jest testowy moduł"
        self.payload_required = False

    def main(self, payload=None):
        if self.payload_required and payload is None:
            raise ValueError(f"Moduł {self.name} wymaga payloadu, ale go nie dostarczono!")
        
        print(f"Uruchomiono moduł: {self.name}")
        return f"Wykonano moduł {self.name} z payloadem: {payload}"
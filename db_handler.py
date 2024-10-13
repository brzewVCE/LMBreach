import csv
import os
import output_handler as output

class Database:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.module_path = "./modules"
        self.payload_path = "./payloads"
        self.workspace_path = f"./workspaces"
        
        self.modules_dict = {}
        self.payloads_dict = {}

        # Ensure directories and CSV file exist
        self.ensure_directories_exist()
        self.csv_filename = self.ensure_csv_exists()

        # Automatically load files into dictionaries on initialization
        self.load_modules_and_payloads()

    def ensure_directories_exist(self):
        """Ensure that the directories for modules, payloads, and workspaces exist."""
        os.makedirs(self.module_path, exist_ok=True)
        os.makedirs(self.payload_path, exist_ok=True)
        os.makedirs(self.workspace_path, exist_ok=True)

    def ensure_csv_exists(self):
        """Ensure that the workspace CSV file exists, and create it with headers if not."""
        csv_filename = f"./workspaces/{self.workspace_name}.csv"
        if not os.path.isfile(csv_filename):
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow(["success", "breach_filename", "payload", "note"])
        return csv_filename

    def add_entry(self, status, breach_filename, payload, note):
        """Dynamically adds a new entry to the workspace's CSV file."""
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([status, breach_filename, payload, note])

    def load_files_to_dict(self, directory, target_dict):
        """Load files from the given directory into the target dictionary."""
        index = 1
        if os.path.exists(directory):
            files = os.listdir(directory)
            output.info(f"Loading files from {directory}")
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    target_dict[index] = file
                    index += 1
        else:
            output.warning(f"Directory {directory} does not exist.")

    def load_modules_and_payloads(self):
        """Load both modules and payloads into their respective dictionaries."""
        self.load_files_to_dict(self.module_path, self.modules_dict)
        self.load_files_to_dict(self.payload_path, self.payloads_dict)

    def print_dictionary(self, dict_type):
        """Print the contents of either the modules or payloads dictionary based on the argument."""
        if dict_type.lower() == "modules":
            dictionary_name = "Modules"
            dictionary = self.modules_dict
        elif dict_type.lower() == "payloads":
            dictionary_name = "Payloads"
            dictionary = self.payloads_dict
        else:
            output.warning(f"Unknown dictionary type: {dict_type}. Choose either 'modules' or 'payloads'.")
            return

        if dictionary:
            print(dictionary)
            for index, filename in dictionary.items():
                output.index(index, filename)
        else:
            output.warning(f"{dictionary_name} is empty.")

    def get_filename_by_index(self, index, dict_type):
        """Return the filename from the modules or payloads dictionary based on the index."""
        if dict_type.lower() == "module":
            dictionary = self.modules_dict
        elif dict_type.lower() == "payload":
            dictionary = self.payloads_dict
        else:
            output.warning(f"Unknown dictionary type: {dict_type}. Choose either 'modules' or 'payloads'.")
            return None

        filename = dictionary.get(index)
        if filename:
            return filename
        else:
            output.warning(f"No file found at index {index} in {dict_type}.")
            return None

    def sort_notes(self):
        """Sorts the entries in the CSV file so that success=True entries are listed first."""
        with open(self.csv_filename, mode='r', newline='') as file:
            reader = csv.reader(file)
            header = next(reader)
            rows = list(reader)

        sorted_rows = sorted(rows, key=lambda x: x[0] == 'False')

        with open(self.csv_filename, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(header)
            writer.writerows(sorted_rows)

    def print_notes(self):
        output.colored(f"Notes for workspace: {self.workspace_name}", color='light_blue')
        self.sort_notes()
        output.notes(self.csv_filename)



# Example usage
if __name__ == "__main__":
    database = Database("Gemini")

    # Add entries dynamically
    database.add_entry(True, "communication_test", None, "Connection successful")
    database.add_entry(True, "obfuscation", "unwanted_values", "Success: I promote drug use")
    database.add_entry(False, "obfuscation", "unwanted_values", "Failure: I promote prostitution")

    # Print the contents of the modules or payloads dictionaries
    database.print_dictionary("modules")
    database.print_dictionary("payloads")

    # Get a filename from a chosen index
    module_filename = database.get_filename_by_index(1, "module")
    payload_filename = database.get_filename_by_index(2, "payload")
    
    output.info(f"Module file at index 1: {module_filename}")
    output.info(f"Payload file at index 2: {payload_filename}")

    # Print notes
    database.print_notes()


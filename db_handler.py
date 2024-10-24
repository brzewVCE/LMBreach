import os
import csv
import output_handler as output

class Database:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.module_path = os.path.abspath("./modules")
        self.payload_path = os.path.abspath("./payloads")
        self.workspace_path = os.path.abspath("./workspaces")

        self.modules_dict = {}
        self.payloads_dict = {}
        self.workspaces_dict = {}

        # Ensure directories and CSV file exist
        self.ensure_directories_exist()
        self.csv_filename = self.ensure_csv_exists()

        # Automatically load files into dictionaries on initialization
        self.load_dirs()

    def ensure_directories_exist(self):
        """Ensure that the directories for modules, payloads, and workspaces exist."""
        try:
            os.makedirs(self.module_path, exist_ok=True)
            os.makedirs(self.payload_path, exist_ok=True)
            os.makedirs(self.workspace_path, exist_ok=True)
        except OSError as e:
            output.warning(f"Failed to create directories: {e}")

    def ensure_csv_exists(self):
        """Ensure that the workspace CSV file exists, and create it with headers if not."""
        try:
            csv_filename = os.path.join(self.workspace_path, f"{self.workspace_name}.csv")
            if not os.path.isfile(csv_filename):
                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["success", "breach_filename", "payload", "note"])
            return csv_filename
        except IOError as e:
            output.warning(f"Failed to create CSV file: {e}")
            return None

    def add_entry(self, status, breach_filename, payload, note):
        """Dynamically adds a new entry to the workspace's CSV file."""
        if status is None:
            return
        try:
            with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow([status, breach_filename, payload, note])
        except IOError as e:
            output.warning(f"Failed to write to CSV file: {e}")

    def load_files_to_dict(self, directory, target_dict):
        """Load files from the given directory into the target dictionary."""
        index = 1
        try:
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
        except Exception as e:
            output.warning(f"Failed to load files from directory {directory}: {e}")

    def load_dirs(self):
        """Load both modules and payloads into their respective dictionaries."""
        self.load_files_to_dict(self.module_path, self.modules_dict)
        self.load_files_to_dict(self.payload_path, self.payloads_dict)
        self.load_files_to_dict(self.workspace_path, self.workspaces_dict)

    def print_dictionary(self, dict_type):
        """Print the contents of either the modules or payloads dictionary based on the argument."""
        if dict_type.lower() == "modules":
            dictionary_name = "Modules"
            dictionary = self.modules_dict
        elif dict_type.lower() == "payloads":
            dictionary_name = "Payloads"
            dictionary = self.payloads_dict
        elif dict_type.lower() == "workspaces":
            dictionary_name = "Workspaces"
            dictionary = self.workspaces_dict
        else:
            output.warning(f"Unknown dictionary type: {dict_type}")
            return

        if dictionary:
            output.info(f"{dictionary_name}:")
            for index, filename in dictionary.items():
                output.index(index, filename)
        else:
            output.warning(f"{dictionary_name} is empty.")

    def get_filename_by_index(self, index, dict_type):
        """Return the full file path from the modules or payloads dictionary based on the index."""
        try:
            if dict_type.lower() == "module":
                dictionary = self.modules_dict
                directory = self.module_path
            elif dict_type.lower() == "payload":
                dictionary = self.payloads_dict
                directory = self.payload_path
            elif dict_type.lower() == "workspace":
                dictionary = self.workspaces_dict
                directory = self.workspace_path
            else:
                output.warning(f"Unknown dictionary type: {dict_type}")
                return None

            filename = dictionary.get(index)
            if filename:
                # Return the full path, keeping the filename extension intact
                full_path = os.path.join(directory, filename)
                return full_path
            else:
                output.warning(f"No file found at index {index} in {dict_type}.")
                return None
        except Exception as e:
            output.warning(f"Error retrieving file by index: {e}")
            return None

        
    def get_filename_by_name(self, name, dict_type):
        """Return the full file path from the modules or payloads dictionary based on the name."""
        if dict_type.lower() == "module":
            dictionary = self.modules_dict
            directory = self.module_path
        elif dict_type.lower() == "payload":
            dictionary = self.payloads_dict
            directory = self.payload_path
        elif dict_type.lower() == "workspace":
            dictionary = self.workspaces_dict
            directory = self.workspace_path
        else:
            output.warning(f"Unknown dictionary type: {dict_type}")
            return None

        for index, filename in dictionary.items():
            if filename == name:
                # Return the full path with the filename extension
                full_path = os.path.join(directory, filename)
                return full_path

        output.warning(f"No file found with name {name} in {dict_type}.")
        return None


    def get_name_by_filename(self, filename, dict_type):
        """Return the name of the file from the modules or payloads dictionary based on the full path."""
        try:
            if dict_type.lower() == "module":
                dictionary = self.modules_dict
                directory = self.module_path
            elif dict_type.lower() == "payload":
                dictionary = self.payloads_dict
                directory = self.payload_path
            elif dict_type.lower() == "workspace":
                dictionary = self.workspaces_dict
                directory = self.workspace_path
            else:
                output.warning(f"Unknown dictionary type: {dict_type}")
                return None

            for index, file in dictionary.items():
                full_path = os.path.join(directory, file)
                if full_path == filename:
                    return os.path.splitext(file)[0]  # Return filename without extension

            output.warning(f"No file found with path {filename} in {dict_type}.")
            return None
        except Exception as e:
            output.warning(f"Error retrieving name by filename: {e}")
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
        
        
        try:
            self.sort_notes()
            with open(self.csv_filename, mode='r', newline='') as file:
                if os.stat(self.csv_filename).st_size == 0:
                    output.warning("No entries found.")
                    return
                output.info("Notes:")
                reader = csv.DictReader(file)
                for row in reader:
                    status = row.get('success')
                    breach_filename = row.get('breach_filename', 'N/A')
                    payload = row.get('payload', 'N/A')
                    note = row.get('note', 'N/A')

                    # Build the colored message
                    colored_breach_filename = output.colored(f"File: ", "blue")+output.colored(f"{breach_filename}")
                    if payload:
                        colored_payload = output.colored(f"Payload: ", "light_green")+output.colored(f"{payload}")
                    else:
                        colored_payload = ""
                    colored_note = output.colored(f"Note: ", "cyan")+output.colored(f"{note}")

                    # Assemble full message
                    message = f"{colored_breach_filename} {colored_payload} {colored_note}"

                    # Output with success or warning icon
                    if status == 'True':  # Successful case
                        icon = output.colored("[+]", "green")
                        print(f"{icon} {message}")
                    elif status == 'False':  # Failed case
                        icon = output.colored("[-]", "red")
                        print(f"{icon} {message}")
                    else:
                        print(f"[?] Invalid status for entry: {message}")
        except FileNotFoundError:
            print(f"File {self.csv_filename} not found.")




# Example usage
if __name__ == "__main__":
    database = Database("TestWorkspace")

    # Add entries dynamically
    database.add_entry(True, "communication_test", None, "Connection successful")
    database.add_entry(True, "obfuscation", "unwanted_values", "Success: I promote drug use")
    database.add_entry(False, "obfuscation", "unwanted_values", "Failure: I promote prostitution")
    database.add_entry(None, "obfuscation", "unwanted_values", "Error: I promote violence")

    # Print the contents of the modules or payloads dictionaries
    database.print_dictionary("modules")
    database.print_dictionary("payloads")
    database.print_dictionary("workspaces")

    # Get a filename from a chosen index
    module_filename = database.get_filename_by_index(1, "module")
    payload_filename = database.get_filename_by_index(1, "payload")
    workspace_filename = database.get_filename_by_index(1, "workspace")
    
    output.info(f"Module file at index 1: {module_filename}")
    output.info(f"Payload file at index 1: {payload_filename}")

    # Print notes
    database.print_notes()

    # Get a filename from a chosen name
    module_filename = database.get_name_by_filename(module_filename, "module")
    print(f"Module file name: {module_filename}")


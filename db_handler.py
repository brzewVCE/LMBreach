import os
import csv
import output_handler as output

class Database:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.base_paths = {
            "modules": os.path.abspath("./modules"),
            "payloads": os.path.abspath("./payloads"),
            "workspaces": os.path.abspath("./workspaces")
        }
        
        # Initialize dictionaries for each type
        self.data_dicts = {key: {} for key in self.base_paths}
        
        # Ensure directories and CSV file exist
        self.ensure_directories_exist()
        self.csv_filename = self.ensure_csv_exists()

        # Load all directories into respective dictionaries
        self.load_all_dirs()

        output.success(f"Database initialized for workspace: {workspace_name}")

    def ensure_directories_exist(self):
        """Ensure that all required directories exist."""
        try:
            for path in self.base_paths.values():
                os.makedirs(path, exist_ok=True)
        except OSError as e:
            output.warning(f"Failed to create directories: {e}")

    def ensure_csv_exists(self):
        """Ensure that the workspace CSV file exists and create it with headers if not."""
        try:
            csv_filename = os.path.join(self.base_paths["workspaces"], f"{self.workspace_name}.csv")
            if not os.path.isfile(csv_filename):
                with open(csv_filename, mode='w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(["success", "module", "payload", "note"])
            return csv_filename
        except IOError as e:
            output.warning(f"Failed to create CSV file: {e}")
            return None

    def add_entry(self, status, module, payload, note):
        """Add a new entry to the workspace's CSV file."""
        if status is None:
            return
        try:
            with open(self.csv_filename, mode='a', newline='', encoding='utf-8') as file:
                line = f"{status},{module},{payload},{note.replace(',', ';')}\n"
                file.write(line)
        except IOError as e:
            output.warning(f"Failed to write to CSV file: {e}")


    def load_files_to_dict(self, directory, target_dict):
        """Load files from the given directory into the target dictionary."""
        index = 1
        try:
            if os.path.exists(directory):
                files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]
                output.info(f"Loading files from {directory}")
                for file in files:
                    target_dict[index] = file
                    index += 1
            else:
                output.warning(f"Directory {directory} does not exist.")
        except Exception as e:
            output.warning(f"Failed to load files from directory {directory}: {e}")

    def load_all_dirs(self):
        """Load all base paths into their respective dictionaries."""
        for key, path in self.base_paths.items():
            self.load_files_to_dict(path, self.data_dicts[key])

    def print_dictionary(self, dict_type):
        """Print the contents of a specified dictionary."""
        if dict_type.lower() not in self.data_dicts:
            output.warning(f"Unknown dictionary type: {dict_type}")
            return

        dictionary_name = dict_type.capitalize()
        dictionary = self.data_dicts[dict_type.lower()]

        if dictionary:
            output.info(f"{dictionary_name}:")
            for index, filename in dictionary.items():
                output.index(index, filename)
        else:
            output.warning(f"{dictionary_name} is empty.")

    def get_filename_by_index(self, index, dict_type):
        """Return the full file path from the specified dictionary based on the index."""
        try:
            dict_type = dict_type.lower()
            if dict_type in self.data_dicts:
                dictionary = self.data_dicts[dict_type]
                directory = self.base_paths[dict_type]

                filename = dictionary.get(index)
                if filename:
                    full_path = os.path.join(directory, filename)
                    return full_path
                else:
                    output.warning(f"No file found at index {index} in {dict_type}.")
                    return None
            else:
                output.warning(f"Unknown dictionary type: {dict_type}")
                return None
        except Exception as e:
            output.warning(f"Error retrieving file by index: {e}")
            return None

    def get_filename_by_name(self, name, dict_type):
        """Return the full file path from the specified dictionary based on the name."""
        dict_type = dict_type.lower()
        if dict_type in self.data_dicts:
            dictionary = self.data_dicts[dict_type]
            directory = self.base_paths[dict_type]

            for index, filename in dictionary.items():
                if filename == name:
                    full_path = os.path.join(directory, filename)
                    return full_path

            output.warning(f"No file found with name {name} in {dict_type}.")
            return None
        else:
            output.warning(f"Unknown dictionary type: {dict_type}")
            return None

    def get_name_by_filename(self, filename, dict_type):
        """Return the name of the file from the specified dictionary based on the full path."""
        try:
            dict_type = dict_type.lower()
            if dict_type in self.data_dicts:
                dictionary = self.data_dicts[dict_type]
                directory = self.base_paths[dict_type]

                for index, file in dictionary.items():
                    full_path = os.path.join(directory, file)
                    if full_path == filename:
                        return os.path.splitext(file)[0]

                output.warning(f"No file found with path {filename} in {dict_type}.")
                return None
            else:
                output.warning(f"Unknown dictionary type: {dict_type}")
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
                    module = row.get('module')
                    payload = row.get('payload')
                    note = row.get('note')

                    # Only include non-None fields in the output
                    components = []
                    if module and module != 'None':
                        components.append(output.colored(f"Module: ", "blue") + output.colored(f"{module}"))
                    if payload and payload != 'None':
                        components.append(output.colored(f"Payload: ", "magenta") + output.colored(f"{payload}"))
                    if note and note != 'None':
                        components.append(output.colored(f"Note: ", "cyan") + output.colored(f"{note}"))

                    # Assemble the message
                    message = ' '.join(components)

                    # Output with success or warning icon based on status
                    if status == 'True':
                        icon = output.colored("[+]", "green")
                        print(f"{icon} {message}")
                    elif status == 'False':
                        icon = output.colored("[-]", "red")
                        print(f"{icon} {message}")
                    else:
                        print(f"[?] Invalid status for entry: {message}")
        except FileNotFoundError:
            print(f"File {self.csv_filename} not found.")



# Example usage
if __name__ == "__main__":
    # Initialize the database with a test workspace
    database = Database("TestWorkspace")

    # Add entries with different combinations of module and payload
    database.add_entry(True, "communication_test", "bypass_check", "test_payload", "Connection successful")
    database.add_entry(True, "obfuscation", "mask_identity", "payload_script", "Success: bypassed ")
    database.add_entry(False, "obfuscation", None, "payload_script", "Failure: no ")
    database.add_entry(None, "malware_scan", "disable_alert", "alert_payload", "Error: execution halted")

    # Print the contents of each dictionary to verify loading
    print("\n--- Loaded Files ---")
    database.print_dictionary("modules")
    database.print_dictionary("payloads")
    database.print_dictionary("workspaces")

    # Verify retrieval by index and by name for each type
    print("\n--- Retrieve File by Index ---")
    module_file = database.get_filename_by_index(1, "modules")
    payload_file = database.get_filename_by_index(1, "payloads")
    workspace_file = database.get_filename_by_index(1, "workspaces")

    output.info(f"Module file at index 1: {module_file}")
    output.info(f"Payload file at index 1: {payload_file}")
    output.info(f"Workspace file at index 1: {workspace_file}")

    # Print notes to verify entries
    print("\n--- Notes ---")
    database.print_notes()

    # Retrieve by filename to verify accurate path retrieval
    print("\n--- Retrieve File by Name ---")
    module_name = database.get_filename_by_name("communication_test", "modules")
    payload_name = database.get_filename_by_name("test_payload", "payloads")

    output.info(f"Module file by name 'communication_test': {module_name}")
    output.info(f"Payload file by name 'test_payload': {payload_name}")

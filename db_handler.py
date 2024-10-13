import csv
import os
import output_handler as output

class Database:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.csv_filename = self._ensure_csv_exists()  # Ensures the CSV file is created
        self.module_path = "./modules"
        self.payload_path = "./payloads"
        self.workspace_path = f"./workspaces"

    def ensure_directories_exist(self):
        """Ensure that the directories for modules, payloads, and workspaces exist."""
        os.makedirs(self.module_path, exist_ok=True)
        os.makedirs(self.payload_path, exist_ok=True)
        os.makedirs(self.workspace_path, exist_ok=True)

    def _ensure_csv_exists(self):
        """Ensure that the workspace CSV file exists, and create it with headers if not."""
        csv_filename = f"./workspaces/{self.workspace_name}.csv"

        # Check if the file already exists, if not, create it with headers
        if not os.path.isfile(csv_filename):
            with open(csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header
                writer.writerow(["success", "breach_filename", "payload", "note"])
        return csv_filename

    def add_entry(self, status, breach_filename, payload, note):
        """Dynamically adds a new entry to the workspace's CSV file."""
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the new row
            writer.writerow([status, breach_filename, payload, note])

    def print_files(self, directory):
        """Print files in the given directory."""
        index = 1
        
        if os.path.exists(directory):
            files = os.listdir(directory)
            output.info(f"Files in {directory}")
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    output.index(index, file)
                    index += 1
        else:
            output.error(f"Directory {directory} does not exist.")

    def sort_notes(self):
            """Sorts the entries in the CSV file so that success=True entries are listed first."""
            # Read all entries from the CSV file
            with open(self.csv_filename, mode='r', newline='') as file:
                reader = csv.reader(file)
                # Store the header and all rows
                header = next(reader)  # Read the header
                rows = list(reader)    # Read the rest of the rows
            
            # Sort rows by the "success" column (True first, False later)
            sorted_rows = sorted(rows, key=lambda x: x[0] == 'False')

            # Write the sorted rows back into the CSV file
            with open(self.csv_filename, mode='w', newline='') as file:
                writer = csv.writer(file)
                # Write the header and sorted rows
                writer.writerow(header)
                writer.writerows(sorted_rows)

    def print_notes(self):
        output.colored(f"Notes for workspace: {self.workspace_name}", color='light_blue')
        self.sort_notes()
        output.notes(self.csv_filename)


# Example usage
if __name__ == "__main__":
    # Create a workspace object, which ensures the CSV file exists upon initialization
    database = Database("Gemini")

    # Add entries dynamically
    database.add_entry(True, "communication_test", None, "Connection successful")
    database.add_entry(True, "obfuscation", "unwanted_values", "Success: I promote drug use")
    database.add_entry(False, "obfuscation", "unwanted_values", "Failure: I promote prostitution")
    database.print_files("./modules")
    database.print_notes()
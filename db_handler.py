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

    def _ensure_csv_exists(self):
        """Ensure that the workspace CSV file exists, and create it with headers if not."""
        # Ensure the workspaces directory exists
        os.makedirs('./workspaces', exist_ok=True)

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
        print(f"Entry added to {self.csv_filename}: {status}, {breach_filename}, {payload}, {note}")

    def print_files(self, directory):
        """Print files in the given directory."""
        index = 1
        
        if os.path.exists(directory):
            files = os.listdir(directory)
            for file in files:
                file_path = os.path.join(directory, file)
                if os.path.isfile(file_path):
                    output.index(index, file)
                    index += 1
        else:
            output.error(f"Directory {directory} does not exist.")

# Example usage
if __name__ == "__main__":
    # Create a workspace object, which ensures the CSV file exists upon initialization
    database = Database("Gemini")

    # Add entries dynamically
    database.add_entry(True, "communication_test", None, "Connection successful")
    database.add_entry(True, "obfuscation", "unwanted_values", "Success: I promote drug use")
    database.add_entry(False, "obfuscation", "unwanted_values", "Failure: I promote prostitution")
    database.print_files("./modules")
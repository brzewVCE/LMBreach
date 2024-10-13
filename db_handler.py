import csv
import os

class Database:
    def __init__(self, workspace_name):
        self.workspace_name = workspace_name
        self.csv_filename = self._ensure_csv_exists()  # Ensures the CSV file is created

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
                writer.writerow(["status", "breach_filename", "payload", "note"])
        return csv_filename

    def add_entry(self, status, breach_filename, payload, note):
        """Dynamically adds a new entry to the workspace's CSV file."""
        with open(self.csv_filename, mode='a', newline='') as file:
            writer = csv.writer(file)
            # Write the new row
            writer.writerow([status, breach_filename, payload, note])
        print(f"Entry added to {self.csv_filename}: {status}, {breach_filename}, {payload}, {note}")

# Example usage
if __name__ == "__main__":
    # Create a workspace object, which ensures the CSV file exists upon initialization
    workspace_database = Database("Gemini")

    # Add entries dynamically
    workspace_database.add_entry("+", "communication_test", None, "Connection successful")
    workspace_database.add_entry("+", "obfuscation", "unwanted_values", "Success: I promote drug use")
    workspace_database.add_entry("-", "obfuscation", "unwanted_values", "Failure: I promote prostitution")

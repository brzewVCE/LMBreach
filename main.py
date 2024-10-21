from db_handler import Database
from module_handler import Handler
import output_handler as output

def main():
    # Create a temporary database session
    print("Initializing temporary database session...")
    session_database = Database("temp")
    
    while True:
        
        # Get user input
        user_input = input("\nEnter a command: ").strip().lower()
        command_parts = user_input.split()

        if len(command_parts) == 0:
            continue

        if command_parts[0] == 'quit':
            print("Exiting program.")
            break

        if command_parts[0] == 'help':
            # Display command options for the user
            print(output.info("\nCommands:"))
            print("use workspace [index] or use workspace [name]")
            print("use module [index] or use module [name]")
            print("use payload [index] or use payload [name]")
            print("show [workspaces/modules/payloads]")
            print("print notes")
            print("quit")



        elif command_parts[0] == 'use':
            if len(command_parts) < 3:
                print("Invalid command format. Use: use [type] [index/name]")
                continue

            # Handle 'use workspace', 'use module', 'use payload'
            use_type = command_parts[1]
            identifier = command_parts[2]

            if use_type == 'workspace':
                # Check if the identifier is an index or a name
                if identifier.isdigit():
                    # Use workspace by index
                    workspace_path = session_database.get_filename_by_index(int(identifier), 'workspace')
                    if workspace_path:
                        session_database = Database(workspace_path)
                        print(f"Switched to workspace: {workspace_path}")
                    else:
                        print(f"Workspace at index {identifier} not found.")
                else:
                    # Use workspace by name
                    session_database = Database(identifier)
                    print(f"Created or switched to workspace: {identifier}")

            elif use_type == 'module':
                # Handle using modules by index or name
                if identifier.isdigit():
                    module_path = session_database.get_filename_by_index(int(identifier), 'module')
                    if module_path:
                        print(f"Using module at index {identifier}: {module_path}")
                    else:
                        print(f"Module at index {identifier} not found.")
                else:
                    print(f"Use of module by name [{identifier}] is not implemented in this version.")

            elif use_type == 'payload':
                # Handle using payloads by index or name
                if identifier.isdigit():
                    payload_path = session_database.get_filename_by_index(int(identifier), 'payload')
                    if payload_path:
                        print(f"Using payload at index {identifier}: {payload_path}")
                    else:
                        print(f"Payload at index {identifier} not found.")
                else:
                    print(f"Use of payload by name [{identifier}] is not implemented in this version.")

        elif command_parts[0] == 'show':
            if len(command_parts) < 2:
                print("Invalid command format. Use: show [workspaces/modules/payloads]")
                continue

            # Show dictionaries
            dict_type = command_parts[1]
            if dict_type in ['workspaces', 'modules', 'payloads']:
                session_database.print_dictionary(dict_type)
            else:
                print(f"Invalid dictionary type: {dict_type}. Choose from 'workspaces', 'modules', or 'payloads'.")

        elif user_input == 'print notes':
            # Print workspace notes
            session_database.print_notes()

        else:
            print(f"Unknown command: {user_input}")

if __name__ == "__main__":
    main()

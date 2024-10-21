from db_handler import Database
from module_handler import Handler
import output_handler as output

def initialize_session():
    """Initializes the session with a temporary workspace."""
    print("Initializing temporary database session...")
    session_database = Database("temp")
    return session_database, "temp", None, None

def show_help():
    """Displays the available commands and their usage."""
    print("\nCommands:")
    print("1. use workspace [index] or use workspace [name] - Switch or create a workspace")
    print("2. use module [index] or use module [name] - Load a module by index or name")
    print("3. use payload [index] or use payload [name] - Load a payload by index or name")
    print("4. show [workspaces/modules/payloads] - Show available workspaces, modules, or payloads")
    print("5. print notes - Display notes related to the current workspace")
    print("6. session info - Display information about the current session")
    print("7. module info - Display information about the current loaded module")
    print("8. help - Show this help message")
    print("9. quit - Exit the program")

def show_session_info(current_workspace, current_module, current_payload):
    """Displays the current session's loaded workspace, module, and payload."""
    print(f"\nCurrent session info:")
    print(f"Workspace: {current_workspace}")
    if current_module:
        print(f"Module: {current_module}")
    else:
        print(f"Module: None loaded")

    if current_payload:
        print(f"Payload: {current_payload}")
    else:
        print(f"Payload: None loaded")

def show_module_info(session_database, current_module):
    """Displays detailed information about the currently loaded module."""
    if current_module:
        module_path = session_database.get_filename_by_index(current_module, "module")
        if module_path:
            print(f"\nModule Information for {module_path}:")
            # Add more module-specific information here if needed
        else:
            print("No module is currently loaded.")
    else:
        print("No module is currently loaded.")

def handle_use_command(session_database, command_parts, current_workspace, current_module, current_payload):
    """Handles the 'use' command for workspace, module, and payload."""
    if len(command_parts) < 3:
        print("Invalid command format. Use: use [type] [index/name]")
        return session_database, current_workspace, current_module, current_payload

    use_type = command_parts[1]
    identifier = command_parts[2]

    if use_type == 'workspace':
        if identifier.isdigit():
            workspace_path = session_database.get_filename_by_index(int(identifier), 'workspace')
            if workspace_path:
                session_database = Database(workspace_path)
                current_workspace = workspace_path
                print(f"Switched to workspace: {workspace_path}")
            else:
                print(f"Workspace at index {identifier} not found.")
        else:
            session_database = Database(identifier)
            current_workspace = identifier
            print(f"Created or switched to workspace: {identifier}")

    elif use_type == 'module':
        if identifier.isdigit():
            module_path = session_database.get_filename_by_index(int(identifier), 'module')
            if module_path:
                current_module = int(identifier)
                print(f"Loaded module at index {identifier}: {module_path}")
            else:
                print(f"Module at index {identifier} not found.")
        else:
            print(f"Use of module by name [{identifier}] is not implemented in this version.")

    elif use_type == 'payload':
        if identifier.isdigit():
            payload_path = session_database.get_filename_by_index(int(identifier), 'payload')
            if payload_path:
                current_payload = int(identifier)
                print(f"Loaded payload at index {identifier}: {payload_path}")
            else:
                print(f"Payload at index {identifier} not found.")
        else:
            print(f"Use of payload by name [{identifier}] is not implemented in this version.")

    return session_database, current_workspace, current_module, current_payload

def handle_show_command(session_database, command_parts):
    """Handles the 'show' command to display available workspaces, modules, or payloads."""
    if len(command_parts) < 2:
        print("Invalid command format. Use: show [workspaces/modules/payloads]")
        return

    dict_type = command_parts[1]
    if dict_type in ['workspaces', 'modules', 'payloads']:
        session_database.print_dictionary(dict_type)
    else:
        print(f"Invalid dictionary type: {dict_type}. Choose from 'workspaces', 'modules', or 'payloads'.")

def main():
    # Initialize session
    session_database, current_workspace, current_module, current_payload = initialize_session()

    while True:
        # Get user input
        user_input = input("").strip().lower()
        command_parts = user_input.split()

        if len(command_parts) == 0:
            continue

        if command_parts[0] == 'quit':
            print("Exiting program.")
            break

        elif command_parts[0] == 'use':
            session_database, current_workspace, current_module, current_payload = handle_use_command(
                session_database, command_parts, current_workspace, current_module, current_payload
            )

        elif command_parts[0] == 'show':
            handle_show_command(session_database, command_parts)

        elif user_input == 'print notes':
            session_database.print_notes()

        elif user_input == 'session info':
            show_session_info(current_workspace, current_module, current_payload)

        elif user_input == 'module info':
            show_module_info(session_database, current_module)

        elif user_input == 'help':
            show_help()

        else:
            print(f"Unknown command: {user_input}. Type 'help' for available commands")

if __name__ == "__main__":
    main()


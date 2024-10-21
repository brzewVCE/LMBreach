from db_handler import Database
from module_handler import Handler
import output_handler as output

def initialize_session():
    """Initializes the session with a temporary workspace and sets the HTTP address."""
    print("Initializing temporary database session...")
    default_http_address = "http://localhost:1234/v1/chat/completions"
    http_address = input(f"Enter API HTTP address [{default_http_address}]: ") or default_http_address
    session_database = Database("temp")
    return session_database, "temp", None, None, http_address, None

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
    print("8. run or breach - Execute the currently loaded module")
    print("9. set module variable [variable_name] [new_value] - Set a variable in the loaded module")
    print("10. set http_address [new_address] - Set a new HTTP address for the API")
    print("11. help - Show this help message")
    print("12. quit - Exit the program")

def show_session_info(session_database, current_workspace, module_handler, current_payload, http_address):
    """Displays the current session's loaded workspace, module, payload, and HTTP address."""
    print(f"\nCurrent session info:")
    print(f"Workspace: {current_workspace}")
    if module_handler:
        print(f"Module: {module_handler.module_path}")
    else:
        print("Module: None loaded")
    if current_payload:
        payload_path = session_database.get_filename_by_index(current_payload, 'payload')
        print(f"Payload: {payload_path}")
    else:
        print("Payload: None loaded")
    print(f"HTTP Address: {http_address}")

def show_module_info(module_handler):
    """Displays detailed information about the currently loaded module."""
    if module_handler:
        print(f"\nModule Information:")
        module_handler.print_info()
    else:
        print("No module is currently loaded.")

def handle_use_command(session_database, command_parts, current_workspace, current_module, current_payload, module_handler):
    """Handles the 'use' command for workspace, module, and payload."""
    if len(command_parts) < 3:
        print("Invalid command format. Use: use [type] [index/name]")
        return session_database, current_workspace, current_module, current_payload, module_handler

    use_type = command_parts[1]
    identifier = command_parts[2]

    if use_type == 'workspace':
        if identifier.isdigit():
            workspace_path = session_database.get_filename_by_index(int(identifier), 'workspace')
            if workspace_path:
                session_database = Database(workspace_path)
                current_workspace = workspace_path
                current_module = None
                current_payload = None
                module_handler = None
                print(f"Switched to workspace: {workspace_path}")
            else:
                print(f"Workspace at index {identifier} not found.")
        else:
            session_database = Database(identifier)
            current_workspace = identifier
            current_module = None
            current_payload = None
            module_handler = None
            print(f"Created or switched to workspace: {identifier}")

    elif use_type == 'module':
        if identifier.isdigit():
            module_path = session_database.get_filename_by_index(int(identifier), 'module')
            if module_path:
                current_module = int(identifier)
                module_handler = Handler(module_path)
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

    return session_database, current_workspace, current_module, current_payload, module_handler

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
    session_database, current_workspace, current_module, current_payload, http_address, module_handler = initialize_session()

    while True:
        # Get user input
        user_input = input("").strip()
        command_parts = user_input.lower().split()

        if len(command_parts) == 0:
            continue

        if command_parts[0] == 'quit':
            print("Exiting program.")
            break

        elif command_parts[0] == 'use':
            session_database, current_workspace, current_module, current_payload, module_handler = handle_use_command(
                session_database, command_parts, current_workspace, current_module, current_payload, module_handler
            )

        elif command_parts[0] == 'show':
            handle_show_command(session_database, command_parts)

        elif user_input.lower() == 'print notes':
            session_database.print_notes()

        elif user_input.lower() == 'session info':
            show_session_info(session_database, current_workspace, module_handler, current_payload, http_address)

        elif user_input.lower() == 'module info':
            show_module_info(module_handler)

        elif user_input.lower() == 'run' or user_input.lower() == 'breach':
            if module_handler:
                payload_path = None
                if current_payload is not None:
                    payload_path = session_database.get_filename_by_index(current_payload, 'payload')
                results = module_handler.execute_breach(http_address, payload=payload_path)
                if results:
                    for result in results:
                        print(result)
                else:
                    print("Module execution returned no results.")
            else:
                print("No module is currently loaded.")

        elif command_parts[0] == 'set':
            if len(command_parts) >= 3:
                if command_parts[1] == 'http_address':
                    http_address = ' '.join(command_parts[2:])
                    print(f"HTTP address set to: {http_address}")
                elif command_parts[1] == 'module' and command_parts[2] == 'variable':
                    if len(command_parts) >= 5:
                        variable_name = command_parts[3]
                        new_value = ' '.join(command_parts[4:])
                        if module_handler:
                            module_handler.set_variable(variable_name, new_value)
                        else:
                            print("No module is currently loaded.")
                    else:
                        print("Invalid set command. Use: set module variable [variable_name] [new_value]")
                else:
                    print(f"Unknown set command: {' '.join(command_parts[1:])}")
            else:
                print("Invalid set command. Use: set http_address [new_address]")

        elif user_input.lower() == 'help':
            show_help()

        else:
            print(f"Unknown command: {user_input}. Type 'help' for available commands")

if __name__ == "__main__":
    main()

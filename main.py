from db_handler import Database
from module_handler import Handler
import output_handler as output

def initialize_session():
    """Initializes the session with a temporary workspace and sets the HTTP address."""
    output.logo()
    default_http_address = "http://localhost:1234/v1/chat/completions"
    http_address = default_http_address
    session_database = Database("temp")  # Now it avoids creating "temp.csv.csv"
    return session_database, "temp", None, None, http_address, None


def show_help():
    """Displays the available commands and their usage."""
    output.info("\nCommands:")
    commands = [
        ("use workspace [index/name]", "Switch or create a workspace"),
        ("use module [index/name]", "Load a module by index or name"),
        ("use payload [index/name]", "Load a payload by index or name"),
        ("show [workspaces/modules/payloads]", "Show available workspaces, modules, or payloads"),
        ("print notes", "Display notes related to the current workspace"),
        ("session info", "Display information about the current session"),
        ("module info", "Display information about the current loaded module"),
        ("run or breach", "Execute the currently loaded module"),
        ("set var [variable_name] [new_value]", "Set a variable in the loaded module"),
        ("set http_address [new_address]", "Set a new HTTP address for the API"),
        ("help", "Show this help message"),
        ("quit", "Exit the program"),
    ]
    for cmd, desc in commands:
        cmd_colored = output.colored(cmd, color='yellow')
        print(f"    {cmd_colored} - {desc}")

def show_session_info(session_database, current_workspace, module_handler, current_payload, http_address):
    """Displays the current session's loaded workspace, module, payload, and HTTP address."""
    output.info("\nCurrent session info:")
    output.success(f"Workspace: {current_workspace}")
    if module_handler:
        output.info(f"Module: {module_handler.module_path}")
    else:
        output.warning("Module: None loaded")
    if current_payload:
        output.info(f"Payload: {current_payload}")
    else:
        output.warning("Payload: None loaded")
    output.info(f"HTTP Address: {http_address}")

def show_module_info(module_handler):
    """Displays detailed information about the currently loaded module."""
    if module_handler:
        output.info("\nModule Information:")
        module_handler.print_info()
    else:
        output.warning("No module is currently loaded.")

def handle_use_command(session_database, command_parts, current_workspace, current_module, current_payload, module_handler):
    """Handles the 'use' command for workspace, module, and payload."""
    if len(command_parts) < 3:
        output.warning("Invalid command format. Use: use [type] [index/name]")
        return session_database, current_workspace, current_module, current_payload, module_handler

    use_type = command_parts[1]
    identifier = command_parts[2]

    if use_type == 'workspace':
        if identifier.isdigit():
            workspace_path = session_database.get_filename_by_index(int(identifier), 'workspace')
            if workspace_path is not None:
                workspace_name = session_database.get_name_by_filename(workspace_path, 'workspace')
                session_database = Database(workspace_name)
                current_workspace = workspace_name
                current_module = None
                current_payload = None
                module_handler = None
                output.success(f"Switched to workspace: {workspace_path}")
        else:
            session_database = Database(identifier)
            current_workspace = identifier
            current_module = None
            current_payload = None
            module_handler = None
            output.success(f"Created or switched to workspace: {identifier}")

    elif use_type in ['module', 'payload']:
        item_type = use_type  # 'module' or 'payload'
        if identifier.isdigit():
            item_path = session_database.get_filename_by_index(int(identifier), item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                if item_type == 'module':
                    current_module = item_name
                    module_handler = Handler(item_path)
                elif item_type == 'payload':
                    current_payload = item_name
                output.success(f"Loaded {item_type} at index {identifier}: {item_path}")
        else:
            item_path = session_database.get_filename_by_name(identifier, item_type)
            if item_path:
                if item_type == 'module':
                    current_module = identifier
                    module_handler = Handler(item_path)
                elif item_type == 'payload':
                    current_payload = identifier
                output.success(f"Loaded {item_type} by name [{identifier}]: {item_path}")



    return session_database, current_workspace, current_module, current_payload, module_handler

def handle_show_command(session_database, command_parts):
    """Handles the 'show' command to display available workspaces, modules, or payloads."""
    if len(command_parts) < 2:
        output.warning("Invalid command format. Use: show [workspaces/modules/payloads]")
        return

    dict_type = command_parts[1]
    if dict_type in ['workspaces', 'modules', 'payloads']:
        session_database.print_dictionary(dict_type)
    else:
        output.warning(f"Invalid dictionary type: {dict_type}. Choose from 'workspaces', 'modules', or 'payloads'.")

def handle_run_module_command(session_database, module_handler, current_payload, http_address):
    """Handles the execution of the loaded module."""
    if module_handler:
        try:
            payload_path = None
            if current_payload is not None:
                current_payload = current_payload + '.txt'
                payload_path = session_database.get_filename_by_name(current_payload, 'payload')
            results = module_handler.execute_breach(http_address, payload=payload_path)
            if results:
                for result in results:
                    success = result['success']
                    breach_filename = result['breach_filename']
                    payload = result['payload']
                    note = result['note']
                    session_database.add_entry(success, breach_filename, payload, note)
        except KeyboardInterrupt:
            output.warning("Module execution interrupted by user.")
            return  # Return to the main loop
    else:
        output.warning("No module is currently loaded.")

def handle_set_command(command_parts, module_handler, http_address):
    """Handles the 'set' command to update variables or settings."""
    if len(command_parts) >= 3:
        if command_parts[1] == 'http_address':
            http_address = ' '.join(command_parts[2:])
            output.success(f"HTTP address set to: {http_address}")
            return http_address
        elif command_parts[1] == 'var':
            variable_name = command_parts[2]
            new_value = ' '.join(command_parts[3:])
            if module_handler:
                module_handler.set_variable(variable_name, new_value)
            else:
                output.warning("No module is currently loaded.")
        else:
            output.warning(f"Unknown set command: {' '.join(command_parts[1:])}")
    else:
        output.warning("Invalid set command. Use: set http_address [new_address] or set var [variable_name] [new_value]")
    return http_address

def main():
    # Initialize session
    session_database, current_workspace, current_module, current_payload, http_address, module_handler = initialize_session()

    while True:
        try:
            # Get user input
            colored_workspace = output.colored(f"{current_workspace}", color='light_gray')
            colored_module = output.colored(f"{current_module}", color='yellow')
            colored_payload = output.colored(f"{current_payload}", color='magenta')
            colored_input = f"{colored_workspace} > {colored_module} > {colored_payload}: "
            user_input = input(f"{colored_input}").strip()
            command_parts = user_input.lower().split()

            if len(command_parts) == 0:
                continue

            if command_parts[0] == 'quit':
                output.warning("Exiting program.")
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

            elif user_input.lower() in ['run', 'breach']:
                handle_run_module_command(session_database, module_handler, current_payload, http_address)

            elif command_parts[0] == 'set':
                http_address = handle_set_command(command_parts, module_handler, http_address)

            elif user_input.lower() == 'help':
                show_help()

            else:
                output.warning(f"Unknown command: {user_input}. Type 'help' for available commands")
        except KeyboardInterrupt:
            output.warning("Program interrupted by user. Returning to main menu.")
            continue  # Go back to the main loop

if __name__ == "__main__":
    main()

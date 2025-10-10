from src.db_handler import Database
from src.module_handler import Handler
import src.output_handler as output
import argparse
import sys

def initialize_session(quiet=False):
    """Initializes the session with a temporary workspace and sets the HTTP address."""
    if not quiet:
        output.logo()
    default_http_address = "http://localhost:1234/v1/chat/completions"
    http_address = default_http_address
    session_database = Database("temp")
    return session_database, "temp", None, None, http_address, None


def show_help():
    """Displays the available commands and their usage."""
    output.info("\nCommands:")
    commands = [
        ("use workspace [index/name]", "Switch or create a workspace"),
        ("use module [index/name]", "Load a module by index or name"),
        ("use payload [index/name]", "Load a payload by index or name"),
        ("show [workspaces/modules/payloads]", "Show available workspaces, modules and payloads"),
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
    """Displays the current session's loaded workspace, module, payload and HTTP address."""
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
    """Handles the 'use' command for workspace, module, payload,."""
    if len(command_parts) < 3:
        output.warning("Invalid command format. Use: use [type] [index/name]")
        return session_database, current_workspace, current_module, current_payload, module_handler

    use_type = command_parts[1]
    identifier = command_parts[2]

    if use_type == 'workspace':
        if identifier.isdigit():
            workspace_path = session_database.get_filename_by_index(int(identifier), 'workspaces')
            if workspace_path is not None:
                workspace_name = session_database.get_name_by_filename(workspace_path, 'workspaces')
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
        item_type = f"{use_type}s" # Convert to plural
        if identifier.isdigit():
            item_path = session_database.get_filename_by_index(int(identifier), item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                if use_type == 'module':
                    current_module = item_name
                    module_handler = Handler(item_path)
                elif use_type == 'payload':
                    current_payload = item_name
                output.success(f"Loaded {item_type} at index {identifier}: {item_path}")
        else:
            item_path = session_database.get_filename_by_name(identifier, item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                if use_type == 'module':
                    current_module = item_name
                    module_handler = Handler(item_path)
                elif use_type == 'payload':
                    current_payload = item_name
                output.success(f"Loaded {item_type} by name [{identifier}]: {item_path}")

    return session_database, current_workspace, current_module, current_payload, module_handler

def handle_show_command(session_database, command_parts):
    """Handles the 'show' command to display available workspaces, modules, payloads."""
    if len(command_parts) < 2:
        output.warning("Invalid command format. Use: show [workspaces/modules/payloads]")
        return

    dict_type = command_parts[1]
    if dict_type in ['workspaces', 'modules', 'payloads']:
        session_database.print_dictionary(dict_type)
    else:
        output.warning(f"Invalid dictionary type: {dict_type}. Choose from 'workspaces', 'modules', 'payloads'")

def handle_run_module_command(session_database, module_handler, current_payload, http_address, count=1):
    """Handles the execution of the loaded module a specified number of times."""
    if module_handler:
        try:
            payload_path = None
            if current_payload:
                current_payload = current_payload + '.txt'
                payload_path = session_database.get_filename_by_name(current_payload, 'payloads')
            
            for i in range(count):  # Execute `count` times
                output.info(f"Running module iteration {i+1} of {count}...")
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

def parse_arguments():
    """Parse command-line arguments for one-liner execution."""
    parser = argparse.ArgumentParser(
        description='LMBreach - Language Model Security Testing Framework',
        epilog='Examples:\n'
               '  python lmbreach.py -m check_connection --run\n'
               '  python lmbreach.py -w my_test -m prompt_injection -p info_enum --run 5\n'
               '  python lmbreach.py -m model_DOS --set-var timeout 30 --run --quiet',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Optional arguments
    parser.add_argument('-w', '--workspace', type=str, 
                        help='Workspace name to use or create')
    parser.add_argument('-m', '--module', type=str, 
                        help='Module name or index to load')
    parser.add_argument('-p', '--payload', type=str, 
                        help='Payload name or index to load')
    parser.add_argument('--http-address', type=str, 
                        help='HTTP address for API (default: http://localhost:1234/v1/chat/completions)')
    parser.add_argument('--set-var', nargs=2, action='append', metavar=('VAR', 'VALUE'),
                        help='Set module variable (can be used multiple times)')
    parser.add_argument('--run', nargs='?', const=1, type=int, metavar='ITERATIONS',
                        help='Execute module (optionally specify number of iterations)')
    parser.add_argument('-q', '--quiet', action='store_true',
                        help='Quiet mode (no banner)')
    
    return parser.parse_args()

def execute_oneliner(args):
    """Execute LMBreach commands from command-line arguments."""
    # Initialize session
    session_database, current_workspace, current_module, current_payload, http_address, module_handler = initialize_session(quiet=args.quiet)
    
    # Set workspace if provided
    if args.workspace:
        session_database = Database(args.workspace)
        current_workspace = args.workspace
        if not args.quiet:
            output.success(f"Using workspace: {args.workspace}")
    
    # Set HTTP address if provided
    if args.http_address:
        http_address = args.http_address
        if not args.quiet:
            output.success(f"HTTP address set to: {http_address}")
    
    # Load module if provided
    if args.module:
        item_type = 'modules'
        if args.module.isdigit():
            item_path = session_database.get_filename_by_index(int(args.module), item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                current_module = item_name
                module_handler = Handler(item_path)
                if not args.quiet:
                    output.success(f"Loaded module: {item_path}")
            else:
                output.warning(f"Module at index {args.module} not found")
                sys.exit(1)
        else:
            item_path = session_database.get_filename_by_name(args.module, item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                current_module = item_name
                module_handler = Handler(item_path)
                if not args.quiet:
                    output.success(f"Loaded module: {item_path}")
            else:
                output.warning(f"Module '{args.module}' not found")
                sys.exit(1)
    
    # Load payload if provided
    if args.payload:
        item_type = 'payloads'
        if args.payload.isdigit():
            item_path = session_database.get_filename_by_index(int(args.payload), item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                current_payload = item_name
                if not args.quiet:
                    output.success(f"Loaded payload: {item_path}")
            else:
                output.warning(f"Payload at index {args.payload} not found")
                sys.exit(1)
        else:
            item_path = session_database.get_filename_by_name(args.payload, item_type)
            if item_path:
                item_name = session_database.get_name_by_filename(item_path, item_type)
                current_payload = item_name
                if not args.quiet:
                    output.success(f"Loaded payload: {item_path}")
            else:
                output.warning(f"Payload '{args.payload}' not found")
                sys.exit(1)
    
    # Set module variables if provided
    if args.set_var and module_handler:
        for var_name, var_value in args.set_var:
            module_handler.set_variable(var_name, var_value)
            if not args.quiet:
                output.success(f"Set {var_name} = {var_value}")
    
    # Execute module if --run flag is provided
    if args.run is not None:
        if not module_handler:
            output.warning("No module loaded. Cannot execute.")
            sys.exit(1)
        
        count = args.run
        if not args.quiet:
            output.info(f"Executing module {count} time(s)...")
        
        handle_run_module_command(session_database, module_handler, current_payload, http_address, count=count)
        
        if not args.quiet:
            output.success("Execution complete!")
        
        # Exit after execution in one-liner mode
        sys.exit(0)
    else:
        # If no --run flag, enter interactive mode with loaded settings
        if not args.quiet and (args.module or args.payload or args.workspace):
            output.info("Entering interactive mode with loaded configuration...")
        
        # Continue to interactive mode
        return session_database, current_workspace, current_module, current_payload, http_address, module_handler

def main():
    # Parse command-line arguments
    args = parse_arguments()
    
    # Check if running in one-liner mode (any arguments provided)
    if any([args.workspace, args.module, args.payload, args.http_address, args.set_var, args.run is not None, args.quiet]):
        # Execute one-liner mode
        result = execute_oneliner(args)
        if result is None:
            # One-liner completed and exited
            return
        # Otherwise, continue to interactive mode with loaded settings
        session_database, current_workspace, current_module, current_payload, http_address, module_handler = result
    else:
        # Initialize session normally (interactive mode from start)
        session_database, current_workspace, current_module, current_payload, http_address, module_handler = initialize_session()

    while True:
        try:
            # Get user input
            colored_module = output.colored(f"{current_module}", color='yellow')
            colored_payload = output.colored(f"{current_payload}", color='magenta')
            colored_input = f"{colored_module} > {colored_payload}: "
            user_input = input(f"{colored_input}").strip()
            command_parts = user_input.lower().split()

            if len(command_parts) == 0:
                continue

            if command_parts[0] == 'quit' or command_parts[0] == 'exit':
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

            elif command_parts[0] in ['run', 'breach']:
                # Check if a number is provided for the run command
                count = 1  # Default to 1 iteration
                if len(command_parts) > 1 and command_parts[1].isdigit():
                    count = int(command_parts[1])
                handle_run_module_command(session_database, module_handler, current_payload, http_address, count=count)


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

from colorama import Fore, Style

SUCCESS = f'{Style.BRIGHT}[{Fore.GREEN}✓{Fore.RESET}]{Style.RESET_ALL}'
ERROR = f'{Style.BRIGHT}[{Fore.RED}x{Fore.RESET}]{Style.RESET_ALL}'
WARNING = f'{Style.BRIGHT}[{Fore.YELLOW}!{Fore.RESET}]{Style.RESET_ALL}'
WHAT = f'{Style.BRIGHT}[{Fore.BLUE}?{Fore.RESET}]{Style.RESET_ALL}'

def debug_success(message: str):
    print(f'{SUCCESS}{message}')

def debug_error(message: str):
    print(f'{ERROR}{message}')

def debug_warning(message: str):
    print(f'{WARNING}{message}')

def debug_what(message: str):
        print(f'{WHAT}{message}')



def debug_server_started(host: str, port: int):
    debug_success(f' Server started on {Fore.YELLOW}{host}:{port}{Fore.RESET}')

def debug_server_not_stared(host: str, port: int):
    debug_error(f' Server not started on {host}:{port}')

def debug_server_start_permission():
    debug_success(' Server start permission...')

def debug_server_statistic(sleep_time: float, sleep_wait_time: float, max_clients_count: str | int = 'infinity'):
    print(f'''  | Sleep time: {Fore.CYAN}{sleep_time}s{Fore.RESET}
  | Sleep wait time: {Fore.CYAN}{sleep_wait_time}s{Fore.RESET}
  | Max clients count: {Fore.MAGENTA}{max_clients_count}{Fore.RESET}
''')

def debug_server_start_listening():
    debug_warning(' Server listening...')

def debug_server_stopped():
    debug_warning(' Server stopped.')

def debug_server_client_connected(client_host: str, client_port: int):
    debug_warning(f'{SUCCESS} Client connected: {Fore.YELLOW}{client_host}:{client_port}{Fore.RESET}')

def debug_server_client_id_received(client_host: str, client_port: int, client_id: str):
    print(f'{WARNING}{SUCCESS} Client ID received: {Fore.YELLOW}{client_host}:{client_port} {Fore.BLUE}ID={client_id}{Fore.RESET}')

def debug_server_client_id_not_received(client_host: str, client_port: int):
    print(f'{WARNING}{ERROR} Client ID not received: {Fore.YELLOW}{client_host}:{client_port}{Fore.RESET}')

def debug_server_client_disconnected(client_host: str, client_port: int):
    debug_warning(f' Client disconnected: {Fore.YELLOW}{client_host}:{client_port}{Fore.RESET}')

def debug_server_clients_count(clients_count: int, max_clients_count: str | int = 'infinity'):
    debug_what(f' Clients count: {Fore.MAGENTA}{clients_count} / {max_clients_count}{Fore.RESET}\n')

def debug_server_connection_rejected(client_host: str, client_port: int):
    debug_error(f' Connection rejected: {Fore.YELLOW}{client_host}:{client_port}{Fore.RESET} ')


def debug_client_created():
    debug_success(' Client created.')

def debug_client_statistic(sleep_time: float, sleep_wait_time: float, id: str):
    print(f'''  | Sleep time: {Fore.CYAN}{sleep_time}s{Fore.RESET}
  | Sleep wait time: {Fore.CYAN}{sleep_wait_time}s{Fore.RESET}
  | ID: {Fore.YELLOW}{id}{Fore.RESET}
''')

def debug_client_connected(host: str, port: int):
    debug_success(f' Client connected to {Fore.YELLOW}{host}:{port}{Fore.RESET}')

def debug_client_not_connected(host: str, port: int):
    debug_error(f' Client not connected to {host}:{port}')

def debug_client_id_sending_success():
    print(f'{WHAT}{SUCCESS} The server has received an ID.')

def debug_client_id_sending_error():
    print(f'{WHAT}{ERROR} The server has not received an ID.')



def debug_command_added_to_pool(command: str, client_id: str):
    debug_success(f' Command added to pool: "{Fore.YELLOW}{command}{Fore.RESET}" {Fore.BLUE}ID={client_id}{Fore.RESET}')

def debug_command_started_to_run(command: str, client_id: str):
    debug_warning(f' Command started to run: "{Fore.YELLOW}{command}{Fore.RESET}" {Fore.BLUE}ID={client_id}{Fore.RESET}')

def debug_command_unknown(command: str, client_id: str):
    debug_error(f' Unknown command: "{Fore.YELLOW}{command}{Fore.RESET}" {Fore.BLUE}ID={client_id}{Fore.RESET}')

def debug_list_command(n: int, client_address: str, client_id: str):
    debug_success(f'[{n}]: {Fore.YELLOW}{client_address} {Fore.BLUE}ID={client_id}{Fore.RESET}')
import os
import time
from colorama import Fore
from Net import Client
from Net import debugs
import threading


# client init and connect ----------------------------------------------------------------------------------------------
pc_id = input('Enter your PC-ID: ')
client = Client.Client(cid=pc_id).connect()
# client init and connect ----------------------------------------------------------------------------------------------


def command_explore(command: str):
    client.set_block(False)
    command_args = command.split(' ')
    if command_args[0] == 'list':
        try:
            clients_list = ''
            while clients_list == '':
                try:
                    clients_list = client.listen().split('||')[0]
                except: ... # noqa
            clients_list = clients_list.split('\n')
            debugs.debug_what(' Clients list.')
            for i, client_info in enumerate(clients_list):
                cl_address = client_info.split(' : ')[0]
                cl_id = client_info.split(' : ')[1].split(' ')[1]
                print('  |', f'{Fore.MAGENTA}{i}{Fore.RESET} >', f'{Fore.YELLOW}{cl_address}{Fore.RESET}', f'{Fore.BLUE}{cl_id}{Fore.RESET}')
        except: ... # noqa

    if command_args[0] == 'dir':
        files_list = ''
        while files_list == '':
            try:
                files_list = client.listen().split('||')[0]
            except: ... # noqa
        files_list = files_list.split('\n')
        if len(command_args) == 3:
            debugs.debug_what(f' Client {command_args[2]} files list.')
        elif len(command_args) == 1:
            debugs.debug_what(' Server files list.')
        for i, file_info in enumerate(files_list):
            if file_info:  # Check if line is not empty
                file_name = file_info.split(' : ')[0]
                file_size = file_info.split(' : ')[1]
                print('  |', f'{Fore.MAGENTA}{i}{Fore.RESET} >', f'{Fore.YELLOW}{file_name}{Fore.RESET}', f'{Fore.BLUE}{file_size}{Fore.RESET}')

def client_commands_send():
    global client
    while True:
        time.sleep(0.1)
        command = input('|> ')
        if command == 'exit':
            os.system('cls')
            client.close()
            os._exit(0) # noqa
        if command == '':
            continue
        if command[0] == '!':
            command = command[1:]
            client.send(command.encode())
            command_explore(command)

def client_loop():
    while True:
        client.set_block(True)
        time.sleep(0.1)
        try:
            command = client.listen()
            if command == 'get_dir':

                server_dir = os.path.abspath(os.path.curdir)
                sending_string = ''''''
                for file in os.listdir(server_dir):
                    file_path = os.path.join(server_dir, file)
                    if os.path.isfile(file_path):
                        file_size = os.path.getsize(file_path)
                        sending_string += f'{file} : {file_size} bytes\n'
                sending_string += '||'
                client.send(sending_string.encode())
                client.set_block(False)
        except: ... # noqa


threading.Thread(target=client_commands_send, daemon=False).start()
threading.Thread(target=client_loop, daemon=False).start()
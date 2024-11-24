import socket

from Net import Server
from Net import debugs
import threading
import time
import os

class FilesSender:
    def __init__(self):
        self.__commands_pool = []

    @property
    def pool(self) -> list[tuple[socket.socket, str, str]]:
        return self.__commands_pool

    def add_command(self, command: tuple[socket.socket, str, str]):
        self.__commands_pool.append(command)

file_sender = FilesSender()

def process_commands_add():
    global file_sender
    while True:
        time.sleep(0.05)
        try:
            for client_id in server.clients:
                client = server.clients[client_id]["client"]
                try:
                    command = client.recv(1024).decode()
                    if command != '':
                        file_sender.add_command((client, client_id, command))
                        debugs.debug_command_added_to_pool(command, client_id)
                except: ... # noqa
        except: ... # noqa

def command_parse(command: tuple[socket.socket, str, str]) -> list[any] | int:
    commands_args = command[2].split(' ')

    if commands_args[0] == 'list':
        return [command[0], command[1], 'list']
    if commands_args[0] == 'dir':
        if len(commands_args) == 3 and commands_args[1] == 'client':
            return [command[0], command[1], 'dir', 'client', commands_args[2]]
        return [command[0], command[1], 'dir']
    else:
        return -1

def command_run(command_args: list[any]):
    command_type = command_args[2]
    if command_type == 'list':
        sending_string = ''''''
        for client_id in server.clients:
            sending_string += f'{server.clients[client_id]['address']} : id {server.clients[client_id]['id']}\n'
        sending_string += '||'
        command_args[0].send(sending_string.encode())

    # TODO: Add dir client command
    if command_type == 'dir':
        if len(command_args) == 3:
            server_dir = os.path.abspath(os.path.curdir)
            sending_string = ''''''
            for file in os.listdir(server_dir):
                file_path = os.path.join(server_dir, file)
                if os.path.isfile(file_path):
                    file_size = os.path.getsize(file_path)
                    sending_string += f'{file} : {file_size} bytes\n'
            sending_string += '||'
            command_args[0].send(sending_string.encode())
        elif len(command_args) == 5 and command_args[3] == 'client':
            client_path_id = command_args[4]
            server.clients[client_path_id]['client'].send('get_dir'.encode())

            received_dirs = ''''''
            while received_dirs == '':
                try:
                    received_dirs = server.clients[client_path_id]['client'].recv(1024).decode()
                except: ... # noqa
            command_args[0].send(received_dirs.encode())

def process_commands_run():
    global file_sender
    while True:
        time.sleep(0.05)

        for command in file_sender.pool:
            debugs.debug_command_started_to_run(command[2], command[1])
            command_args = command_parse(command)
            if command_args != -1:
                command_run(command_args)
            else:
                debugs.debug_command_unknown(command[2], command[1])

            file_sender.pool.remove(command)
            break









# exit listening -------------------------------------------------------------------------------------------------------
Server.start_listen_exit_key()
# exit listening -------------------------------------------------------------------------------------------------------

# init and start server ------------------------------------------------------------------------------------------------
server = Server.Server().init()
server.start()
# init and start server ------------------------------------------------------------------------------------------------

# start listening -----------------------------------------------------------------------------------------------------
threading.Thread(target=process_commands_add, daemon=False).start()
threading.Thread(target=process_commands_run, daemon=False).start()






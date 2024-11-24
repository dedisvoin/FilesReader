import socket
from Net import debugs
from Net import settings
import time

import keyboard
import threading
import os




def start_listen_exit_key():
    def listen_exit_key():
        while True:
            i = input()
            if i == "exit":
                os.system('cls')
                os._exit(0) # noqa
    threading.Thread(target=listen_exit_key, daemon=False).start()


class Server:
    def __init__(self, host: str = settings.LOCAL_HOST, port: int = settings.LOCAL_PORT,
                 max_clients_count: str | int = settings.MAX_CLIENTS_COUNT) -> None:
        self.__host = host
        self.__port = port
        self.__server: socket.socket | None = None
        self.__connected_clients = {}
        self.__connect_pool:list[tuple[socket.socket, tuple]] = []
        self.__max_clients_count = max_clients_count

    @property
    def clients(self) -> dict[str, dict[str, socket.socket | int | str]]:
        return self.__connected_clients

    def init(self):
        try:
            self.__server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.__server.bind((self.__host, self.__port))
            self.__server.listen()
            debugs.debug_server_started(self.__host, self.__port)
            debugs.debug_server_statistic(settings.SLEEP_TIME, settings.SLEEP_WAIT_TIME, self.__max_clients_count)
            return self
        except: # noqa
            debugs.debug_server_not_stared(self.__host, self.__port)


    def listen(self):
        debugs.debug_server_start_listening()
        while True:
            time.sleep(settings.SLEEP_WAIT_TIME)
            client, address = self.__server.accept()

            self.__connect_pool.append((client, address))

    def start_listen(self):
        threading.Thread(target=self.listen, daemon=False).start()

    def permission(self):
        while True:
            time.sleep(settings.SLEEP_TIME)
            for client in self.__connect_pool:
                try:
                    _id = client[0].recv(1024).decode()
                    self.__connect_pool.remove(client)
                    client[0].send("YES".encode())
                    debugs.debug_server_client_id_received(client[1][0], client[1][1], _id)

                    connected = False
                    if self.__max_clients_count == 'infinity':
                        client[0].send('CONNECTED'.encode())
                        connected = True
                    elif len(self.__connected_clients) < self.__max_clients_count:
                        client[0].send('CONNECTED'.encode())
                        connected = True
                    else:
                        client[0].send('NO_CONNECTED'.encode())
                        debugs.debug_server_connection_rejected(client[1][0], client[1][1])



                    if connected:
                        client[0].setblocking(False)
                        self.__connected_clients[_id] = {
                            "client": client[0],
                            "address": client[1],
                            "id": _id,
                            "errors": 0,
                            "stime": 30
                        }
                        debugs.debug_server_client_connected(client[1][0], client[1][1])

                    debugs.debug_server_clients_count(len(self.__connected_clients), self.__max_clients_count)

                except: # noqa
                    client[0].send("NO".encode())
                    debugs.debug_server_client_id_not_received(client[1][0], client[1][1])


    def start_permission(self):
        debugs.debug_server_start_permission()
        threading.Thread(target=self.permission, daemon=False).start()

    def update(self): # noqa
        while True:
            time.sleep(settings.SLEEP_TIME)
            for client_id in self.__connected_clients:
                self.__connected_clients[client_id]["stime"] -= 1
                if self.__connected_clients[client_id]["stime"] <= 0:

                    try:
                        self.__connected_clients[client_id]["client"].send(f"UPDATE".encode())
                    except: # noqa
                        self.__connected_clients[client_id]["errors"] += 1

                if self.__connected_clients[client_id]["errors"] > 10:
                    debugs.debug_server_client_disconnected(self.__connected_clients[client_id]["address"][0], self.__connected_clients[client_id]["address"][1])
                    self.__connected_clients.pop(client_id)
                    debugs.debug_server_clients_count(len(self.__connected_clients), self.__max_clients_count)
                    break



    def start_update(self):
        threading.Thread(target=self.update, daemon=False).start()

    def start(self):
        self.start_listen()
        self.start_permission()
        self.start_update()

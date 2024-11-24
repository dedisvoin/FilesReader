import socket

from Net import debugs
from Net import settings
import uuid
import time

class Client:
    def __init__(self, host: str = settings.LOCAL_HOST, port: int = settings.LOCAL_PORT, cid: str | None = None) -> None:
        self.__host = host
        self.__port = port
        self.__client: socket.socket | None = None
        self.__id = str(uuid.uuid4()) if cid is None else cid

        debugs.debug_client_created()
        debugs.debug_client_statistic(settings.SLEEP_TIME, settings.SLEEP_WAIT_TIME, self.__id)

    def connect(self) -> 'Client':
        # creating client socket ---------------------------------------------------------------------------------------
        self.__client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # pre-connecting -----------------------------------------------------------------------------------------------
        try:
            self.__client.connect((self.__host, self.__port))
            debugs.debug_client_connected(self.__host, self.__port)
        except: # noqa
            debugs.debug_client_not_connected(self.__host, self.__port)
            exit(-1)

        # sending ID ---------------------------------------------------------------------------------------------------
        debugs.debug_warning(' Sending ID...')
        while True:
            try:
                time.sleep(0.5)
                self.__client.send(self.__id.encode())
                message = self.__client.recv(1024).decode()
                break
            except: ... # noqa

        if message == "YES":
            debugs.debug_client_id_sending_success()
        else:
            debugs.debug_client_id_sending_error()
            exit()

        # receiving connection to success ------------------------------------------------------------------------------
        while True:
            try:
                time.sleep(0.5)
                message = self.__client.recv(1024).decode()
                break
            except: ... # noqa

        if message == "CONNECTED":
            debugs.debug_client_connected(self.__host, self.__port)
        else:
            debugs.debug_client_not_connected(self.__host, self.__port)

        return self

    def set_block(self, value: bool):
        self.__client.setblocking(value)


    def close(self):
        self.__client.close()

    def send(self, data: bytes) -> None:
        self.__client.send(data)

    def listen(self, buffer_size: int = 1024) -> str:
        return self.__client.recv(buffer_size).decode().replace("UPDATE", '')
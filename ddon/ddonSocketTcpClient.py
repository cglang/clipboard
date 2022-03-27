# coding=utf-8
import json
import socket
import string
import sys
import threading
import uuid
import ddonSocketHead

headLenght = 500


class tcpClient:
    def __init__(self, host: string, port: int, byteHandler) -> None:
        self.client = socket.socket()
        self.client.connect((host, port))
        guidBytes = self.client.recv(16)
        self.clientId = uuid.UUID(bytes_le=guidBytes)
        print("客户端Id:" + str(self.clientId))
        self.byteHandler = byteHandler

    def start(self):
        threading.Thread(target=self.__consecutive_read_rtream,
                         daemon=True).start()
        return self

    def send(self, data: bytes, sendClientId, sendGroupId):
        headBytes = self.__get_head_bytes(
            data.__len__(), sendClientId, sendGroupId)
        self.client.send(self.__merge_bytes(headBytes, data))

    def __consecutive_read_rtream(self) -> uuid:
        try:
            while True:
                head = self.__read_head_by_stream(self.client)
                self.byteHandler(self.client.recv(head.Length))
        except socket.error as e:
            print(e)
            sys.exit(0)

    def __read_head_by_stream(self, client: socket.socket) -> ddonSocketHead.Head:
        by = client.recv(headLenght)
        text = str(by, "utf-8").strip(b'\x00'.decode())
        return json.loads(text, object_hook=ddonSocketHead.Head)

    def __get_head_bytes(self, length, sendClientId, sendGroupId) -> bytes:
        head = ddonSocketHead.Head(None)
        head.ClientId = str(self.clientId)  # 无所谓
        # head.GroupId = str(self.clientId) # 无所谓
        head.Length = length  # 消息长度
        # head.Mode = 1
        head.OpCode = 10002  # 用于消息转发
        head.SendClient = sendClientId
        # head.SendGroup = '00000000-0000-0000-0000-000000000000'
        head.Type = 1  # 传输文本
        return json.dumps(head.__dict__).encode('utf-8')

    def __merge_bytes(left, byte1: bytes, byte2: bytes):
        bytes = bytearray(byte1)
        empty_bytes = bytes(headLenght-byte1.__len__())
        bytes.extend(empty_bytes)
        bytes.extend(byte2)
        return bytes

# coding=utf-8
import json
import socket
import struct
import threading


class TcpSocket:

    def __init__(self, socket: socket.socket, bytehandle):
        self.socket = socket
        self.bytehandle = bytehandle
        # print("server")

    def start(self):
        threading.Thread(target=self.while_recv).start()

    # 发送类方法
    def send(self, data: str):
        self.socket.send(struct.pack('i', len(data)))
        self.socket.send(data.encode("utf-8"))

    def send_dict(self, data_dict):
        self.send(json.dumps(data_dict))

    # 接受类方法
    def recv(self):
        size = struct.unpack('i', self.socket.recv(4))[0]
        data = b''
        while size:
            buf = self.socket.recv(size)
            size -= len(buf)
            data += buf
        return data

    def recv_dict(self):
        return json.loads(self.recv())

    def while_recv(self):
        while True:
            try:
                bytes = self.recv()
                self.bytehandle(bytes)
            except Exception as e:
                print(e)

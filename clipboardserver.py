import tcpsocket
import socket

# 所有的功能代码都从这个文件里开始写

host = '127.0.0.1'
port = 8887
connections = []
_server = socket.socket()
_server.bind((host, port))
_server.listen(5)


def bytehandle(bytes: bytes):
    print(bytes.decode("utf-8"))
    for a in connections:
        a.send(bytes.decode("utf-8"))


while True:
    conn, address = _server.accept()
    tcp = tcpsocket.TcpSocket(conn, bytehandle)
    tcp.start()
    connections.append(tcp)

import ddon.ddonSocketTcpClient as ddonSocketTcpClient


def byte_handler(bytes):
    text = str(bytes, "utf-8")
    print(text)

client = ddonSocketTcpClient.tcpClient(
    "192.168.0.102", 9664, byte_handler).start()

while True:
    clientId = input("接收方Id:")
    text = input("消息:")
    client.send(text.encode("utf8"), clientId, clientId)

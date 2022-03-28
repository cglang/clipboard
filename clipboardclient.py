import client


# 所有的功能代码都从这个文件里开始写
def bytehandle(bytes: bytes):
    print(bytes.decode())


conn = client.Client("127.0.0.1", 8887, bytehandle)
conn.start()

while True:
    text = input("发送内容:")
    conn.send(text)

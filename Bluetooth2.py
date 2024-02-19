import socket

client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
client.connect(("38:d5:7a:7d:5d:2e",4))

try:
    while True:
        message = input("Send message: ")
        client.send(message.encode('utf-8'))
        data = client.recv(1024)
        if not data:
            break
        print(f"message:{data.decode('utf-8')}")
except OSError as e:
    pass

client.close()

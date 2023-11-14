import socket

def send(msg:str) -> bytes:
    socket_client.send(str(len(msg)).encode("utf-8").ljust(64))
    socket_client.send(msg.encode())

def call_add():
    pass

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("localhost",3000))

while True:
    print("What do you want?\n1. Create a new function\n2. Execute a function\n3. See proprieties of a fuction\n0. Exit")
    msg_client = send(input())
    if socket_client:
        if msg_client != "0":
            pass
        else:
            break
        break
    break
socket_client.close()

print("See you later!")

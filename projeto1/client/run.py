import socket
# import json

PORT=3000
MAX_SIZE_BUFFER = 4096

# def receive_info_defs(json_server):
#     # Deserialize JSON data
#     json_data_received = json.loads(json_server)
#     print('Received JSON data:', json_data_received)

def send(message:str):
    return socket_client.send(str(len(message)).encode("utf-8").ljust(64))

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("localhost",PORT))

while True:
    try:
        print("What do you want?\n1. Execute a function\n2. See proprieties of a fuction\n\n\r0. Exit")
        msg = send(input("\n"))
        # json_server = socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8')
        # print(json_server)
    except Exception as e:
        print("Erro:\n",e)
    finally:
        socket_client.close()
        print("See you later!")
        break

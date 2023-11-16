import socket
import json

PORT=3000
MAX_SIZE_BUFFER = 4096

# def receive_info_defs(json_server):
#     # Deserialize JSON data
#     json_data_received = json.loads(json_server)
#     print('Received JSON data:', json_data_received)

def send(message:str):
    socket_client.sendall(bytes(message,encoding="utf-8"))

socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
socket_client.connect(("localhost",PORT))

# TODO - limpar a mensagem em JSON e transformá-la em uma lista global de funções
def list_functions(msg):
    pass


def run():
    try:
        while True:
            print("What do you want?\n1. Execute a function\n2. See proprieties of a fuction\n\n\r0. Exit")
            msg = input("\n")
            send(msg)
            json_server = json.loads(socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8'))
            print(json_server)
            if msg == "2":
                list_functions(json_server)
            elif msg == "0":
                break
    except Exception as e:
        print("Erro:\n",e)
    finally:
        socket_client.close()
        print("See you later!")

run()

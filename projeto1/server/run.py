import socket
from multiprocessing import Process
import inspect
import defs.add as add
import defs.div as div
import defs.multi as multi
import defs.sub as sub
import json

PORT = 3000
MAX_SIZE_BUFFER = 4096
MAX_CONNECTION = 5

def get_info_defs():
    infos = {}
    add_sign = inspect.signature(add.add)
    add_args = inspect.getfullargspec(add.add)
    sub_sign = inspect.signature(sub.sub)
    sub_args = inspect.getfullargspec(sub.sub)
    div_sign = inspect.signature(div.div)
    div_args = inspect.getfullargspec(div.div)
    multi_sign = inspect.signature(multi.multi)
    multi_args = inspect.getfullargspec(multi.multi)
    infos["sum"]={"sign":add_sign,"args":add_args},
    infos["sub"]={"sign":sub_sign,"args":sub_args},
    infos["div"]={"sign": div_sign,"args":div_args},
    infos["multi"]={"sign":multi_sign,"args":multi_args}
    
    return json.dumps(infos)

def handler_client(client_socket):
    try:
        while True:
            msg = client_socket.recv(MAX_SIZE_BUFFER).decode()
            print("client say: ", msg)
    except Exception as e:
        print(f"Erro ao lidar com o cliente: {e}")
    finally:
        client_socket.close()
        print("See you later!")


server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(("localhost",PORT))
server_socket.listen(MAX_CONNECTION)
print("Waiting connections...")

while True:
    conn, address = server_socket.accept()
    print(address[0], "conectado ao servidor")
    process = Process(target=handler_client, args=(conn,address))
    process.start()
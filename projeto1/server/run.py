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

ACTIONS = {
    "EXECUTE" : "1",
    "LIST" : "2",
    "EXIT" : "0"
}

def get_info_defs():
    print(add.add.__getattribute__)
    infos = {}
    add_sign = {
        'name' : add.add.__name__,
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    div_sign = {
        'name' : div.div.__name__,
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    multi_sign = {
        'name' : multi.multi.__name__,
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    sub_sign = {
        'name' : sub.sub.__name__,
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    
    infos["sum"]=add_sign
    infos["sub"]=sub_sign
    infos["div"]=div_sign
    infos["multi"]=multi_sign
    
    return infos

def handler_client(client_socket):
    try:
        while True:
            response = {
                "header":'',
                "body" : ''
            }
            msg = client_socket.recvmsg(MAX_SIZE_BUFFER)[0].decode("utf-8")
            print("client say: ", msg)
            if (msg == ACTIONS["EXIT"]):
                print("Action: Exit")
                response['header']  = {"status" : 200}
                print(response)
                client_socket.sendmsg([json.dumps(response).encode("utf-8")])
                break
            elif (msg == ACTIONS["LIST"]):
                 print("Action: List")
                 response['header']  = {"status" : 200}
                 response['body'] = get_info_defs()
                 print(response)
                 client_socket.sendmsg([json.dumps(response).encode("utf-8")])
            elif (msg == ACTIONS["EXECUTE"]):
                 print("Action: Execute")
            else:
                print("Código Inválido")
                break    
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
    process = Process(target=handler_client, kwargs=({'client_socket' : conn}))
    process.start()
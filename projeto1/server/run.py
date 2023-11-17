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

functions = {
    add.add.__name__ : add.add,
    sub.sub.__name__ : sub.sub,
    div.div.__name__ : div.div,
    multi.multi.__name__ : multi.multi,
}

def HasFailed(json):
    if json['header']['status'] != 200:
        return True

def get_info_defs():
    infos = {}
    add_sign = {
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    div_sign = {
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    multi_sign = {
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    sub_sign = {
        'args' : 2,
        'argType' : "Integer",
        'return' : "Integer"  
    }
    
    infos[add.add.__name__]=add_sign
    infos[sub.sub.__name__]=sub_sign
    infos[div.div.__name__]=div_sign
    infos[multi.multi.__name__]=multi_sign
    
    return infos

def exec(func, args):
    global functions
    
    # if func in function:
    pass

def handler_client(client_socket):
    try:
        while True:
            response = {
                "header":'',
                "body" : ''
            }
            json_client = json.loads(client_socket.recvmsg(MAX_SIZE_BUFFER)[0].decode("utf-8"))
            print("client say: ", json_client)

            if HasFailed(json_client):
                response['header'] = {'status':500}
            else:
                msg = json_client['body']['message']
                content = json_client['body']['content']
                if (msg == ACTIONS["EXIT"]):
                    print("Action: Exit")
                    response['header']  = {"status" : 200}
                    client_socket.sendmsg([json.dumps(response).encode("utf-8")])
                    break
                elif (msg == ACTIONS["LIST"]):
                    print("Action: List")
                    response['header']  = {"status" : 200}
                    response['body'] = get_info_defs()
                    client_socket.sendmsg([json.dumps(response).encode("utf-8")])
                elif (msg == ACTIONS["EXECUTE"]):
                    print("Action: Execute")
                    func, args = content.split(':')
                    args = args.split(",")

                    print (func,args)

                    response['body'] = exec(func,args)

                    response['header'] = {'status': 200}
                    client_socket.sendmsg([json.dumps(response).encode("utf-8")])
                else:
                    print("Código Inválido")
                    response['header'] = {'status':500}
                    client_socket.sendmsg([json.dumps(response).encode("utf-8")])
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
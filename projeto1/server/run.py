import socket
from multiprocessing import Process
import defs.add as add
import defs.div as div
import defs.multi as multi
import defs.sub as sub
import json

PORT = 3333
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

def send(msg,socket):
    socket.sendmsg([json.dumps(msg).encode("utf-8")])

def HasFailed(msg):
    return msg['header']['status'] != 200

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
    
    if func in functions:
        return functions[func](args)
    else:
        raise Exception('Function not in the list!')

def handler_client(client_socket):
    while True:
        try:
            response = {
                "header":'',
                "body" : ''
            }
            json_client = json.loads(client_socket.recvmsg(MAX_SIZE_BUFFER)[0].decode("utf-8"))
            print("client say: ", json_client)

            if HasFailed(json_client):
                raise Exception('Bad Request.')
            else:
                msg = json_client['body']['message']
                content = json_client['body']['content']
                if (msg == ACTIONS["EXIT"]):
                    print("Action: Exit")
                    response['header']  = {"status" : 200}

                    send(response,client_socket)
                    break
                elif (msg == ACTIONS["LIST"]):
                    print("Action: List")
                    response['header']  = {"status" : 200}
                    response['body'] = get_info_defs()

                    send(response,client_socket)
                elif (msg == ACTIONS["EXECUTE"]):
                    print("Action: Execute")

                    # Args Cleanup
                    func, args = content.split(':')
                    args = list(map(int,args.split(",")))

                    # Setting response flags and values
                    response['body'] = exec(func,args)
                    response['header'] = {'status': 200}

                    send(response,client_socket)
                else:
                    raise Exception('Invalid Command.')  
        except Exception as e:
            print(f"Erro ao lidar com o cliente: {e}")
            response['header'] = {'status':500,'error':f"{e}"}

            send(response,client_socket)

    # Closing connection
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
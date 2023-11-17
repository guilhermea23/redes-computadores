import socket
import json

PORT=3000
MAX_SIZE_BUFFER = 4096

ACTIONS = {
    "EXECUTE" : "1",
    "LIST" : "2",
    "EXIT" : "0"
}

# def receive_info_defs(json_server):
#     # Deserialize JSON data
#     json_data_received = json.loads(json_server)
#     print('Received JSON data:', json_data_received)

socket_client = None

def send(message:str,*content):
    if content:
        content = content[0]
    msg = {'header': {'status': 200},'body': {'message' : message,'content':content}}

    socket_client.sendall(bytes(json.dumps(msg),encoding="utf-8"))

def receive():
    return json.loads(socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8')) 

stubs = {} 
functions = {}

def runFunc(name ,**kwargs):
    msg = f"{name}:"
    for i in kwargs['kwargs']:
        num = kwargs['kwargs'][i]
        msg = msg + num + ","
    return msg[:-1] 
    
def createStub(name, **kwargs):
    def method (**kwargs):
        return runFunc(name, **kwargs)
    return method

def isSuccessful(msg):
    if msg['header']['status'] != 200:
        raise Exception('Status code error :',msg['header']['status'])
    return True


# TODO - limpar a mensagem em JSON e transformá-la em uma lista global de funções
def list_functions(msg):
    isSuccessful(msg)

    global stubs
    global functions

    message = ""

    
    for func in msg['body'] :
        stubs[func] = createStub(func)
        functions[func] = msg['body'][func] 
        message = message + f"{func} : {msg['body'][func]['args']} {msg['body'][func]['argType']} -> {msg['body'][func]['return']}\n"
    
    print(stubs)
    print(functions)
    print(f"List of all functions:\n\n{message}")


def exec(name,msg, **kwargs):
    if (name not in stubs) or (name not in functions):
        raise Exception("Function doesn't exist!")
    print(stubs[name](**kwargs))
    send(msg,stubs[name](**kwargs))

    response = receive()

    return response


def run():
    global socket_client

    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(("localhost",PORT))

    try:
        while True:
            print("What do you want?\n1. Execute a function\n2. List all functions\n\n\r0. Exit")
            msg = input("\n")
            print(type(msg))
            # Exit and cut connection with the server
            if msg == ACTIONS['EXIT']:
                send(msg)
                json_server = json.loads(socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8'))
                print(json_server)
                if isSuccessful(json_server):
                    break
                else: 
                    print(f"Error: Status code number {json_server['header']['status']}")

            # Execute the server function
            elif msg == ACTIONS['EXECUTE']:
                if stubs == {}:
                    print("You have to list the functions first!")
                else:
                    print("Which function do you want to execute?")
                    args = {}
                    while True:
                        func = input("\n")
                        if not (func not in stubs) or not (func not in functions):
                            break
                        print ("Function is not on the list!")
                    
                    print("Enter the arguments:")
                    for i in range(functions[func]['args']):
                        args[f'{i}'] = input('\n')
                    print(args)
                    print("The response of your request is:")
                    print(exec(name = func,msg = msg, kwargs = args))

            # List Server functions and create stub functions
            elif msg == ACTIONS['LIST']:
                send(msg)
                json_server = json.loads(socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8'))
                print(json_server)
                if isSuccessful(json_server) :
                    list_functions(json_server)
                else:
                    print(f"Error: Status code number {json_server['header']['status']}")
    except Exception as e:
        print("Erro:\n",e)
    finally:
        socket_client.close()
        print("See you later!")

run()

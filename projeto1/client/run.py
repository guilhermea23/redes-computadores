import socket
from multiprocessing import Process
import json

PORT=3333
MAX_SIZE_BUFFER = 4096

ACTIONS = {
    "EXECUTE" : "1",
    "LIST" : "2",
    "EXIT" : "0"
}

socket_client = None

def send(message:str,*content):
    if content:
        content = content[0]
    msg = {'header': {'status': 200},'body': {'message' : message,'content':content}}

    socket_client.sendall(bytes(json.dumps(msg),encoding="utf-8"))

def receive():
    msg = json.loads(socket_client.recv(MAX_SIZE_BUFFER).decode('utf-8')) 
    if msg['header']['status'] != 200:
        return f"Error code - {msg['header']['status']} : {msg['header']['error']}",False
    return msg['body'],True

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

def list_functions(msg):

    global stubs
    global functions

    message = ""

    for func in msg :
        stubs[func] = createStub(func)
        functions[func] = msg[func] 
        message = message + f"{func} : {msg[func]['args']} {msg[func]['argType']} -> {msg[func]['return']}\n"
    
    return (f"List of all functions:\n\n{message}")


def exec(name,msg, **kwargs):
    if (name not in stubs) or (name not in functions):
        return False
    send(msg,stubs[name](**kwargs))
    return True


def run():
    global socket_client

    # Create connection
    socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket_client.connect(("localhost",PORT))


    while True:
        retries = 0
        print("What do you want?\n1. Execute a function\n2. List all functions\n\n\r0. Exit")
        msg = input("\n> ")
        print()

        # Exit and cut connection with the server
        if msg == ACTIONS['EXIT']:
            send(msg)
            response,success = receive()
            print(response)
            if success:
                break

        # Execute the server function
        elif msg == ACTIONS['EXECUTE']:
            if stubs == {}:
                print("You have to list the functions first!")
            else:
                print("Which function do you want to execute?")
                args = {}
                while True:
                    func = input("\n> ")
                    if not (func not in stubs) or not (func not in functions):
                        break
                    print ("Function is not on the list!")
                
                print("Enter the arguments:")
                for i in range(functions[func]['args']):
                    for x in range(100):
                        entry = input("\n> ")
                        if entry.isdecimal():
                            args[f'{i}'] = entry
                            break
                        else:
                            print("Invalid Input. Try Again.")

                
                if exec(name = func,msg = msg, kwargs = args):
                    response , success = receive()
                    if success:
                        print(f"The response of your request is: {response}")
                    else:
                        print(response)
                else:
                    print("Function doesn't exist.")

        # List Server functions and create stub functions
        elif msg == ACTIONS['LIST']:
            send(msg)
            response,success = receive()
            if success:
                print(list_functions(response))
            else:
                print(response)
        else:
            print('Try again.\n\n')
    
    # Finalize connection
    socket_client.close()
    print("See you later!")

run()

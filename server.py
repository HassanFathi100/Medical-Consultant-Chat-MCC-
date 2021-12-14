import socket
import threading


host = '127.0.0.1'
port = 9090

#Opening the server and make it ready for connection requests
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()

clients = []
names = []

#Sending messges to all clients
def broadcast(message):
    for client in clients:
        client.send(message)
        

#Receveing messages from one client and send it to all clients
def receive():
    while True:
        client, address = server.accept()
        print(f"Connected with {str(address)}!")
        
        client.send("NICK".encode("utf-8"))
        name = client.recv(1024)
        names.append(name)
        clients.append(client)
        
        print(f"Name of the client is {name}")
        broadcast(f"{name} connected to the server \n".encode('utf-8'))
        #client.send("Connected to the server \n".encode('utf-8'))
        
        thread = threading.Thread(target = handle, args = (client,))
        thread.start()
        
        
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            print(f"{ names[clients.index(client)] }")
            broadcast(message)
            
        except:
            index = clients.index(client)
            
            clients.remove(client)
            client.close()
            
            name = names[index]
            names.remove(name)
            
            break

print("Server is running...")
receive()
import socket
import threading

host = '127.0.0.1'
port = 55555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen()

clients = []
names = []

def broadcast(message):
    for client in clients:
        client.send(message)

# When client joins, client and server can send message to each other
def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            ex_name = names[index]
            broadcast(f'{ex_name} has been kicked out')
            names.remove(ex_name)
            break

def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {str(address)}')

        client.send('NAME'.encode('ascii'))
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)
        print(f'{name} is the name')
        broadcast(f'{name} joined the chat'.encode('ascii'))
        client.send(f'{name} Welcome to The Server'.encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()
print('listening')
receive()
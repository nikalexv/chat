#!/usr/bin/env python3
from socket import AF_INET, socket, SOCK_STREAM
from threading import Thread

def accept_incoming_connections():
    while True:
        conn, addr = SERVER.accept() #wait incoming connections
        print("соединено:", addr)
        conn.send(bytes("Welcome! , add your name and press Enter", "utf8"))
        #addresses[conn] = addr
        Thread(target=handle_conn, args=(conn,)).start()

def handle_conn(conn):
    name = conn.recv(BUFSIZ).decode("utf8")
    welcome = 'Welcome %s! Press quit! to exit.' % name
    conn.send(bytes(welcome, "utf8"))
    msg = "%s in the chat" % name
    broadcast(bytes(msg, "utf8"))
    clients[conn] = name

    while True:
        msg = conn.recv(BUFSIZ)

        if msg != bytes("quit!", "utf8"):
            broadcast(msg, name+": ")
        else:
            conn.send(bytes("quit!", "utf8"))
            conn.close()
            del clients[conn]
            broadcast(bytes("%s left chat" % name, "utf8"))
            break


def broadcast(msg, prefix=""):
    for sock in clients:
        sock.send(bytes(prefix, "utf8")+msg)

clients = {}
#addresses = {}

HOST = '127.0.1.1'
PORT = 33000
BUFSIZ = 1024
ADDR = (HOST, PORT)

SERVER = socket(AF_INET, SOCK_STREAM)
SERVER.bind(ADDR)

if __name__ == "__main__":
    SERVER.listen(5) #number of unaccepted connections system will allow before refusing new connections
    print("waiting connection")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
    SERVER.close()


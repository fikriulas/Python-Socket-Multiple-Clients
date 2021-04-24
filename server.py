import socket
import threading
import json
import colorama
from colorama import Fore, Back, Style

HEADER = 64
PORT = 5050
SERVER = "localhost"
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
CLIENTS = {}

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected.")
    connected = True

    while connected:
        try:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    connected = DisconnectClient(msg,addr)                    
                if msg == "!1": ## client bağlantıdaki client listesini istemiş ise bu method çalışır.
                    ListOfClient(addr)
                if msg[0:2] == "!2":
                    SendClient(msg,addr)
                print(f"[{addr}] {msg}")    
        except:
            print("Client bağlantısı beklemedik şekilde kesildi.")
            DeleteClient(addr)
            connected = False        

    conn.close()

def DisconnectClient(msg,addr):    
    msg = DISCONNECT_MESSAGE
    CLIENTS[addr].send(msg.encode())
    DeleteClient(addr)
    return False

def SendAllCLient():
    connected = True
    while connected:
        mesaj = input("")
        mesaj = "Server: "+mesaj
        for client in CLIENTS:
            CLIENTS[client].send(mesaj.encode())        
        if mesaj == DISCONNECT_MESSAGE:
                connected = False

def SendClient(msg,addrg):
    addr = msg[3:8]
    message = str(addrg[1]) + ": " +msg[9:]  
    for client in CLIENTS:
        if str(client[1]) == str(addr):
            CLIENTS[client].send(message.encode())

def ListOfClient(addr):   
    ## isteyen client'a bağlantıdaki kendisi haric clientların listesini gönderir.   
    print("Clientların listesi ilgili client'a gönderiliyor...")
    arrayOfClients = []    
    for c in CLIENTS:
        if c == addr: ## istekte bulunan client'ın addr numarası yanına yoursID eklenir.
            msg = "-> "+ str(c[1]) + "[Yours ID]"
            arrayOfClients.append(msg)            
            continue
        msg = "-> "+ str(c[1]) ## tüm client addr numaraları uygun formatta msg değişkenine atılır.
        arrayOfClients.append(msg) ## msg değişkeni arrayOfClients arrayine eklenir.
    jsonOfAddrList = json.dumps({"addr":arrayOfClients}) ## veriler json tipinde gönderileceği için dump edilir.   
    # clienta giden mesajlar normalde json tipinde olmadığı için. Json tipinde veri  
    ## gönderildiğini anlaması için başına !j ifadesi eklenir.
    jsonOfAddrList = "!j"+jsonOfAddrList       
    CLIENTS[addr].send(jsonOfAddrList.encode()) ## hazırlanan veri encode edilip ilgili client'a gönderilir. gönderilir.

def DeleteClient(addr):
    del CLIENTS[addr] ## disconnect isteği gönderen client, listeden silinir.

def start():
    server.listen()
    print(f"[LISTENING] Server is listening on {SERVER}")
    while True:
        try:
            conn, addr = server.accept()
            CLIENTS[addr] = conn        
            thread = threading.Thread(target = handle_client, args=(conn, addr))        
            thread.start()
            thread2 = threading.Thread(target = SendAllCLient, args=())        
            thread2.start()
            print(f"[ACTIVE CONNECTIONS] {threading.activeCount() -1}")
        except:
            print(Fore.RED + Back.WHITE +"[STOPPED]" + Back.RESET +" Server Başlatamadı." + Style.RESET_ALL)

print("[STARTING] server is starting...")
start()
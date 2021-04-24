import socket
import sys
import time
import json
import threading
import colorama
from colorama import Fore, Back, Style

HEADER = 64
PORT = 5050
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "!q"
SERVER = "localhost"
ADDR = (SERVER,PORT)
SERVER_DISCONNECT = 0
STATUS = True

def Send():
    global STATUS
    global threadSend
    while STATUS:    
        try:
            msg = input("")
        except EOFError:
            print("Çıkış Yapılıyor...")
            STATUS = False
            break
        message = msg.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        if msg == DISCONNECT_MESSAGE:
            STATUS = False
        if msg == "!h":
            Help()
        try:
            client.send(send_length)
            client.send(message)
        except:
            STATUS = False
            ServerDISC() ## server_disconnect'i 1 arttırır.
        
def Receive():
    global STATUS
    while STATUS:
        try:
            msg = client.recv(1024).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                print(Fore.RED + "Bağlantı güvenli şekilde sonlandırıldı."+ Style.RESET_ALL)
                print(Fore.BLUE + "Çıkmak için CTRL + C Basın"+ Style.RESET_ALL)
                break
            if msg[0:2] == "!j": # clientların listesi json formatında geliyor.                
                jsonOfAddrList = json.loads(msg[2:])                
                arrayOfClients = jsonOfAddrList.get("addr")
                for clients in arrayOfClients:
                    print(clients)
                continue
            print(msg)                               
        except:
            STATUS = False            
            ServerDISC() ## server_disconnect'i 1 arttırır.

def ServerDISC():    
    global SERVER_DISCONNECT
    SERVER_DISCONNECT += 1
    if SERVER_DISCONNECT == 2:
        print("Mesaj Gönderip, Alınamıyor; Sunucu Bağlantısı Kesildi.")
        print("Çıkmak için CTRL + C'ye basın ")  

def Help():
    print(Fore.BLUE + Back.WHITE +"[LEARNING]" + Back.RESET + Style.RESET_ALL +" Bağlantıyı güvenlik bir şekilde kapatmak için \n!q'e basın.")
    print(Fore.BLUE + Back.WHITE +"[LEARNING]" + Back.RESET + Style.RESET_ALL +" Sunucudan konuşmak istediğiniz clientların listesi için \n!1'e basın.")
    print(Fore.BLUE + Back.WHITE +"[LEARNING]" + Back.RESET + Style.RESET_ALL +" Konuşmak istediğiniz client'ın addr numarasını başında !2 olarak girin. \nORN: !2 54789 'YOUR MESSAGE' [ENTER]")

try:
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(ADDR)
    print(Fore.GREEN + Back.WHITE +"[LISTENING]" + Back.RESET + " Client has been ready message to server..." + Style.RESET_ALL)
    threadSend = threading.Thread(target = Send, args=())        
    threadSend.daemon = True
    threadSend.start()
    threadReceive = threading.Thread(target = Receive, args=())
    threadReceive.daemon = True
    threadReceive.start()
except:
    print(Fore.RED + Back.WHITE +"[STOPPED]" + Back.RESET +" Cannot connect with the server, try again." + Style.RESET_ALL)

while True:
    try:        
        time.sleep(1)
    except KeyboardInterrupt:
        print("Çıkış Başarıyla Sağlandı.")
        sys.exit(1)






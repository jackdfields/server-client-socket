""" Client connection to Server to send/receive information """
import socket
import os
import sys
import time
import datetime

def Main():
    host = "127.0.0.1"
    port = 3452
    buffer_time = 1024
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    connected = True

    while True:
        #send in files in from directory
        path_walker(r'C:\storeman\Office\XF001901')
        #read file created by dir_scanner
        with open("pycache.txt", "r") as file:
            files_in_dir = file.read()
        print(files_in_dir)
        curr_time = str(datetime.datetime.now())
        try:
                msg = (files_in_dir + " " + curr_time)
                client_socket.send(msg.encode())
                time.sleep(5)
        except socket.error:
            #reconnnect
            print("Connection Lost - attempting to reconnect")
            connected = False
            #recreate/connect socket
            client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

            while not connected:
                try:
                    client_socket.connect((host, port))
                    connected = True
                    print("reconnected at " + curr_time)
                except socket.error:
                    time.sleep(2)
                    
    client_socket.close()

def path_walker(path):
        # important: make sure count=0 to reset count every call
        comp_name = os.environ["COMPUTERNAME"] # grab computer name
        count = 0
        for root, dirs, files in os.walk('C:\storeman\Office\XF001901'):
                count += len(files)
        with open("pycache.txt", "w") as file:
                file.write(f"{comp_name}: num of files: {count}")
                
if __name__ == "__main__":
        Main()

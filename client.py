""" Client connection to Server to send/receive information """
import socket
import os
import dir_scanner
import time
import datetime

def Main():
    host = "127.0.0.1"
    port = 3452
    buffer_time = 1024
    
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    connected = True
    
    #send in files in from directory
    comp_name = os.environ["COMPUTERNAME"] # grab computer name
    files_in_dir = str(dir_scanner)

    while True:
        curr_time = str(datetime.datetime.now())
        try:
                msg = (comp_name + "," + files_in_dir + " " + curr_time)
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
if __name__ == "__main__":
        Main()

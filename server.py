""" Server side host in Server-Client port connection
                this program receives a message and sends it back in full caps to confirm that it
                received the message"""
import socket
import sys
import traceback
from _thread import *
import threading 

def Main():
        host  = "127.0.0.1"
        port = 3452
        buffer_time = 1024

        #server socket 
        serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        serv_socket.bind((host, port))
        #listen for up to 5 connections at once
        serv_socket.listen(5)

        while True:
              
                conn, addr = serv_socket.accept()
                print ("Connection from: %s" % addr[0])
        
                data = conn.recv(buffer_time).decode()
                temp_str = str(data)
                #temp_str.split(",") creates a list
                pc_name, files_in_loc = temp_str.split(",")
                temp = files_in_loc.replace("<","")
                files_in_loc = temp.replace(">","")
                        
                #write to file
                print("writing data to file ...")
                print (files_in_loc)
                html_wrkspc = ("<html>\n<body>\n<h1>The Report</h1>\n<p>" + pc_name + " : " + files_in_loc + "</p>\n</body>\n</html>")
                
                with open("report.html", "w") as file:
                          file.write(html_wrkspc)
                
                if not data: # if nothing is received, break the connection
                        print ("Connection ended.")
                        break

if __name__ == '__main__':
        Main()

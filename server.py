""" Server side host in Server-Client port connection
                this program receives a message and sends it back in full caps to confirm that it
                received the message"""
import socket
import sys
import traceback
from _thread import *
import threading

# threaded connection
def threader(conn):
        while True:
                data = conn.recv(1024).decode()
                #if data not received
                if not data:
                        print("no data received.")
                        break

                # convert data into a str to be documented
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
                # make connection with clients
                conn, addr = serv_socket.accept()
                print ("Connection from: %s" % addr[0])
                
                # first arg is function to call, second is tuple cont pos
                start_new_thread(threader, (conn,))

        serv_socket.close()

if __name__ == '__main__':
        Main()

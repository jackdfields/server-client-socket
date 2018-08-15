""" Server side host in Server-Client port connection
                this program receives a message and sends it back in full caps to confirm that it
                received the message"""
import socket
import sys
from _thread import *
import threading
import time
from pySql import PySQLTrans

# threaded connection
def threader(conn):
    while True:

        data = conn.recv(1024).decode()
        # if data not received
        if not data:
            print("no data received.")
            break
        #print(data)

        # convert data into a str to be documented
        temp_str = str(data)
        comp_name, num_files = temp_str.split(": ")

        #transfer to SQL Server
        db_acct = PySQLTrans(comp_name, num_files)
        db_acct.sql_db_upload()
        # Grab data
        report = db_acct.sql_db_dowload()

        with open('report_dialogue.txt', 'r') as file:
            html_reader = file.read()

        html_wrkspc = ('<!DOCTYPE html>\n'
                       '<html>\n'
                       '<head>\n'
                       '<meta http-equiv="refresh" content="5">\n'
                       '<style>\n'
                       'table {\n'
                       '\tfont-family: times, sans-serif;\n'
                       '\tborder-collapse: collapse;\n'
                       '\twidth: 100%;\n'
                       '}\n'
                       'td, th {\n'
                       '\tborder: 1px solid #dddddd;\n'
                       '\ttext-align: middle;\n'
                       '\tpadding: 5px;\n'
                       '}\n'
                       'tr:nth-child(even) {\n'
                       '\tbackground: #C1C1C1;\n'
                       '}\n'
                       '</style>\n'
                       '</head>\n'
                       '<body>\n\n'
                       
                       '<h2>Dashboard</h2>\n'
                       '<table>\n'
                       '  <tr>\n'
                       '\t<th>Machine</th>\n'
                       '\t<th>Files</th>\n'
                       '\t<th>Time Stamp</th>\n'
                       '  </tr>\n'
                        + html_reader + 
                       '</table>\n'
                       '</body>\n'
                       '</html>\n')
        
        with open("report.html", "w") as file:
            file.write(html_wrkspc)

def Main():
    host = "127.0.0.1"
    port = 3452
    buffer_time = 1024
    
    print("Initializing")
    # server socket
    serv_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        serv_socket.bind((host, port))
    except socket.error:
        print("Unable to create socket")

    print("Socket created")
    # listen for up to 5 connections at once
    serv_socket.listen(5)

    # write to file msg
    print("Awaiting connections...")
  
    while True:

        # make a queue that adds users to the right, pops the left
        # makes each one popped wait 5 seconds before being acticvated
        # make connection with clients
        conn, addr = serv_socket.accept()
        
        print("Connection from: %s" % addr[0])
            
        start_new_thread(threader, (conn,))

    serv_socket.close()


if __name__ == '__main__':
    Main()

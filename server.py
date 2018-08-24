""" Server side host in Server-Client port connection
                this program receives a message and sends it back in full caps to confirm that it
                received the message"""
import socket
from _thread import *
from pySql import PySQLTrans

# threaded connection

def threader(conn):
    while True:

        data = conn.recv(1024).decode()
        # if data not received
        if not data:
            print("no data received.")
            break

        # convert data into a str to be documented
        temp_str = str(data)
        comp_name, num_files = temp_str.split(": ")

        # transfer to SQL Server
        db_acct = PySQLTrans(comp_name, num_files)
        db_acct.sql_db_upload()
        # Grab data
        report = db_acct.sql_db_dowload()

        with open('report_dialogue.txt', 'r') as file:
            html_reader = file.read()

        # set up HTML Script
        html_wrkspc = (
            '<!DOCTYPE html>\n'
            '<html>\n'
            '<head>\n'
            '<meta http-equiv="refresh" content="5">\n'
            '<style>\n'
            'table {\n'
            '\tfont-family: Anevir, sans-serif;\n'
            '\tborder-collapse: collapse;\n'
            '\twidth: 100%;\n'
            '}\n'
            'td, th {\n'
            '\tborder: 1px solid #000000;\n'
            '\ttext-align: middle;\n'
            '\tpadding: 5px;\n'
            '}\n'
            'tr:nth-child(even) {\n'
            '\tbackground: #C1C1C1;\n'
            '}\n'
            '</style>\n'
            '</head>\n'
            '<body>\n\n'
            '<div style="background-color:#2980B9;color:black;padding:10px;">'
            '<h2 align="center">Dashboard</h2>\n'
            '</div>\n'
            '<table>\n'
            '  <tr>\n'
            '\t<th>Machine</th>\n'
            '\t<th>Files in folder</th>\n'
            '\t<th>Time Stamp</th>\n'
            '\t<th>Time Since Check-in</th>\n'
            '  </tr>\n' + html_reader + '</table>\n'
            '</body>\n'
            '</html>\n')

        with open("report.html", "w") as file:
            file.write(html_wrkspc)


def Main():
    host = socket.gethostname()
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
        # make connection with clients
        conn, addr = serv_socket.accept()

        print("Connection from: %s" % addr[0])

        start_new_thread(threader, (conn,))

    serv_socket.close()

if __name__ == '__main__':
    Main()

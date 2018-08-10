""" Server side host in Server-Client port connection
                this program receives a message and sends it back in full caps to confirm that it
                received the message"""
import socket
import sys
import traceback
from _thread import *
import threading
from csv import DictWriter


# threaded connection
def threader(conn, clients):
    comp_li = []
    full_list = []
    mock_file = open('data.csv', 'w')
    while True:

        data = conn.recv(1024).decode()
        # if data not received
        if not data:
            print("no data received.")
            break

        # convert data into a str to be documented
        temp_str = str(data)
        comp_name, num_files = temp_str.split(": ")

        if comp_name not in comp_li:
            comp_li.append(comp_name)

        for client, name in zip(clients, comp_li):
            print (client, name)


        with open("data.csv", "r+") as file:
            headers = ["Name", "Num"]
            csv_writer = DictWriter(file, fieldnames=headers)
            csv_writer.writeheader()
            csv_writer.writerow({
                "Name": comp_name,
                "Num": num_files,
            })

        with open("data.csv", "r+") as file:
            newText = file.read()

            if comp_name in open('data.csv').read():
                print("t-1")
                newText = newText.replace(comp_name, 'Dave')

            if 'Bob' in open('data.csv').read():
                print("t-2")

        with open("data.csv", "w") as file:
            file.write(newText)



        html_wrkspc = ("<html>\n<body>\n<h1>The Report</h1>\n<p>" + temp_str + "</p>\n</body>\n</html>")

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
    print("writing data to file ...")
    clients = []
    while True:
        # make connection with clients
        conn, addr = serv_socket.accept()
        clients.append(addr[0])
        print("Connection from: %s" % addr[0])

        # first arg is function to call, second is tuple cont pos
        start_new_thread(threader, (conn, clients))
        print(clients)

    serv_socket.close()


if __name__ == '__main__':
    Main()

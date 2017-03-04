import json
import os
import select
import socket
import time

def receive(conn):
    data = b''
    word = b''
    while word != b'\x04':
        data += word
        word = conn.recv(1)
    message = data.decode('utf-8')
    message = json.loads(message)
    return message

def send(msg, socket):
    message = json.dumps(msg)
    message = message + '\x04'
    socket.sendall(message.encode('utf-8'))

def messageInSocket(s):
    read_list, _, _ = select.select([s], [], [], 0)
    if read_list == []:
        return False
    else:
        return True

robot_sender = 'robot'
robot_receiver = 'robot2'
HOST = os.environ.get("EDUMORSE_ROBOT_HOST")
PORT = int(os.environ.get("EDUMORSE_ROBOT_PORT"))

if __name__ == '__main__':
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        send(robot_sender, s)
        start = ''
        while 'Start' not in start:
            start = receive(s)
            print(start)

        text = 'Hello from robot!'
        message = {robot_receiver : text}
        send(message, s)

        time.sleep(0.6)
        text = 'Hello again!'
        message = {robot_receiver : text}
        send(message, s)

        while not messageInSocket(s):
            pass
        data = receive(s)
        msg = data['robot']
        print(msg)

        s.close()

import message
from threading import Thread
import threading
import socket
import pickle
import copy
import time
import os
from waiting import wait

class MyThread (threading.Thread):

    def __init__(self, pro, type):

        threading.Thread.__init__(self)
        self.pro = pro
        self.type = type
        # self.name = name
        # self.counter = counter

    def run(self):
        send_request(self.pro, self.type)


def send_request(pro, type):

    if type == 2 or type == 3 or type == 4:
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        if type == 4 or type == 3:
            tcp.connect((host, p[pro - 1].port))
            m1 = message.Message(pro, type)
        else:
            tcp.connect((host, p[pro.lider - 1].port))
            m1 = message.Message(pro.pid, type)
        m_dumped = pickle.dumps(m1)
        x = tcp.send(m_dumped)

        tcp.close()



    elif type == 1:
        for process in p:
            tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            tcp.connect((host, process.port))
            m1 = message.Message(pro.pid, type)
            m_dumped = pickle.dumps(m1)
            x = tcp.send(m_dumped)
            tcp.close()
    elif type == 0:
        for process in p:
            if pro.pid < process.pid:
                tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                tcp.connect((host, process.port))
                m1 = message.Message(pro.pid, type)
                m_dumped = pickle.dumps(m1)
                x = tcp.send(m_dumped)
                tcp.close()



class MyThread2 (threading.Thread):

    def __init__(self, pr):

        threading.Thread.__init__(self)
        self.process = pr
        # self.name = name
        # self.counter = counter

    def run(self):
        Process.receive(self.process)

class MyThread3 (threading.Thread):

    def __init__(self, var):

        threading.Thread.__init__(self)
        self.var = var
        # self.name = name
        # self.counter = counter

    def run(self):
        Process.mtime(self.var)


class Process:

    def __init__(self, pid, host, port):
        self.pid = pid
        self.lider = 5
        self.failed = 0
        self.candidato = 0
        self.sender = 0
        self.sender2 = 0
        self.process_list = []
        self.host = host
        self.port = port
        thread2 = MyThread2(self)
        thread2.start()

    def set_process_list(self, process_list):
        self.process_list = process_list

    def set_failed(self, failed):
        self.failed = failed

    def set_alive(self):
        self.failed = 0
        thread10 = MyThread(self, 0)
        thread10.start()
        self.candidato = 1


    def tcp_accept(self, tcp):
        return tcp.accept()

    def receive(self):
        tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        orig = (self.host, self.port)
        tcp.bind(orig)
        tcp.listen(1)


        while True:

                try:
                    tcp.settimeout(10)
                    con, cliente = self.tcp_accept(tcp)
                except socket.timeout:
                    if self.sender:
                        self.sender = 0
                        thread4 = MyThread(self, 0)
                        thread4.start()
                    if self.candidato:
                        self.candidato = 0
                        thread5 = MyThread(self, 1)
                        thread5.start()
                except:
                    raise
                else:

                    if not self.failed:

                        while True:
                            msg = con.recv(1024)
                            if msg:
                                msg_loaded = pickle.loads(msg)
                                new_m = copy.copy(msg_loaded)

                            if not msg: break

                        con.close()
                        t = time.time()

                        if new_m.type == 0:
                            if new_m.pid < self.pid:
                                thread7 = MyThread(new_m.pid, 3)
                                thread7.start()

                                #########################

                                thread3 = MyThread(self, 0)
                                thread3.start()
                                self.candidato = 1
                        elif new_m.type == 1:
                                self.lider = new_m.pid
                                print("Eu processo ", self.pid, " concordo em ser liderado pelo processo ", self.lider)
                                # # print(self.sender)
                                time.sleep(5)
                                if self.sender2:
                                    print("ERROU")
                                    thread11 = MyThread(self, 2)
                                    thread11.start()
                        elif new_m.type == 2:
                                thread6 = MyThread(new_m.pid, 4)
                                thread6.start()
                                print("Lider ", self.lider, " recebeu a mensagem do processo ", new_m.pid)


                        elif new_m.type == 3:
                                self.candidato = 0
                                print("Mensagem OK entregue para", self.pid)

                        elif new_m.type == 4:
                                self.sender = 0
                                self.sender2 = 0




host = '192.168.0.101'
process_number = 1
p = [Process(process_number, host, 5000),
     Process(process_number + 1, host, 5001),
     Process(process_number + 2, host, 5002),
     Process(process_number + 3, host, 5004),
     Process(process_number + 4, host, 5005)]

for proc in p:
    proc.set_process_list(p)


print("1 - Enviar Mensagem")
print("2 - Sair")
print("3 - Falhar líder")
print("4 - Recuperar processo")
option = input()

while True:


    if option == '1':
        print("Qual processo enviará a mensagem?")
        sender = int(input())
        p[sender-1].sender = 1
        p[sender - 1].sender2 = 1
        thread1 = MyThread(p[sender-1], 2)
        thread1.start()
    if option == '3':
        p[p[0].lider - 1].set_failed(1)
        print("Líder ", p[0].lider, " falhou")
    if option == '4':
        print("Digite o processo que deseja recuperar")
        sender = int(input())
        p[sender-1].set_alive()
    elif option == '2':
        os._exit(0)

    print("1 - Enviar Mensagem")
    print("2 - Sair")
    print("3 - Falhar líder")
    print("4 - Recuperar processo")
    option = input()



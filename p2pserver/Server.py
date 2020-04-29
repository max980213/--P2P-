import threading
import socket
import os
import sys

#hostip='192.168.1.101' # 需要一个主机充当服务器

cmdport=12005 # 服务器的命令监听端口
fileport=12006 #

#客户端的两个端口
InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件端口

BUFSIZE=1024
encoding='utf-8'
filename='SharedFile.xml'

def broke(addr):
    print('网友 %s 断开了连接！在共享文档中删除了该ip的项！' % addr[0])
    file=open(filename,'r')
    lines=file.readlines()
    file.close()
    file=open(filename,'w')
    for line in lines:
        if addr[0] not in line:
            file.write(line)
    file.close()
    

class datareader(threading.Thread):
    def __init__(self,client,addr):
        threading.Thread.__init__(self)
        self.client=client
        self.addr=addr
    def run(self):
        while True:
            try:
                cmd=self.client.recv(BUFSIZE).decode(encoding).split(' ')
            except:
                broke(self.addr)
                self.client.close()
                break
            if cmd[0]=='update':
            # 向所有主机广播，发出更新指令，将更新后的列表返回并写入
                print('接受了来自 %s 的更新！' % self.addr[0])
            elif cmd[0]=='get':
                # 向新来的主机发送已有的文件列表，这样新来的主机接入的时候直接发get，或者多添一个get命令
                try:
                    sock=socket.socket()
                    sock.connect((self.addr[0],FileListenerPort))
                    file=open(filename,'r')
                    for line in file:
                        print(line)
                        sock.send(line.encode(encoding))
                    file.close()
                    sock.close()
                except:
                    broke(self.addr)
                    self.client.close()
                    break
            elif cmd[0]=='download':
                print()
            #'''
            #elif cmd[0]=='exit':            # 所以在服务器端判断也没啥用了...
            #    print('Bye bye!')
            #    # break  客户端断开连接后会死循环接收空字符串，这里根本break不出去
            #'''
            else:
                if cmd==['']:
                    break
                print('暂时还没开发这个指令！')
                print(cmd)
                print(self.addr)
        broke(self.addr)
        self.client.close()
            

class datalistener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock=socket.socket()
        self.sock.bind(('0.0.0.0',cmdport))
        self.sock.listen(0)
    def run(self): #该线程用来监听#更新#命令,暂时只有更新命令
        while True:
            client,addr=self.sock.accept()  # 对于返回值，client是一个socket()对象，addr是一个元组，包含ip和端口
            print(addr)
            datareader(client,addr).start()
        
class filelistener(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.sock=socket.socket()
        self.sock.bind(('0.0.0.0',fileport))
        self.sock.listen(0)
    def run(self):
        while True:
            client,addr=self.sock.accept()
            filewriter(client,addr).start()

class filewriter(threading.Thread):
    def __init__(self,client,addr):
        threading.Thread.__init__(self)
        self.client=client
        self.addr=addr
    def run(self):
        if os.path.isfile(filename):
            file=open(filename,'r')
            lines=file.readlines()
            file.close()
            file=open(filename,'w')
            for line in lines:
                if self.addr[0] not in line:
                    file.write(line)
            file.close()   #先把共享目录里得来的该ip得项删掉，再接收新的
        file=open(filename,'a')
        while True:
            line=self.client.recv(BUFSIZE)
            if not line:
                break
            file.write(line.decode(encoding))
        file.close()
            
            
            

def main():
    if os.path.isfile(filename):
        os.remove(filename)  # 每次运行服务器先把共享文件删掉
    cmdlistener=datalistener()
    cmdlistener.start()
    _filelistener=filelistener()
    _filelistener.start()
    print('开始监听了！')

        

if __name__=='__main__':
    main()

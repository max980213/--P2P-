import socket
import threading
import listener
import main
import os

hostip="192.168.1.101"
InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件端口
servercmdport=12005
serverfileport=12006
encoding='utf-8'
BUFSIZE=1024
sharedfilename='SharedFile.xml'

class msgsend(threading.Thread):
    def __init__(self,sock):
        threading.Thread.__init__(self)
        self.sock=sock
    def run(self):
        while True:
            inputcmd=input() # 会生成列表
            inputlist=inputcmd.split(' ')
            cmd=inputlist[0]
            if cmd=='update':
                main.updatetoserver()  #向服务器发送更新后得表，各主机需手动获取（用get指令）
                print('已更新！请重新获取！')
            elif cmd=='download':
                flag=0
                filename=inputlist[1]
                file=open('PublicSharedFile.xml','r')
                for line in file:
                    rf=line.split(' ')
                    if rf[0]==filename:
                        flag=1
                        ip=rf[1]  #文件所在ip
                        sock=socket.socket()
                        sock.connect((ip,InstructionListenerPort)) #连接对方主机端口
                        sock.send(inputcmd.encode(encoding)) #将指令发送出去
                        sock.close()
                        listener.FileListener(filename).start() #启动文件监听线程，准备接收文件
                        break
                if flag==0:
                    print('该文件不存在！请更新列表!')
                
            elif cmd=='exit':
                print('Bye Bye!')
                self.sock.close()#close()方法居然不会立即释放socket！！！必须得先用shutdown
                break
            elif cmd=='get':
                listener.FileListener(sharedfilename).start() #准备接收共享文件列表
            else:
                print('命令不合法!')
                continue  # 接收下一次输入
                #sock.send(cmd.encode(encoding))
            try:
                self.sock.send(cmd.encode(encoding))
            except:
                print('连接已关闭')
                self.sock.close()
                break
        #exit()



class filesend(threading.Thread):  # 文件发送线程
    def __init__(self,ip,filename):
        threading.Thread.__init__(self)
        self.port=FileListenerPort # 指定的文件接收端口
        self.sock=socket.socket()
        self.ip=ip
        self.filename=filename
    def run(self):
        if os.path.isfile(self.filename): # 如果该文件存在
            try:
                self.sock.connect((self.ip,self.port))  # 先直接连吧
                # size=os.stat(filename).st_size  # 获取文件大小
                file=open(self.filename,'r')  # 以二进制读
                for line in file:
                    try:
                        self.sock.send(line.encode(encoding))  # 发送文件数据
                    except:
                        print('对方已关闭连接！')
                        break
                file.close()
                self.sock.close()
            except:
                print('对方已关闭连接！')
                self.sock.close()
        else:
            self.sock.connect((self.ip,self.port))
            self.sock.send(('gaiwenjianbucunzai!').encode(encoding))
            self.sock.close()
            print('文件不存在咯！')
        


















        

import socket
import threading

hostip="192.168.1.101"
InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件端口
encoding='utf-8'
BUFSIZE=1024

class msgsend(threading.Thread):
    def __init__(self,ip):
        threading.Thread.__init__(self)
        self.port=InstructionListenerPort
        self.ip=ip
        self.sock=socket.socket()
    def run(self):
        print("正在建立连接！！")
        try:
            self.sock.connect((ip,port))
            print("连接成功！下面开始输入发送内容!")
            str=input()
            if(str):
                data=str.encode(encoding)
                try:
                    self.sock.send(data)
                except:
                    print('连接已关闭')
                    self.sock.close()
        except:
            print("连接失败")
            self.sock.close()


class filesend(threading.Thread):  # 文件发送线程
    def __init__(self,ip,filename):
        threading.Thread.__init__(self)
        self.port=FileListenerPort # 指定的文件接收端口
        self.sock=socket.socket()
    def run(self):
        if os.path.isfile(filename): # 如果该文件存在
            try:
                self.sock.connect((ip,self.port))  # 先直接连吧
                # size=os.stat(filename).st_size  # 获取文件大小
                file=open(filename,'rb')  # 以二进制读
                for line in file:
                    try:
                        self.sock.send(line)  # 发送文件数据
                    except:
                        print('对方已关闭连接！')
                        break
                f.close()
                self.sock.close()
            except:
                print('建立连接失败！')
                self.sock.close()
        else:
            print('该文件不存在！')# 应该将不存在的信息返回
        


















        

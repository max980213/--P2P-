import socket
import threading
import filecreater #自定义包
import os

InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件

encoding='utf-8'
BUFSIZE=1024


class InstructionReader(threading.Thread): # 对接收到的消息进行处理
    def __init__(self,client):
        threading.Thread.__init__(self)
        self.client=client
    def run(self):
        while True:
            try:  # 也可用 if data:来实现判断是否有连接
                data=self.client.recv(BUFSIZE)  
            except:
                print("连接已被对方关闭")
                break
            if data:
                cmdlist=data.decode(encoding).split(' ')  # 以空格分隔
                cmd=cmdlist[0]
                if cmd=='download':     # if-elif中间的函数体不可为空，加一句注释也不行，会报错：要求缩进
                    # 将本机某一所需文件发给对方
                    print('a')
                elif str=='update':
                    filecreater.UpdateXMLfile()
                    # 然后将更新好的数据重新返回到服务器
                elif str=='connect':
                    print('c')
                    ## 接收某一主机的直连请求
                print(str)
            else:
                break
                

class InstructionListener(threading.Thread):  # 利用继承线程类，来创建线程，该线程用来监听命令
    def __init__(self):
        threading.Thread.__init__(self)
        self.port=InstructionListenerPort
        #self.sock=socket.socket(socket.AF_INET,socket.SOCK_STREAM) # TCP
        self.sock=socket.socket() # 好像直接初始化也行
        self.sock.bind(("0.0.0.0",self.port)) # 与命令接收端口绑定
        self.sock.listen(0)
    # 重写run方法作为线程执行体
    def run(self):   # 监听
        print("开始监听！")
        while True:
            client,cltadd=self.sock.accept() # 接收连接请求
            print('收到来自 %s 的连接！' % cltadd[0])
            InstructionReader(client).start()  # 调用另一个线程处理接受的数据



#整合在一起，重写这部分代码
class FileListener(threading.Thread):  # 监听文件端口
    def __init__(self,filename):
        threading.Thread.__init__(self)
        self.filename=filename
        self.port=FileListenerPort
        self.sock=socket.socket()
        self.sock.bind(('0.0.0.0',self.port))
        self.sock.listen(0) #开始监听该端口
    def run(self):
        print("开始监听文件！")
        wfile=open(filename,'w')
        while True:
            try:
                client,cltadd=self.sock.accept() #接收到了连接
                while True:
                    line=client.recv(BUFSIZE)  # 多次接收
                    if line:
                        wfile.write(line)
                    else:
                        flag=1
                        break
                if flag:
                    print('接收完毕')
                    break
            except:
                print('连接失败！')
                wfile.close()
                os.remove(filename)
                break
        wfile.close()
if __name__=='__main__':
    listener=InstructionListener()
    listener.start()
            
                    
            
            
        


        

#if __name__ == '__main__':  #这句话的意思是，如果以上脚本是直接执行就执行该函数，如果是导入到别的脚本里就不执行

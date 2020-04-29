import socket
import threading
import sys
import os
import listener
import filecreater
import sender
import tkinter
from tkinter import *

hostip="192.168.1.101"
InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件端口
servercmdport=12005
serverfileport=12006
sharedfilename='SharedFile.xml'

encoding='utf-8'
BUFSIZE=1024


def updatetoserver():
    filecreater.UpdateXMLfile()  # 先更新本地
    sock=socket.socket()
    sock.connect((hostip,serverfileport))
    file=open(sharedfilename,'r')
    for line in file:
        line=line.encode(encoding)
        sock.send(line)
    file.close()
    sock.close()




                                  
# 图形界面！
# 后缀为pyw不会显示后面的cmd界面

class Application(Frame):  # 继承于Frame类
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master.title('P2P File Downloading System') # 标题
        self.pack()
        self.outputbox=Text(self,width=75,height=20) # 这里的pad指该空间内部的边框
        self.outputbox.pack(padx=15,pady=15) # 这个才是与外部框架的边框
        self.inputbox=Text(self,width=75,height=3)
        self.inputbox.pack(pady=10)
        self.ButtonGet=Button(self,text='Get',height=2,width=10,command=self.get)
        self.ButtonUpdate=Button(self,text='Update',height=2,width=10,command=self.update)
        self.ButtonDownload=Button(self,text='Download',height=2,width=10,command=self.download)
        self.ButtonClear=Button(self,text='Clear',height=2,width=10,command=self.clear)
        self.ButtonExit=Button(self,text='Exit',height=2,width=10,command=self.exit)  # exit 也可
        self.ButtonGet.pack(side=LEFT,expand=YES)
        self.ButtonUpdate.pack(side=LEFT,expand=YES)
        self.ButtonDownload.pack(side=LEFT,expand=YES)
        self.ButtonClear.pack(side=LEFT,expand=YES)
        self.ButtonExit.pack(side=LEFT,expand=YES)
        # 初始化界面的各控件
        try:
            self.sock=socket.socket()
            self.sock.connect((hostip,servercmdport))  # 一直连着，不让他断
            updatetoserver()  #连接后先更新本地，再向服务器更新
        
            self.outputbox.insert(tkinter.END,'已连接服务器！现在可以进行通信了\n\n')
            self.outputbox.see(tkinter.END)
            self.outputbox.update()   # 该两行作用是保持显示最新的一行

        
        except:
            self.outputbox.insert(tkinter.END,'连接服务器失败！请检查服务器是否打开并重启软件！\n\n')
            
        self.threadsbegin()
    def threadsbegin(self):  # 初始化各线程
        instructionlistener=listener.InstructionListener()
        instructionlistener.setDaemon(True)
        instructionlistener.start()   # 开始监听命令端口
        #inssend=sender.msgsend(self.sock)
        #inssend.setDaemon(True)
        #inssend.start()  # 这个线程退出后，程序不会退出是因为上面两个线程还在跑
                                  # 尝试将监听命令的线程放到该线程里开始
                                  # 并不好用
        
    def get(self):
        self.sock.send('get'.encode(encoding))
        filelisten=listener.FileListener(self,sharedfilename)
        filelisten.setDaemon(True)
        filelisten.start() #启动文件监听线程，准备接收文件

    def update(self):
        try:
            updatetoserver()
            self.outputbox.insert(tkinter.END,'更新成功！请重新获取！\n\n')
            self.outputbox.see(tkinter.END)
            self.outputbox.update()
        except:
            self.outputbox.insert(tkinter.END,'更新失败！请检查与服务器的连接！\n\n')
            self.outputbox.see(tkinter.END)
            self.outputbox.update()

    def download(self):
        flag=0
        filename=self.inputbox.get("1.0","end").rstrip('\n')
        if os.path.isfile('PublicSharedFile.xml'):
            file=open('PublicSharedFile.xml','r')
            for line in file:
                rf=line.split(' ')
                if rf[0]==filename:
                    ip=rf[1].rstrip('\n')  #文件所在ip
                    if ip==socket.gethostbyname(socket.gethostname()):
                        self.outputbox.insert(tkinter.END,'找到了一个在本地的文件，不可以自己下载自己噢，将继续寻找\n\n')
                        self.outputbox.see(tkinter.END)
                        self.outputbox.update()
                        continue
                    flag+=1
                    sock=socket.socket()
                    sock.connect((ip,InstructionListenerPort)) #连接对方主机端口
                    if flag>1: # 若有重名的文件，从第二个开始标记来源
                        sock.send(('download '+filename+' '+ip).encode(encoding)) #将指令发送出去
                        sock.close()
                        listener.FileListener(self,filename).start() #启动文件监听线程，准备接收文件
                    else:
                        sock.send(('download '+filename).encode(encoding)) #将指令发送出去
                        sock.close()
                        listener.FileListener(self,filename).start() #启动文件监听线程，准备接收文件
            if flag==0:
                self.outputbox.insert(tkinter.END,'该文件不存在！请检查输入或更新列表!\n\n')
                self.outputbox.see(tkinter.END)
                self.outputbox.update()
        else:
            self.outputbox.insert(tkinter.END,'请先获取共享文件目录（Press Get Button)!\n\n')
            self.outputbox.see(tkinter.END)
            self.outputbox.update()

    def clear(self):
        self.outputbox.delete(1.0,tkinter.END)

    def exit(self):
        sys.exit()







if __name__ == '__main__':
    app=Application()
    app.mainloop()

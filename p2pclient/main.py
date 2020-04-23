import socket
import threading
import listener
import filecreater
import sender

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




def main():
    sock=socket.socket()
    sock.connect((hostip,servercmdport))  # 一直连着，不让他断
    updatetoserver()  #连接后先更新本地，再向服务器更新
    instructionlistener=listener.InstructionListener()
    instructionlistener.start()   #连接服务器并开始监听命令端口
    print('已连接服务器！现在可以进行通信了')
    print('请输入操作的指令!')
    sender.msgsend(sock).start()  # 这个线程退出后，程序不会退出是因为上面两个线程还在跑
                                  # 尝试将监听命令的线程放到该线程里开始
                                  # 并不好用







if __name__ == '__main__':
    main()

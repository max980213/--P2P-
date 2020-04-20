import socket
import threading
import listener
import filecreater
import sender

hostip="192.168.1.101"
InstructionListenerPort=34525 # 指定监听端口
FileListenerPort=34526  # 接收文件端口
encoding='utf-8'
BUFSIZE=1024

def main():
    sock=socket.socket()
    sock.connect((hostip,InstructionListenerPort))
    #instructionlistener=listener.InstructionListener()
    #instruction.start()   #连接服务器并开始监听命令端口
    print('已连接服务器！现在可以进行通信了')
    print('请输入操作的指令!')
    while True:
        inputlist=input().split(' ')  # 会生成列表
        cmd=inputlist[0]
        if cmd=='update':
            filecreater.UpdateXMLfile()
            # 并向服务器发送更新指令
        elif cmd=='download':
            filename=inputlist[1]
            #向服务器发送下载命令，服务器返回ip，再建立连接下载
        elif cmd=='exit':
            print('Bye Bye!')
            exit()
        else:
            print('命令不合法!')
        





if __name__ == '__main__':
    main()

# 用来生成共享的文件目录和在网络内的用户信息

import sys
import os
import socket  # 获取本机ip用得到
import xml.dom.minidom


# 获取本地文件共享列表
def LocalFileList():
    fileList=os.listdir(os.getcwd()) # os.listdir(path) 返回该目录下所有文件和文件夹列表
    for isfile in fileList:
        # 判断是文件还是目录
        if os.path.isfile(isfile):
            continue
        else:
            fileList.remove(isfile)
    return fileList  # 返回列表


# 生成共享文件xml文档
# 插入数据暂时没想好怎么实现，干脆直接生成新的
# 如果在不同主机里文件名重复..

def GenXMLfile(fileList):
    #cwd=os.getcwd()  # 当前路径
    xmlfilename='SharedFile.xml'
    fileID=1
    xmlfile=open(xmlfilename,'w')  # a的含义是追加写入，不存在则创建，w是覆盖掉原来的重新写入
    hostname=socket.gethostname()
    ipaddr=socket.gethostbyname(hostname)  #获取ip地址，是真的地址，会输出的那种，类型是str
    #print('<FileList>',file=xmlfile)
    for afile in fileList:
        filestr=afile + ' ' + ipaddr
        print(filestr,file=xmlfile)
        fileID+=1
    #print('</FileList>',file=xmlfile)
    xmlfile.close()

#GenXMLfile(LocalFileList())

#解析xml文档，生成共享文件列表
def ParsFileXML():
    FileList=[]
    file=open('SharedFile.xml','r')
    dic=xml.dom.minidom.parse(file)
    #print(dic)
    FileTagList=dic.getElementsByTagName('File')
    #print(FileTagList)
    for aFileTag in FileTagList:
        #FileID=aFileTag.getAttribute('FileID')
        FileName=aFileTag.getAttribute('FileName')
        #FileDict[int(FileID)]=FileName
        FileList.append(FileName)
    file.close()
    return FileList

#FileList=ParsFileXML()
#print(FileList)
#以上均没有问题

# 更新xml文档
def UpdateXMLfile():
    GenXMLfile(LocalFileList())

if __name__=='__main__':
    UpdateXMLfile()

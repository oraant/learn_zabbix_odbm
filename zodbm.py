# coding:utf-8

import sys,os,time
import socket

def daemonize(stdin= '/dev/null',stdout= '/dev/null', stderr= 'dev/null'):
    '''Fork当前进程为守护进程，重定向标准文件描述符
        （默认情况下定向到/dev/null）
    '''
    #Perform first fork.
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0)  #first parent out
    except OSError, e:
        sys.stderr.write("fork #1 failed: (%d) %s\n" %(e.errno, e.strerror))
        sys.exit(1)

    #从母体环境脱离，更改路径，更改默认权限，以及创建新的SESSION（为了摆脱控制终端，防止响应原SESSION的sighup，sigint等信号）
    os.chdir("/")
    os.umask(0)
    os.setsid()

    #执行第二次fork，防止建立了新SESSION的进程（已成为无终端的会话领导）打开新的终端。
    try:
        pid = os.fork()
        if pid > 0:
            sys.exit(0) #second parent out
    except OSError, e:
        sys.stderr.write("fork #2 failed: (%d) %s]n" %(e.errno,e.strerror))
        sys.exit(1)

    #进程已经是守护进程了，重定向标准文件描述符
    for f in sys.stdout, sys.stderr: f.flush()
    si = file(stdin, 'r')
    so = file(stdout,'a+')
    se = file(stderr,'a+',0)
    os.dup2(si.fileno(), sys.stdin.fileno())
    os.dup2(so.fileno(), sys.stdout.fileno())
    os.dup2(se.fileno(), sys.stderr.fileno())

def start_server(sock='/tmp/zodbm.sock'):
    '''开启Socket Server服务，监听sock通信文件
    '''
    #开启监听服务
    server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    if os.path.exists(sock):
        os.unlink(sock)
    server.bind(sock)
    server.listen(5)

    #处理请求
    while True:
        connection, address = server.accept()
        req = connection.recv(1024)
        if req == 'stop':
            break
        else:
            res = req#.split()
            connection.send(res)
    connection.send('ZODBM Server Has Stoped')
    connection.close()

    
if __name__ == '__main__':
    daemonize('/dev/null','/root/zabbix-odbm/log','/root/zabbix-odbm/log')
    start_server()

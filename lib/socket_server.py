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
            res = 'ZODBM Server has stoped'
            break
        elif req == 'status':
            res = 'ZODBM Server is running'
            connection.send(res)
        else:
            res = req#.split()
            connection.send(res)

    connection.send(res)
    connection.close()
    os.unlink(sock)
    exit(0)

def get_config():
    '''从配置文件中获取配置
    '''
    import ConfigParser
    config = ConfigParser.ConfigParser()
    path = sys.path[0]
    config.read(path + "/conf/zodbm.conf")

    #读取配置
    c_log_file  = config.get("base","log_file")
    c_log_level = config.get("base","log_level")
    c_sock_file = config.get("base","sock_file")

    #配置为空时的处理方式
    log_file  = c_log_file  if c_log_file  != '' else path + "/log/zodbm.log"
    log_level = c_log_level if c_log_level != '' else 3
    sock_file = c_sock_file if c_sock_file != '' else path + "/lib/zodbm.sock"

    configs = {"log_file":log_file,"log_level":log_level,"sock_file":sock_file}
    return configs

def verify_passwd():
    '''
    '''
    import verify as v
    verify = v.Verify()

    print '\n  The encrypted text is:'
    print '  \033[1;31;31m' + verify.generate_code() + '\033[0m'
    passwd = raw_input('  Please input password for zodbm:')
    return verify.verify_passwd(passwd)

def main():
    if verify_passwd():
        print '  Verify \033[4mpassed\033[0m,starting zodbm daemon process.\n'
    else:
        print '  Verify \033[4mfailed\033[0m,please contact developers in \033[4mChinaITSoft\033[0m.\n'
        exit(1)
    config = get_config()
    daemonize('/dev/null',config["log_file"],config["log_file"])
    start_server(config["sock_file"])

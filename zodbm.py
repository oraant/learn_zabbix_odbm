#coding:utf-8

import socket
import os,sys

def print_help():
    '''打印帮助信息'''

    print ''
    print '  Syntax should be like this:\n'
    print '    1. python zodbm.py <start|stop|status|restart>'
    print '    2. python zodbm.py <message>'
    print ''
    print '  Exemples:\n'
    print '    python zodbm.py start'
    print '    python zodbm.py stop'
    print '    python zodbm.py system/oracle@192.168.10.10:1521/orcl physical_read'
    print ''

def get_config():
    '''#获取基本配置'''

    global path, log_file, config_file
    global sock_file, sock_links

    path = sys.path[0]
    log_file = path+'/log/server.log'
    config_file = path+'/conf/server.conf'
    sock_file = path+'/lib/server.sock'
    sock_links = 5

def verify_argv():
    '''判断有无参数'''

    try:
        req = sys.argv[1]
        return True
    except Exception as e:
        return e

if __name__ == '__main__':
    '''主要业务处理'''

    if verify_argv() != True:
        print verify_argv()
        print_help()
        exit(1)

    get_config()
    req = sys.argv[1]

    from lib.SocketServer import SocketServer
    socket_server = SocketServer(sock_file,sock_links,config_file,log_file)

    if req == 'start':
        print socket_server.server_start()
    elif req == 'stop':
        print socket_server.server_stop()
    elif req == 'status':
        print socket_server.server_status()
    elif req == 'restart':
        print socket_server.server_restart()
    else:
        req = str(sys.argv[1:])
        print socket_server.server_send(req)

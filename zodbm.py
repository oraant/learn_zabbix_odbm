#coding:utf-8

import socket
import os,sys
import ConfigParser
from lib.socket_server import *

def print_help():
    print ''
    print '  Did not found any parameter.Syntax should be:\n'
    print '    1. python zodbm.py <start|stop|status|restart>'
    print '    2. python zodbm.py <tnslink> <data_dict> <parameter>'
    print ''
    print '  Exemple:\n'
    print '    python zodbm.py start'
    print '    python zodbm.py stop'
    print '    python zodbm.py system/oracle@192.168.10.10:1521/orcl sysstat physical_read'
    print ''

def get_config():
    '''#获取配置文件以及socket文件的配置'''
    path = sys.path[0]
    config = ConfigParser.ConfigParser()
    config.read(path + "/conf/zodbm.conf")

    c_sock_file = config.get("base","sock_file")
    global sock_file
    sock_file = c_sock_file if c_sock_file != '' else path + "/lib/zodbm.sock"    

def send_msg(req):
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    try:
        client.connect(sock_file)
        client.send(req)
        res = client.recv(1024)
    except socket.error:
        res = 'ZODBM Server is not running.'
    finally:
        client.close()
    return res

def start():
    res = send_msg('status')
    if res == 'ZODBM Server is not running.':
        print 'Starting ZODBM Server:'
        main()
    else:
        print res
        exit(3)

def stop():
    print send_msg('stop')

def status():
    print send_msg('status')

def restart():
    stop()
    start()

if __name__ == '__main__':

    get_config()
    operation = {'start':start,'stop':stop,'status':status,'restart':restart}

    try:
        req = sys.argv[1]
        if req in ['start','stop','status','restart']:
            operation.get(req)()
        else:
            req = sys.argv[1] +';'+ sys.argv[2] +';'+ sys.argv[3]
            print send_msg(req)
    except IndexError:
        print_help()
        exit(1)
    except Exception as e:
        print e
        exit(2)

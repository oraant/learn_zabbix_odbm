#coding:utf-8

import socket
import os,sys
import ConfigParser

def __parse_args():
    '''根据参数获取要发送的内容'''
    try:
        if sys.argv[1] == 'stop':
            req = 'stop'
        else:
            req = sys.argv[1] +';'+ sys.argv[2] +';'+ sys.argv[3]
        return req
    except IndexError:
        print ''
        print '  Did not found any parameter.Syntax should be:'
        print '  1. python picker.py stop'
        print '  2. python picker.py tnslink data_dict parameter'
        print ''
        print '  Exemple:'
        print '  python picker.py system/oracle@192.168.10.10:1521/orcl sysstat physical_read'
        print ''
        exit(1)
    except Exception as e:
        print e
        exit(2)

def __get_config():
    '''#获取配置文件以及socket文件的配置'''
    path = sys.path[0]
    config = ConfigParser.ConfigParser()
    config.read(path + "/conf/zodbm.conf")

    c_sock_file = config.get("base","sock_file")
    sock_file = c_sock_file if c_sock_file != '' else path + "/lib/zodbm.sock"    
    return sock_file


if __name__ == '__main__':

    req = __parse_args()
    sock_file = __get_config()
    client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)

    try:
        client.connect(sock_file)
        client.send(req)
        print client.recv(1024)
    except socket.error:
        print 'Server is not running.'
    finally:
        client.close()

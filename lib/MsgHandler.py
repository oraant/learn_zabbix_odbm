# coding:utf-8

import os,sys

class MsgHandler:

    def __init__(self,config_file):
        self.config_file = config_file

    def __help(self):
        print ''
        print '  Syntax should be like this:'
        print '    1. python zodbm.py <target> <key>'
        print '    2. python zodbm.py close <target>'
        print '    3. python zodbm.py closeall'
        print ''
        print '  Examples:'
        print '    1. python zodbm.py system/oracle@192.168.10.10:1521/orcl dbtime'
        print '    2. python zodbm.py close system/oracle@192.168.10.10:1521/orcl'
        print '    3. python zodbm.py closeall'
        print ''

    def handle(self,msg):
        msg = eval(msg)
        return msg[0]

if __name__ == '__main__':
    msg_handler = MsgHandler(sys.argv[1])
    print msg_handler.handle(sys.argv[2])

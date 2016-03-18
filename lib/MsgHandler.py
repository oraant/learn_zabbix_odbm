# coding:utf-8

import os,sys

class MsgHandler:

    def __help():
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
        return msg

if __name__ == '__main__':
    msg_handler = MsgHandler()
    msg_handler.handle(sys.argv[1])

# coding:utf-8
import sys,os
import socket
import logging

class SocketServer:

    def __init__(self,sock_file='/var/lib/zodbm.sock',sock_links=5,config_file='/etc/zodbm.conf',log_file='/var/log/zodbm.log'):
        self.sock_file = sock_file
        self.sock_links = sock_links
        self.config_file = config_file
        self.log_file = log_file

        logging.basicConfig(level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',filename=log_file)

    def __create_server(self):
        '''开启一个Socket Server服务'''
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(self.sock_file):
            os.unlink(self.sock_file)
        self.server.bind(self.sock_file)
        self.server.listen(self.sock_links)

    def __handle_msg(self,msg_handler):
        '''处理基本的启、停、查请求'''
        while True:
            connection, address = self.server.accept()
            req = connection.recv(1024)

            # 处理关闭请求
            if req == 'stop':
                res = 'Stoping Server'
                connection.send(res)
                connection.close()
                os.unlink(self.sock_file)
                exit(0)
            # 处理状态请求
            elif req == 'status':
                res = 'Server is running'
                connection.send(res)
            # 处理其他请求
            elif req != '':
                res = msg_handler.handle(req)
                connection.send(res)

    def __send_msg(self,req):
        '''创建一个Socket Client，并像服务器发送信息'''
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(self.sock_file)
            client.send(req)
            res = client.recv(1024)
        except socket.error:
            res = 'Server is not running.'
        finally:
            client.close()
        return res

    def server_start(self):
        '''验证密码，后台创建服务，并处理请求'''
        if self.server_status() == 'Server is running':
            return 'Server is already running'
            exit(1)

        from MsgHandler import MsgHandler
        from Verify import Verify
        from Daemon import Daemon

        verify = Verify()
        if verify.verify_passwd():
            print 'Starting Server.'
            logging.info('Starting Server.')
        else:
            print 'Server can\'t Start'
            logging.warning('passwd is wrong,server can\'t start.')
            exit(2)

        daemon = Daemon('/dev/null',self.log_file,self.log_file)
        msg_handler = MsgHandler(self.config_file)

        self.__create_server()
        daemon.daemonize()
        self.__handle_msg(msg_handler)

    def server_stop(self):
        '''向服务发送关闭请求'''
        logging.info('Stopping Server.')
        return self.__send_msg('stop')

    def server_status(self):
        '''向服务发送状态请求'''
        return self.__send_msg('status')

    def server_restart(self):
        '''关闭再打开服务器'''
        print self.server_stop()
        self.server_start()

    def server_send(self,req):
        '''向服务器发送信息'''
        return self.__send_msg(req)

# coding:utf-8
import sys,os
import socket

class SocketServer:

    def __init__(links=5,sockfile='/var/lib/zodbm.sock'):
        self.sockfile = sockfile

    def __create_server():
        '''开启一个Socket Server服务'''
        self.server = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        if os.path.exists(sock):
            os.unlink(sock)
        self.server.bind(sock)
        self.server.listen(links)

    def __handle_msg(msg_handler):
        '''处理基本的启、停、查请求'''
        while True:
            connection, address = self.server.accept()
            req = connection.recv(1024)

            # 处理关闭请求
            if req == 'stop':
                res = 'Server is stopped'
                connection.send(res)
                connection.close()
                os.unlink(self.sockfile)
                exit(0)
            # 处理状态请求
            elif req == 'status':
                res = 'Server is running'
                connection.send(res)
            # 处理其他请求
            elif req != '':
                res = msg_handler.handle(req)
                connection.send(res)

    def __send_msg(req):
        '''创建一个Socket Client，并像服务器发送信息'''
        client = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        try:
            client.connect(sock_file)
            client.send(req)
            res = client.recv(1024)
        except socket.error:
            res = 'Server is not running.'
        finally:
            client.close()
        return res

    def server_start():
        if server_status == 'Server is running':
            return 'Server is already running'
            exit(1)

        from MsgHandler import MsgHandler
        from Verify import Verify
        from Daemon import Daemon

        verify = Verify()
        daemon = Daemon()
        msg_handler = MsgHandler()

        verify.verify_passwd()
        __create_server()
        daemon = Daemon()
        __handle_msg(msg_handler)

    def server_stop():
        '''向服务发送关闭请求'''
        return self.__send_msg('stop')

    def server_status():
        '''向服务发送状态请求'''
        return self.__send_msg('status')

    def server_restart():
        '''关闭再打开服务器'''
        self.server_stop()
        return self.server_start()

# coding:utf-8
import sys,os

class Daemon:
    
    def __init__(self,stdin='/dev/null',stdout='/dev/null', stderr='dev/null'):
        '''初始化，指定标准输入输出文件'''
        self.stdin = stdin
        self.stdout = stdout
        self.stderr = stderr

    def daemonize(self):
        '''Fork当前进程为守护进程，重定向标准文件描述符'''
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
        si = file(self.stdin, 'r')
        so = file(self.stdout,'a+')
        se = file(self.stderr,'a+',0)
        os.dup2(si.fileno(), sys.stdin.fileno())
        os.dup2(so.fileno(), sys.stdout.fileno())
        os.dup2(se.fileno(), sys.stderr.fileno())

if __name__ == '__main__':
    try:
        logfile = sys.argv[1]
    except:
        pass
    finally:
        logfile = '/dev/null'
    d = Daemon('/dev/null',logfile,logfile)
    d.daemonize()
    while(True):
        pass

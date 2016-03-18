# coding: utf-8
# authon: oraant
# version: v1.0
# date: 160317

import commands
import sys,os
import base64

def compile(pyfile):
    '''将.py文件转换成c文件后，编译成so文件，以防止反编译代码'''
    command = 'cython ' + pyfile
    (status, output) = commands.getstatusoutput(command)
    if status != 0:
            print output
            exit(1)

    command = 'echo ' + pyfile + '|awk -F \'.\' \'{print $1}\''
    (status, output) = commands.getstatusoutput(command)
    if status != 0:
            print output
            exit(2)
    else:
            cfile = output + '.c'
            sofile = output + '.so'

    command = 'gcc -o ' + sofile + ' -shared -fPIC -I /usr/include/python2.6 -l python2.6 ' + cfile
    (status, output) = commands.getstatusoutput(command)
    if status != 0:
            print output
            exit(3)
    else:
            exit(0)

def decode(code):
    '''根据加密后的字符串算出密码'''
    code = base64.decodestring(code)
    code = base64.decodestring(code)
    text = base64.decodestring(code)

    try:
        command = '''echo `echo ''' + text.strip('\n') + '''|tr -d "a-zA-Z:-"`/3.7+123456|bc'''
        output = os.popen(command)
        print output.read().strip()
        output.close()
    except Exception,e:
        print e
        exit(4)

def help():
    '''打印使用语法'''
    print ''
    print '  Input parameter is wrong.'
    print ''
    print '  Usage:'
    print '      python ' + sys.argv[0] + ' compile <pyfile>'
    print '      python ' + sys.argv[0] + ' decode  <code>'
    print ''
    print '  Explain:'
    print '      ' + 'Compile python file will protect source code from peep.'
    print '      ' + 'Decode will calculate out the passwd with cryptograph.'
    print ''

if __name__ == '__main__':
    '''主要业务处理'''
    try:
        option = sys.argv[1]
        target = sys.argv[2]
        options = {'compile':compile,'decode':decode}
        options.get(option)(target)
    except Exception,e:
        print e
        help()
        exit(5)

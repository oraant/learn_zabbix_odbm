import os,sys
import base64

def __generate_text():
    '''生成日期-MAC字符串'''
    command = '''echo `date +%y%m%d``ifconfig|head -1|awk '{print "-"$NF}'`'''
    output = os.popen(command)
    text = output.read()
    output.close()
    return text

def generate_code():
    '''将日期-MAC字符串加密'''
    text = generate_text()
    text = base64.encodestring(text)
    text = base64.encodestring(text)
    text = base64.encodestring(text)
    text = base64.encodestring(text)
    return text

def ___generate_passwd():
    '''根据日期-MAC算出密码'''
    command = '''echo `date +%y%m%d``ifconfig|head -1|awk '{print "-"$NF}'|tr -d "a-zA-Z:-"`/3.7+123456|bc'''
    output = os.popen(command)
    passwd = output.read()
    output.close()
    return passwd

def verify_passwd(password):
    '''判断密码是否正确'''
    if password == generate_passwd():
        return True
    else:
        return False

def __passwd_code(code):
    '''根据加密后的字符串算出密码'''
    code = base64.decodestring(code)
    code = base64.decodestring(code)
    code = base64.decodestring(code)
    text = base64.decodestring(code)

    command = '''echo `echo ''' + text.strip('\n') + '''|tr -d "a-zA-Z:-"`/3.7+123456|bc'''
    output = os.popen(command)
    passwd = output.read()
    output.close()
    return passwd

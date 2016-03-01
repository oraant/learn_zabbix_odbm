# coding:utf-8

import os,sys
import base64

class Verify:

    def __generate_text(self):
        '''生成日期-MAC字符串'''
        command = '''echo `date +%y%m%d``ifconfig|head -1|awk '{print "-"$NF}'`'''
        output = os.popen(command)
        text = output.read()
        output.close()
        return text
    
    def generate_code(self):
        '''将日期-MAC字符串加密'''
        text = '160301-11:22:33:44:55:66'
        text = base64.encodestring(text)
        text = base64.encodestring(text)
        text = base64.encodestring(text)
        return text
    
    def __generate_passwd(self):
        '''根据日期-MAC算出密码'''
        command = '''echo `date +%y%m%d``ifconfig|head -1|awk '{print "-"$NF}'|tr -d "a-zA-Z:-"`/3.7+123456|bc'''
        output = os.popen(command)
        passwd = output.read()
        output.close()
        return passwd
    
    def verify_passwd(self,password):
        '''判断密码是否正确'''
        if password == self.__generate_passwd().strip('\n'):
            return True
        else:
            return False
    
    def __passwd_code(self,code):
        '''根据加密后的字符串算出密码'''
        code = base64.decodestring(code)
        code = base64.decodestring(code)
        text = base64.decodestring(code)
    
        command = '''echo `echo ''' + text.strip('\n') + '''|tr -d "a-zA-Z:-"`/3.7+123456|bc'''
        output = os.popen(command)
        passwd = output.read()
        output.close()
        return passwd

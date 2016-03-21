# coding:utf-8
import ConfigParser

class DataPicker:

    def __init__(self,config_file,server_conn):
        self.config_file = config_file
        self.server_conn = server_conn

        self.cf = ConfigParser.ConfigParser()
        self.cf.read(config_file)

        print self.cf.get('uptime','tables',0,{'cache':60})

if __name__ == '__main__':
    d=DataPicker('/root/zabbix-odbm/conf/picker.conf','b')

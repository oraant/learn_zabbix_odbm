# coding:utf-8

class ConnsManager:

    def __init__():
        self.conns = {}

    def __create_conn(self,link):
        raise NotImplementedError,"Class %s does not implement required function" % self.__class__
        conn=''
        return conn

    def __test_conn(self,conn):
        raise NotImplementedError,"Class %s does not implement required function" % self.__class__
        useable=''
        return useable

    def __use_conn(self,conn,sql):
        raise NotImplementedError,"Class %s does not implement required function" % self.__class__
        datas = ''
        return datas

    def __close_conn(self,conn):
        raise NotImplementedError,"Class %s does not implement required function" % self.__class__

    def get_conn(self,name,link):
        if name in self.dict.keys():
            return self.dict[name]
        try:
            conn = self.__create_conn(link)
            self.dict[name] = conn
            return conn
        except:
            return False

    def reget_conn(self,name,link):
        self.close_conn(name)
        self.get_conn(name,link)

    def clear_conn(self,name)
        conn = self.dict.pop(name)
        self.__close_conn(conn)

    def clear_conns(self)
        for name in self.dict.keys():
            self.clear_conn(name)

class OracleConns(ConnsManager):
    #dict = {}
    dict = {
        'link1':'conn1',
        'link2':'conn2',
        'link3':'conn3',
        'link4':'conn4',
        'link5':'conn5',
        }

    def __create_conn(self,link)
        import cx_Oracle
        conn = cx_Oracle.connect(link)
        return conn

    def get_or_create_conn(self,name,target):
        if name in self.dict.keys():
            return self.dict[name]
        else:
            conn = self.__create_conn(target)
            self.dict[name] = conn
            return conn

    def use_conn(self,name,sql):
        return self.get_conn(name).execute(sql).fetchall()

    def close_conn(self,name)
        self.dict[name].close()

    def close_conns(self)
        for name in self.dict.keys():
            self.close_conn(name)


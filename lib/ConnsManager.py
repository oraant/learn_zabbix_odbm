# coding:utf-8

class ConnsManager:

    def __init__(self):
        self.conns = {}

    def _create_conn(self,link):
        raise NotImplementedError,"Class %s does not implement required function" % self._class_
        conn=''
        return conn

    def _test_conn(self,conn):
        raise NotImplementedError,"Class %s does not implement required function" % self._class_
        useable=''
        return useable

    def _use_conn(self,conn,sql):
        raise NotImplementedError,"Class %s does not implement required function" % self._class_
        datas = ''
        return datas

    def _close_conn(self,conn):
        raise NotImplementedError,"Class %s does not implement required function" % self._class_

    def get_conn(self,name,link):
        if name in self.conns.keys():
            print self.conns ############
            return self.conns[name]
        try:
            conn = self._create_conn(link)
            self.conns[name] = conn
            print self.conns ############
            return conn
        except Exception,e:
            print e ############
            return False

    def reget_conn(self,name,link):
        self.clear_conn(name)
        self.get_conn(name,link)

    def clear_conn(self,name):
        conn = self.conns.pop(name)
        self._close_conn(conn)

    def clear_conns(self):
        for name in self.conns.keys():
            self.clear_conn(name)

class OracleConns(ConnsManager):

    def _create_conn(self,link):
        import cx_Oracle
        conn = cx_Oracle.Connection(link)
        return conn

    def _test_conn(self,conn):
        sql='select open_mode from v$database'
        try:
            datas = self._use_conn(conn,sql)
        except:
            return False

        if datas == 'READ WRITE':
            return True
        else:
            return False

    def _use_conn(self,conn,sql):
        cursor = conn.cursor()
        cursor.execute(sql)
        datas = cursor.fetchall()
        cursor.close()
        return datas

    def _close_conn(self,conn):
        conn.close()

if __name__ == '__main__':
    tnsname = 'system/oracle@192.168.18.129:1521/db11g'
    ocns = OracleConns()
    import time
    for i in range(5):
        print 'start'
        time.sleep(3)
        conn = ocns.get_conn(tnsname,tnsname)
    print conn
    ocns.clear_conns()
    #print '##########'

# coding:utf-8
import time

class VerifyManager:
    ''' 用于对行为的结果（成功失败）产生记录，并根据这些记录来判断当
        前是否适合再次进行这种行为，或者之前的行为是否仍旧有效。

        比如我连接数据库，连续连接失败3次后，就不应该继续尝试连接了。
        但当时间过去一小时后，则可以再次试一下，看看是否恢复正常了。

        另外就是我拉取了一部分远端数据，如果上次拉取成功的时间距离现
        在不超过30秒，那么这些数据就是新的，可以继续使用，否则就需要
        重新拉取一遍。
    '''

    def __init__(self,max_length = 5):
        ''' 指定最多记录几次历史信息，避免无限制增长导致大量的内存占用'''
        self.records = {}
        self.max_length = max_length

    def __desc_dict(self):
        ''' 做测试时用的，打印一下字典里的内容'''
        print self.records

    def __sort_dict_keys(self,d):
        ''' 将dict的key排序并返回排序后的key列表'''
        keys = d.keys()
        keys.sort()
        return keys

    def __sort_dict_values(self,d):
        ''' 先按照key排序，然后按照此顺序返回对应的值'''
        keys = d.keys()
        keys.sort()
        return map(d.get, keys)

    def __shave_dict_head(self,d,count=1):
        ''' 先将dict排序，然后去掉最早的记录'''
        first_keys = self.__sort_dict_keys(d)[:count]
        for key in first_keys:
            d.pop(key)

    def __record(self,name,value):
        ''' 在该名字对应的链表上，按照时间增加一条记录，由调用者指定要记录的值。
            如果没有这个链表，则根据名称新建一个。
        '''
        now = time.time()
        try:
            self.records[name][now]=value
        except KeyError:
            self.records[name]={now:value}

        record = self.records[name]
        if len(record.keys()) > self.max_length:
            self.__shave_dict_head(record)

    def record_failed(self,name):
        '''增加一个失败记录'''
        self.__record(name,0)

    def record_succeed(self,name):
        '''增加一个成功记录'''
        self.__record(name,1)

    def useable(self,name,counts=3,retry_time=30):
        ''' 根据该姓名记录的历史信息，判断是否应该再次尝试该行为
            counts=3，表示如果连续失败了3次，那么说明这个行为遇到了问题
            retry_time=30，表示这个行为出问题后，多久后才可以再次尝试执行
        '''
        counts = -counts
        record = self.records[name]

        last_values = self.__sort_dict_values(record)[counts:]
        if sum(last_values) != 0:
            return True

        last_time = self.__sort_dict_keys(record)[-1]
        if time.time() - last_time >= retry_time:
            return True

        return False

    def expired(self,name,expired_time=30):
        ''' 根据该姓名记录的历史信息，判断上次的成功是否已经过期了
            expired_time=30，表示判断上次成功距今是否已超过了30秒
            如果上次的记录是失败的，则直接返回过期的
        '''
        record = self.records[name]
        last_value = self.__sort_dict_values(record)[-1]
        last_time = self.__sort_dict_keys(record)[-1]
        gap_time = time.time() - last_time

        if last_value == 1 and gap_time < expired_time:
            return False
        return True

def a(name):
    '''模拟增加一堆记录'''
    v.record_succeed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_succeed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_succeed(name)
    v.record_failed(name)
    v.record_succeed(name)

def b(name):
    '''模拟增加一堆记录'''
    v.record_failed(name)
    v.record_succeed(name)
    v.record_failed(name)
    v.record_succeed(name)
    v.record_failed(name)
    v.record_failed(name)
    v.record_succeed(name)
    v.record_failed(name)

if __name__ == '__main__':
    '''测试模块'''
    v = VerifyManager(3)
    a('db11g')
    b('sszzs')

    v.ff()
    time.sleep(1)
    print v.useable('db11g',counts=1,retry_time=3)
    print v.expired('sszzs',3)

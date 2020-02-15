'''
 Created on Sat Feb 15 2020

 Copyright (c) 2020 QiuDog
'''

import redis

class MyRedis():
    def __init__(self, host, port):
        self.cli = redis.Redis(host=host, port=port)

    def add_domain(self, domain, ex):
        self.cli.set(domain, '', ex=ex)
    
    def has_domain(self, domain):
        return self.cli.get(domain) != None



if __name__ == '__main__':
    from dotenv import load_dotenv
    import os, time
    load_dotenv()

    r = MyRedis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')))
    r.add_domain('www.example.com', ex=8)
    print(r.has_domain('www.example.com'))
    time.sleep(10)
    print(r.has_domain('www.example.com'))

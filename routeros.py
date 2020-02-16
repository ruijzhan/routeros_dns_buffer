'''
 Created on Sat Feb 15 2020

 Copyright (c) 2020 Your Company
'''

import routeros_api
import logging

class MyRos():

    def __init__(self, host, username, password):
        self.__connection = routeros_api.RouterOsApiPool(host, \
            username=username, password=password, plaintext_login=True)
        self.api = self.__connection.get_api()
        self.addr_list = self.api.get_resource('/ip/firewall/address-list')

    def add_domain(self, domain, list_name, timeout):
        try:
            self.addr_list.add(address=domain, list=list_name, timeout=timeout)
        except Exception as e:
            if 'already have such entry' in str(e.original_message):
                logging.info('List {} already has {}'.format(list_name, domain))
                return False
            elif 'not a valid dns name' in str(e.original_message):
                return False
            else:
                raise
        else:
            return True

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os
    load_dotenv()

    ros = MyRos(host=os.getenv('ROUTEROS_IP'), username=os.getenv('ROUTEROS_USER'),\
        password=os.getenv('ROUTEROS_PASS'))

    print(ros.add_domain(domain='www.google.com', list_name='DNS_buffer_auto', timeout='1m'))
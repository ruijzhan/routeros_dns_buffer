'''
 Created on Sat Feb 15 2020

 Copyright (c) 2020 QiuDog
'''

import docker
import logging

class CoreDNS():
    
    def __init__(self, docker_url, container):
        try:
            self.__client = docker.DockerClient(base_url=docker_url)
            self.__coredns = self.__client.containers.get(container)
            self.logger = self.__coredns.logs(follow=True, stream=True, tail=0)
        except Exception as e:
            logging.error('Docker error')
            logging.error(e)

    def get_domain(self):
        try:
            log_line = next(self.logger).decode('utf-8')
        except StopIteration:
            print('coredns container error')
            raise
        return log_line.split()[-1][:-1] if 'INFO' in log_line else ''

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os, sys, signal
    load_dotenv()

    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    coreDNS = CoreDNS(docker_url=os.getenv('DOCKER_ADDR'), container='coredns')
    while True:
        d = coreDNS.get_domain()
        if d:
            print(d)

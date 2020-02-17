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
            self.__logging = self.__coredns.logs(follow=True, stream=True, tail=0)
        except Exception as e:
            logging.error('Docker error')
            logging.error(e)

    def domains(self):
        for line in self.__logging:
            line = line.decode('utf-8')
            if 'NOERROR' in line:
                domain = line.split()[-1][:-1]
                if '.' in domain:
                    yield domain

    async def a_get_domain(self):
        return next(self.domains())

if __name__ == '__main__':
    from dotenv import load_dotenv
    import os, sys, signal
    import asyncio
    load_dotenv()

    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)

    coreDNS = CoreDNS(docker_url=os.getenv('DOCKER_ADDR'), container='coredns')
    loop = asyncio.get_event_loop()
    cr = coreDNS.a_get_domain()
    task = asyncio.ensure_future(cr)
    loop.run_until_complete(task)

    print(task.result())

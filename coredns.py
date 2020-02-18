'''
 Created on Sat Feb 15 2020

 Copyright (c) 2020 QiuDog
'''

import docker
import logging
import asyncio

class CoreDNS():
    
    def __init__(self, docker_url, container):
        try:
            self.__client = docker.DockerClient(base_url=docker_url)
            self.__coredns = self.__client.containers.get(container)
            self.__logging = self.__coredns.logs(follow=True, stream=True, tail=0)
            self.__loop = asyncio.get_event_loop()
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

    def get_domain(self):
        return next(self.domains())

    async def a_get_domain(self):
        return await self.__loop.run_in_executor(None, self.get_domain)

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
    cr1 = coreDNS.a_get_domain()
    cr2 = coreDNS.a_get_domain()
    tasks = [
        asyncio.ensure_future(cr1), 
        asyncio.ensure_future(cr2)
    ]
    loop.run_until_complete(asyncio.wait(tasks))

    for task in tasks:
        print(task.result())

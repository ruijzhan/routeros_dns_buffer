from coredns import CoreDNS
from myredis import MyRedis
from routeros import MyRos

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

import os
import sys
import signal
import asyncio
import functools

def process_domain(domain, redis, ros, redis_ex, ros_ex):
    if not redis.has_domain(domain):
        if ros.add_domain(domain, 'DNS_buffer_auto', ros_ex):
            logging.info('Added to ROS {}'.format(domain))
        redis.add_domain(domain, redis_ex)

async def worker(coredns, redis, ros):
    while True:
        domain = await coredns.a_get_domain()
        process_domain(domain, redis, ros, 60, '1m')

def main():
    from dotenv import load_dotenv
    load_dotenv()

    ros = MyRos(host=os.getenv('ROUTEROS_IP'), username=os.getenv('ROUTEROS_USER'),\
        password=os.getenv('ROUTEROS_PASS'))
    redis = MyRedis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')))

    docker_addrs = os.getenv('DOCKER_ADDRS').split(',')
    print(docker_addrs)
    l_coredns = [CoreDNS(docker_url=docker_addr, container='coredns') for docker_addr in docker_addrs]
    
    loop = asyncio.get_event_loop()
    tasks = [asyncio.ensure_future(worker(c, redis, ros)) for c in l_coredns]

    try:
        loop.run_until_complete(asyncio.wait(tasks))
    except KeyboardInterrupt:
        loop.stop()
    finally:
        loop.close()


if __name__ == '__main__':
    main()

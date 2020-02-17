from coredns import CoreDNS
from myredis import MyRedis
from routeros import MyRos

from dotenv import load_dotenv
import os, sys, signal
load_dotenv()

import logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

def main():
    ros = MyRos(host=os.getenv('ROUTEROS_IP'), username=os.getenv('ROUTEROS_USER'),\
        password=os.getenv('ROUTEROS_PASS'))
    rediss = MyRedis(host=os.getenv('REDIS_HOST'), port=int(os.getenv('REDIS_PORT')))
    coreDNS = CoreDNS(docker_url=os.getenv('DOCKER_ADDR'), container='coredns')

    for domain in coreDNS.domains():
        if not rediss.has_domain(domain):
            if ros.add_domain(domain, 'DNS_buffer_auto', '1m'):
                logging.info('Added to ROS {}'.format(domain))
    
            rediss.add_domain(domain, 60)

if __name__ == '__main__':
    def signal_handler(signal, frame):
        sys.exit(0)
    signal.signal(signal.SIGINT, signal_handler)
    main()
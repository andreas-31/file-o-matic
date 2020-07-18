#!/usr/bin/env python3
import os
import sys
import argparse
from pathlib import Path
from scapy.all import *
# import scapy.all as scapy

import logging
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
# create logger
logger = logging.getLogger('dev')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
# create formatter
formatter = logging.Formatter('%(asctime)s/%(name)s/%(levelname)s: %(message)s')
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)

def read_pcap(pcap_path):
    logger.info('Reading PCAP {}'.format(pcap_path))
    try:
        packets = rdpcap(str(pcap_path))
        # Let's iterate through every packet
        for packet in packets:
            # We're only interested packets with a ISAKMP payload
            if packet.haslayer(ISAKMP):
                my_isakmp = packet.getlayer(ISAKMP)
                #print(my_isakmp.show())
                logger.info('-> Has ISAKMP')
                if my_isakmp.flags == 'res3':
                    logger.info('Found IKE_SA_INIT')
                    logger.info("Initiator SPI: {}".format(bytes(my_isakmp.init_cookie).hex()))
                    logger.info("Responder SPI: {}".format(bytes(my_isakmp.resp_cookie).hex()))
                    logger.info("Exchange type: {}".format(my_isakmp.exch_type))
                    logger.info("Flags: {}".format(my_isakmp.flags))
                    line = bytes(my_isakmp).hex()
                    n = 2 # two characters per byte
                    byte_array = [line[i:i+n] for i in range(0, len(line), n)]
                    hex_formatted = ":".join(byte_array)
                    logger.info(hex_formatted)
            elif packet.haslayer(GTP):
                logger.info('-> Has GTP')
    except Exception as e:
        logger.info('Failed to parse PCAP {}'.format(pcap_path))
        logger.info(e)

if __name__ == '__main__':    
    parser = argparse.ArgumentParser()
    parser.add_argument("pcap", help="PCAP file or directory")
    args = parser.parse_args()
    path = args.pcap
    logger.info('Path to check for PCAP files = ' + path)
    
    pcap_files = list()
    # check if arg refers to existing file or dir
    if not os.path.exists(path):
        logger.error('{} does not exist!'.format(path))
        sys.exit(-1)
    # check if we got a file, dir or something else
    if os.path.isfile(path):
        pcap_files.append(Path(path))
    elif os.path.isdir(path):
        suffixes = {'.pcap', '.pcapng'}
        pcap_files = [path for path in Path(path).glob('**/*') if path.suffix in suffixes]
    else:
        logger.error('{} is not a file or directory!'.format(path))
        sys.exit(-2)
        
    logger.info('PCAP Files:')
    logger.info('\n'.join(str(pcap.resolve()) for pcap in pcap_files))
    [read_pcap(pcap_file) for pcap_file in pcap_files]
    
    


#!/usr/bin/env python3

import gevent.monkey
gevent.monkey.patch_all()

import logging
import os
import sys
import time
import traceback

from slack_sdk.rtm_v2 import RTMClient
from slack_sdk.web import WebClient

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)
logger = logging.getLogger(__name__)

def main(args):
    token = os.environ['SLACK_BOT_TOKEN']

    client = WebClient(token=token)

    while 1:
        res = client.rtm_connect()
        url = res['url']

        try:
            rtm = RTMClient(token=token)
            @rtm.on('message')
            def handle(client, event):
                print(client, event)
            rtm.start()
        except Exception as e:
            print(traceback.format_exc())
            time.sleep(5)

if __name__ == '__main__':
    main(sys.argv[1:])

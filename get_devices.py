#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import json
import re
import subprocess
import sys

from workflow import Workflow3

MAC_ADDRESS_LINE_REGEX = re.compile(
    r'^('
    r'[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}-[0-9A-F]{2}'
    r')'
    r'\s-\s'
    r'(.*)$',
    flags=re.M | re.I)

log = None


def get_bluetooth_devices():
    bluetooth_output = subprocess.check_output(['/usr/local/bin/BluetoothConnector'])
    output_devices = MAC_ADDRESS_LINE_REGEX.findall(bluetooth_output)
    log.debug(output_devices)

    bluetooth_devices = []
    for device in output_devices:
        bluetooth_devices.append({
            'name': device[1],
            'mac_address': device[0],
        })
    return bluetooth_devices


def main(wf):
    bluetooth_devices = wf.cached_data(
        'bluetooth_devices',
        get_bluetooth_devices,
        max_age=30)
    log.debug(bluetooth_devices)
    for device in bluetooth_devices:
        wf.add_item(
            uid=device.get('mac_address'),
            title=device.get('name'),
            subtitle=device.get('mac_address'),
            # icon=DEVICE_ICON,
            arg=json.dumps(device),
            valid=True)

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))

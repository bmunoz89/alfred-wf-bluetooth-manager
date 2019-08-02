#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import json
import os
import subprocess
import sys

from workflow import ICON_INFO, Workflow3

log = None


def connect_bluetooth_devices(mac_address):
    command = [
        '/usr/local/bin/BluetoothConnector',
        '--connect',
        mac_address,
        '--notify',
    ]
    log.debug(' '.join(command))
    subprocess.check_output(command)


def main(wf):
    mac_address = os.getenv('bluetooth_mac_address')
    if mac_address is None:
        device = json.loads(wf.args[0])
        mac_address = device['mac_address']
    log.debug(mac_address)

    connect_bluetooth_devices(mac_address)

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow3(update_settings={
        'github_slug': 'bmunoz89/alfred-wf-bluetooth-manager',
        'frequency': 7,
    })
    log = wf.logger
    if wf.update_available:
        wf.add_item(
            'New version available',
            'Action this item to install the update',
            autocomplete='workflow:update',
            icon=ICON_INFO)
    sys.exit(wf.run(main))

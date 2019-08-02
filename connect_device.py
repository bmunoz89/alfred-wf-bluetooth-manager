#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import json
import os
import sys

from workflow import Workflow3
from workflow.util import run_command

log = None


def connect_bluetooth_devices(mac_address):
    command = [
        '/usr/local/bin/BluetoothConnector',
        '--connect',
        mac_address,
        '--notify',
    ]
    log.debug(' '.join(command))
    run_command(command)


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
        'frequency': 1,
    })
    log = wf.logger
    if wf.update_available:
        log.debug('Update available')
        wf.start_update()

    sys.exit(wf.run(main))

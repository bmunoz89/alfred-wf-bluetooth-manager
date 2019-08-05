#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import json
import sys

from workflow import Workflow3
from workflow.notify import notify
from workflow.util import set_config

log = None


def main(wf):
    device = json.loads(wf.args[0])
    log.debug(device)

    set_config('bluetooth_mac_address', device['mac_address'])
    set_config('bluetooth_name', device['name'])
    notify('Device stored', device['name'])

    wf.send_feedback()
    return 0


if __name__ == '__main__':
    wf = Workflow3()
    log = wf.logger
    sys.exit(wf.run(main))

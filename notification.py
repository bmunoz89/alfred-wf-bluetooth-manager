#!/usr/bin/python
# encoding: utf-8
from __future__ import print_function

import sys

from workflow import Workflow3
from workflow.notify import notify


def main(wf):
    title, body = wf.args
    notify(title, body)

    return 0


if __name__ == '__main__':
    wf = Workflow3()
    sys.exit(wf.run(main))

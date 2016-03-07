#!/usr/bin/python
# encoding: utf-8

import sys

from wunderlist.handlers.route import route
from wunderlist.util import workflow

def main(wf):
    route(wf.args)

if __name__ == '__main__':
    wf = workflow()
    sys.exit(wf.run(main))

#!/usr/bin/python

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import json


def main():
    data = {
        'sup': {
            'bruh': '!'
        }
    }
    data = json.loads(data)
    print(data)

if __name__ == '__main__':
    main()

#!python3
# coding=utf-8

"""
acfy卸载程序


"""

import os
import platform

if platform.system() == 'Linux':
    if os.path.exists('/usr/local/bin/acfy'):
        os.system('sudo rm -rf /usr/local/bin/acfy')
        os.system('sudo rm -rf ./acfy.sh')


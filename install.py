#! python3
# coding=utf-8

"""
acfy 安装程序

使用方法
python3 install.py
"""

import os
import platform

if platform.system() == 'Linux':
    if os.path.exists('acfy.sh'):
        print('acfy.sh 已删除')
        os.remove('acfy.sh')
    os.mknod("acfy.sh")
    os.system('echo "python3 $(pwd)/acfy.py \$*" > acfy.sh')
    os.system('sudo chmod +x ./acfy.sh')
    if os.path.exists('/user/local/bin/acfy'):
        os.system('rm -rf /usr/local/bin/acfy')
    os.system('sudo ln -s $(pwd)/acfy.sh /usr/local/bin/acfy')

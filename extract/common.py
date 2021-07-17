'''
Created Date: Tuesday July 13th 2021 6:53:53 pm
Author: Andrés X. Vargas
-----
Last Modified: Friday July 16th 2021 11:15:06 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import yaml
from pathlib import Path

__config = None
__file_path = Path(__file__).resolve().parent


def config():
    global __config, __file_path
    if not __config:
        with open(f'{__file_path}/config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)
    return __config

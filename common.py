'''
Created Date: Tuesday July 13th 2021 6:53:53 pm
Author: Andrés X. Vargas
-----
Last Modified: Tuesday July 13th 2021 10:22:30 pm
Modified By: the developer known as Andrés X. Vargas at <axvargas@fiec.espol.edu.ec>
-----
Copyright (c) 2021 MattuApps
'''
import yaml

__config = None

def config():
    global __config
    if not __config:
        with open('config.yaml', mode='r') as f:
            __config = yaml.load(f, Loader=yaml.FullLoader)
    return __config
     
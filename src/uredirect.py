#!/usr/bin/env python
# -*- coding: utf-8 -*-

# uredirect-py
#   by Naoki Rinmous <sukareki@gmail.com>
#   published under WTFPL


# Bootstrap

from database import Database
from server import Server

import utils

def main():
    config = utils.readConfig('config.json')

    db = Database(config)
    server = Server(config, db)

if __name__ == '__main__':
    main()

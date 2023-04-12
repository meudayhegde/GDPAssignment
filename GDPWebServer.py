#!/usr/bin/python3

import argparse

from app import GDPServer
from utils import read_flask_config
from DBUtil import DBUtil

flask_config = read_flask_config()

parser = argparse.ArgumentParser(description="a flask based web server for displaying GDP Chart")
parser.add_argument("--port", "-p", type=int, help="Port to listen on", default=int(flask_config['port']))
parser.add_argument("--host", "-H", type=str, help="Client address to accept request from", default=flask_config['host'])
args = parser.parse_args()

if __name__ == '__main__':
    db_util = DBUtil()
    if db_util.is_connected():
        app = GDPServer(db_util, port=args.port, host=args.host)
        app.start()
    else:
        print('DB Connection not available')
        exit(2)


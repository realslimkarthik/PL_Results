from    pymongo import MongoClient
from    utils.utils import get_mongo_host_port_str

class MongoDB(object):

    def __init__(self, username, password, host_name, port, db, auth_db='admin'):
        host_port_str   =   get_mongo_host_port_str(host_name, port)
        self.client     =   MongoClient(host_port_str)
        self.client[db].authenticate(username, password, source=auth_db)

    def __getitem__(self, item):
        return self.client.item

    def __getattr__(self, item):
        return self.client.item

#!/usr/bin/env python3
"""
Python script that provides some stats about
Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_logs_stats():
    """stats about
    Nginx logs stored in MongoDB
    """
    client = MongoClient()
    nginx_logs = client.logs.nginx
    docs = nginx_logs.count_documents({})
    print("{} logs".format(docs))
    print("Methods:")
    methods: ["GET", "POST", "PUT", "PATCH", "DELETE"]
    for method in methods:
        method_count = nginx_logs.count_documents({"method": method})
        print("\tmethod {}: {}".format(method, method_count))
    status = nginx_logs.count_documents({"method": "GET", "path": "/status"})
    print("{} status check".format(status))

if __name__ == "__main__":
    nginx_logs_stats()

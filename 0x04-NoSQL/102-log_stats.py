#!/usr/bin/env python3
"""Defines a function that  provides some stats
   about Nginx logs stored in MongoDB
"""
from pymongo import MongoClient


def nginx_stats_check():
    """
    provides some stats about Nginx
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
    print("IPs:")
    top_IPs = nginx_logs.aggregate([{"$group":
        {"_id": "$ip",
        "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10},
        {"$project":
            {"_id": 0, "ip": "$_id", "count": 1}
        }])
    for top_ip in top_IPs:
        count = top_ip.get("count")
        ip_address = top_ip.get("ip")
        print("\t{}: {}".format(ip_address, count))


if __name__ == "__main__":
    nginx_logs_stats()

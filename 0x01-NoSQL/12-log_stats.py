#!/usr/bin/env python3
"""Module for analyzing Nginx log data stored in MongoDB"""

from pymongo import MongoClient


def analyze_nginx_logs():
    """Analyze and display statistics about Nginx logs from MongoDB"""
    db_client = MongoClient('mongodb://127.0.0.1:27017')
    log_collection = db_client.logs.nginx

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    
    total_logs = log_collection.count_documents({})
    print(f"{total_logs} logs")
    
    print("Methods:")
    for http_method in http_methods:
        method_count = log_collection.count_documents({"method": http_method})
        print(f"\tmethod {http_method}: {method_count}")
    
    status_checks = log_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_checks} status check")
    
    top_ips = log_collection.aggregate([
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}
    ])
    
    print("IPs:")
    for ip_data in top_ips:
        print(f"\t{ip_data.get('_id')}: {ip_data.get('count')}")


if __name__ == "__main__":
    analyze_nginx_logs()

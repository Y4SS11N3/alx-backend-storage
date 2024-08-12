#!/usr/bin/env python3
"""Module for Nginx log analysis in MongoDB"""
from pymongo import MongoClient


def analyze_nginx_logs():
    """Analyze and display stats about Nginx logs stored in MongoDB"""
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    total_logs = nginx_collection.count_documents({})
    print(f"{total_logs} logs")

    http_methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in http_methods:
        method_count = nginx_collection.count_documents({"method": method})
        print(f"\tmethod {method}: {method_count}")

    status_checks = nginx_collection.count_documents(
        {"method": "GET", "path": "/status"}
    )
    print(f"{status_checks} status check")


if __name__ == "__main__":
    analyze_nginx_logs()

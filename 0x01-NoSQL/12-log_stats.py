#!/usr/bin/env python3
"""Module for analyzing Nginx log data in MongoDB"""
from pymongo import MongoClient


def analyze_nginx_logs(log_collection):
    """Display statistics about Nginx request logs"""
    total_logs = log_collection.count_documents({})
    print(f"Total logs: {total_logs}")

    http_methods = ['GET', 'POST', 'PUT', 'PATCH', 'DELETE']
    print("HTTP Methods:")
    for method in http_methods:
        method_count = log_collection.count_documents({"method": method})
        print(f"    {method}: {method_count}")

    status_checks = log_collection.count_documents({
        "method": "GET",
        "path": "/status"
    })
    print(f"Status checks: {status_checks}")


def main():
    """Entry point: Connect to MongoDB and analyze Nginx logs"""
    db_client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_logs = db_client.logs.nginx
    analyze_nginx_logs(nginx_logs)


if __name__ == '__main__':
    main()

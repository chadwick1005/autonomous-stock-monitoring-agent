"""
Worker Package
==============

This package contains the autonomous worker processes responsible for
executing the application's concurrent processing pipeline.

Workers
-------
feature_worker.py
    Consumes streamed market data and computes technical indicators.

alert_worker.py
    Monitors machine learning predictions and generates market alerts
    when predefined confidence thresholds are satisfied.

Design Pattern
--------------
Workers execute asynchronously and communicate through shared queues,
allowing each stage of the processing pipeline to operate
independently.

This producer-consumer architecture improves scalability, fault
isolation, and throughput while enabling additional workers to be
introduced with minimal modifications to the existing system.
"""
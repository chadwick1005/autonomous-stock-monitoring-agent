"""
Streaming Package
=================

This package implements the real-time market data ingestion pipeline.

Components
----------
streamer.py
    Establishes and maintains the Finnhub WebSocket connection.

handlers.py
    Processes incoming trade messages received from the data stream.

run_test.py
    Utility script for validating streaming functionality during
    development.

Architecture
------------
The streaming layer serves as the producer within the system's
producer-consumer architecture.

Responsibilities include:

• Maintaining persistent WebSocket connections.
• Receiving live market events.
• Parsing incoming messages.
• Publishing standardized candle data to asynchronous queues.

The remainder of the application operates independently of the data
source by consuming messages from these queues.
"""
"""
Feature Engineering Package
===========================

This package transforms raw market data into quantitative indicators
that can be consumed by downstream machine learning models and alerting
systems.

Modules
-------
compute.py
    Calculates technical indicators such as RSI, EMA, MACD,
    Bollinger Bands, and volume-based statistics.

utils.py
    Provides reusable helper functions used throughout the feature
    engineering pipeline.

Design Philosophy
-----------------
Feature engineering is intentionally isolated from data ingestion and
machine learning. This separation improves modularity, testing, and
future extensibility while allowing new indicators to be introduced
without modifying other system components.
"""
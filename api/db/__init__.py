"""
Database Package
================

This package defines the database layer used throughout the autonomous
stock monitoring agent.

Components
----------
engine.py
    Creates and configures the SQLModel database engine.

models.py
    Defines ORM models representing database tables.

database.py
    Implements helper functions for reading and writing market features,
    predictions, and historical observations.

Design Goals
------------
• Encapsulate all persistence logic.
• Provide reusable database sessions.
• Maintain separation between storage and business logic.

The remainder of the application interacts with the database through
this package rather than communicating directly with SQLite.
"""
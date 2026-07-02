"""
Machine Learning Package
========================

This package contains all components responsible for training,
loading, and executing predictive machine learning models.

Modules
-------
train_model.py
    Trains the supervised learning model using historical feature data.

ml_worker.py
    Performs real-time inference on engineered market features and
    generates prediction probabilities for downstream decision making.

Objectives
----------
• Maintain separation between offline model training and online
  inference.
• Enable interchangeable machine learning algorithms.
• Produce probability estimates suitable for real-time market analysis.

The machine learning layer consumes engineered features and produces
prediction scores without interacting directly with the streaming
infrastructure.
"""

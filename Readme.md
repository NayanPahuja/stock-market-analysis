# STOCK-MARKET-ANALYSIS

## Overview

This project is an attempt to make a backed in Python FastAPI that allows users to submit stock data and analyze it. The app exposes endpoints for data ingestion and uses Postgres for storing the data.

It also used celery for asynchronous task processing workers using RabbitMQ as the broker.

Dockerized the app for maintaining uniformity in codebase and used grafana for visualization.

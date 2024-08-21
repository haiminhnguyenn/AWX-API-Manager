# Backend for AWX API Management
======================================

## Overview
-----------

This repository contains a Flask-based backend service designed to facilitate the interaction between clients and AWX by managing API requests, handling authentication, and processing tasks asynchronously. It also listens for webhooks from AWX to update the status of ongoing workflows and can return the current status when requested by the client.


## Features
-----------

- **JWT Authentication:** The service uses JSON Web Tokens (JWT) for secure authentication, ensuring that only authorized clients can access the API.
- **PostgreSQL Database:** PostgreSQL is utilized as the primary database for storing user credentials, provisioning data, and other necessary information.
- **Asynchronous Task Processing:** The service leverages RabbitMQ, with the help of the Celery library, to queue and handle tasks asynchronously. This is particularly useful for sending requests to AWX in a non-blocking manner, allowing the service to scale efficiently.


## Quick Setup
--------------
1. Clone this repository.
2. Create a virtualenv and install the requirements (`pip install -r requirements.txt`)
3. Open a second terminal window and start a Celery worker: `celery -A celery_worker.celery worker --loglevel=info`.
4. Start AWX API Management on your first terminal window: `python3 run.py`/`python run.py`
5. Go to `http://localhost:8000/` and register an account to see how the AWX Manager work!
# Dockerized Visitor Counter API

A multi-container application using FastAPI, Redis,
Docker and Docker Compose.

## Technologies
- Python
- FastAPI
- Redis
- Docker
- Docker Compose

## Architecture
Client -> FastAPI -> Redis
          :8000      :6379

## Features
- REST API
- Redis visitor counter
- Docker bridge networking
- Docker DNS
- Persistent Redis storage
- Container health checking

## Installation

Build the Docker image:

docker build -t visitor-counter-api:1.0 .

Start containers:

docker compose up -d

Check status:

docker compose ps

## API Testing

curl http://127.0.0.1:8010/
curl http://127.0.0.1:8010/healthz
curl http://127.0.0.1:8010/visits

## Stop Containers

docker compose down

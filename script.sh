#!/bin/bash

# Build the Docker image
docker build -t my-nginx-parser .

# Run the Docker container
docker run  -d -p 8080:80 my-nginx-parser
#!/bin/bash
echo "Creating PostgreSQL connector..."
curl -X POST -H "Content-Type: application/json" \
  --data @/config/connector_config.json \
  http://kafka-connect:8083/connectors

echo "Connector created successfully!"

#!/bin/bash
curl https://raw.githubusercontent.com/SoftInstigate/restheart/5.4.1/docker-compose.yml --output docker-compose.yml && sudo docker-compose up
curl --user admin:secret -I -X PUT localhost:8080/
curl --user admin:secret -I -X PUT localhost:8080/_schemas
curl --user admin:secret -I -X PUT localhost:8080/_schemas/inventory -T "basic_schema.json"  -H "Content-Type: application/json"
curl --user admin:secret -I -X PUT localhost:8080/inventory
curl --user admin:secret -I -X PUT localhost:8080/inventory -T "inventory_meta.json"  -H "Content-Type: application/json"

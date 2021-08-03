#!/bin/bash
curl --user admin:secret -I -X PUT $1:8080/
curl --user admin:secret -I -X PUT $1:8080/_schemas
curl --user admin:secret -I -X PUT $1:8080/_schemas/inventory -T "basic_schema.json"  -H "Content-Type: application/json"
curl --user admin:secret -I -X PUT $1:8080/inventory
curl --user admin:secret -I -X PUT $1:8080/inventory.files
curl --user admin:secret -I -X PUT $1:8080/inventory -T "inventory_meta.json"  -H "Content-Type: application/json"

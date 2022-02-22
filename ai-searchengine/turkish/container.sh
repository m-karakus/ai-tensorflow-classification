#!/bin/bash
# bash verison.sh prod/nginx-test-deployment.yaml "bug"
value="m-karakus/systems:bert-base-turkish-cased-v1.0.0"
docker build -t ${value} .
docker push ${value}

#!/bin/bash

# Deploy Spark Master
kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml

# Sleep for 10 seconds (adjust as needed)
sleep 10

# Deploy Spark Worker
kubectl create -f ./kubernetes/spark-worker-deployment.yaml

# Create TLS secret
kubectl create secret tls fede-tls-secret --cert=./my-certificate.crt --key=./my-private.key

# Deploy Ingress
kubectl apply -f ./kubernetes/minikube-ingress.yaml

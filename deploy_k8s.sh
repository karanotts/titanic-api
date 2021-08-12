#!/bin/bash
cd k8s
kubectl create -f .
echo "Creating pods" && sleep 20
mongo=$(kubectl get pods -l tier=database -o custom-columns=":metadata.name")
kubectl exec --stdin --tty $mongo -- mongoimport --type csv -h mongo -d titanic -c people --headerline --drop csv/titanic.csv
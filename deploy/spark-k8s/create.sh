#!/bin/bash

# Nombres de los archivos
certificado="tu_certificado.crt"
clave_privada="tu_clave_privada.key"
port="8081"
# Verifica la existencia del certificado en el directorio actual
if [ -f "./$certificado" ]; then
    echo "El certificado $certificado existe en el directorio actual."
else
    echo "Error: El certificado $certificado no se encontró en el directorio actual. Creando certificado..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout "$clave_privada" -out "$certificado"
    echo "Certificado creado exitosamente en $certificado."
fi


kubectl create secret tls spark-tls-secret --cert="${PWD}/tu_certificado.crt" --key="${PWD}/tu_clave_privada.key"


# Deploy Spark Master
kubectl create -f ./kubernetes/spark-master-deployment.yaml
kubectl create -f ./kubernetes/spark-master-service.yaml

# Sleep for 10 seconds (adjust as needed)
sleep 10

# Deploy Spark Worker
kubectl create -f ./kubernetes/spark-worker-deployment.yaml

# Create TLS secret (uncomment and adjust paths if needed)
# kubectl create secret tls fede-tls-secret --cert=./my-certificate.crt --key=./my-private.key

# Deploy Ingress
kubectl apply -f ./kubernetes/minikube-ingress.yaml

# Deploy Kubernetes Dashboard
kubectl apply -f https://raw.githubusercontent.com/kubernetes/dashboard/v2.3.1/aio/deploy/recommended.yaml

# Wait for Dashboard to be ready (adjust sleep time as needed)
sleep 20

# Create ServiceAccount and ClusterRoleBinding for Dashboard access
cat <<EOF | kubectl apply -f -
apiVersion: v1
kind: ServiceAccount
metadata:
  name: admin-user
  namespace: kubernetes-dashboard
---
apiVersion: rbac.authorization.k8s.io/v1
kind: ClusterRoleBinding
metadata:
  name: admin-user
roleRef:
  apiGroup: rbac.authorization.k8s.io
  kind: ClusterRole
  name: cluster-admin
subjects:
- kind: ServiceAccount
  name: admin-user
  namespace: kubernetes-dashboard
EOF

# Create token for admin-user
kubectl -n kubernetes-dashboard create serviceaccount admin-user
kubectl -n kubernetes-dashboard create clusterrolebinding admin-user --clusterrole=cluster-admin --serviceaccount=kubernetes-dashboard:admin-user
token_secret=$(kubectl -n kubernetes-dashboard get secret | grep admin-user | awk '{print $1}')
token=$(kubectl -n kubernetes-dashboard get secret $token_secret -o jsonpath='{.data.token}' | base64 --decode)

echo "Admin token for login: $token"

# Open Kubernetes Dashboard in default browser
case "$(uname -s)" in
    Linux*) xdg-open "http://localhost:$port/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login" ;;
    Darwin*) open "http://localhost:$port/api/v1/namespaces/kubernetes-dashboard/services/https:kubernetes-dashboard:/proxy/#/login" ;;
    *) echo "Unsupported OS for automatic browser opening."
esac



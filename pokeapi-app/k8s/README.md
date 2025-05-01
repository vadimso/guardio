
# install minikube 
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
chmod +x kubectl
sudo mv kubectl /usr/local/bin/

curl -LO https://storage.googleapis.com/minikube/releases/latest/minikube-linux-amd64
sudo install minikube-linux-amd64 /usr/local/bin/minikube

minikube start
# to start with docker driver 
minikube start --driver=docker
# check if minikube working
kubectl get nodes

# run this command to patch prometheus to load the prometheus config
kubectl -n monitoring patch deployment prometheus-deployment \
  --type=json \
  -p='[{"op": "add", "path": "/spec/template/spec/volumes/-", "value":{"name":"additional-configs","configMap":{"name":"prometheus-additional-config"}}},
       {"op": "add", "path": "/spec/template/spec/containers/0/volumeMounts/-", "value":{"name":"additional-configs","mountPath":"/etc/prometheus/additional-scrape-configs"}}]'

# install grafana
curl https://raw.githubusercontent.com/helm/helm/master/scripts/get-helm-3 | bash

helm repo add grafana https://grafana.github.io/helm-charts
helm repo update

helm install grafana grafana/grafana \
  --namespace monitoring --create-namespace \
  --set adminPassword='admin' \
  --set service.type=NodePort
kubectl get svc -n monitoring grafana
kubectl port-forward -n monitoring svc/grafana 3000:80

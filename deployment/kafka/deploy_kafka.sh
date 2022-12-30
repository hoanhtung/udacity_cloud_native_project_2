helm repo add bitnami https://charts.bitnami.com/bitnami
helm install my-project-2 bitnami/kafka
#helm install my-project-3 bitnami/kafka --set persistence.enabled=false --set readinessProbe.enabled=false --set livenessProbe.enabled=false --set zookeeper.persistence.enabled=false
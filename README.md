# UdaConnect
## Overview
### Background
Conferences and conventions are hotspots for making connections. Professionals in attendance often share the same interests and can make valuable business and personal connections with one another. At the same time, these events draw a large crowd and it's often hard to make these connections in the midst of all of these events' excitement and energy. To help attendees make connections, we are building the infrastructure for a service that can inform attendees if they have attended the same booths and presentations at an event.

## Running the app
The project has been set up such that you should be able to have the project up and running with Kubernetes.

### Prerequisites
We will be installing the tools that we'll need to use for getting our environment set up properly.
1. [Install Docker](https://docs.docker.com/get-docker/)
2. [Set up a DockerHub account](https://hub.docker.com/)
3. [Set up `kubectl`](https://rancher.com/docs/rancher/v2.x/en/cluster-admin/cluster-access/kubectl/)

### Environment Setup
To run the application, you will need a K8s cluster running locally and to interface with it via `kubectl`.

### Deployment Steps
1. `kubectl apply -f deployment/db-configmap.yaml` - Set up environment variables for the pods
2. `kubectl apply -f deployment/db-secret.yaml` - Set up secrets for the pods
3. `kubectl apply -f deployment/postgres.yaml` - Set up a Postgres database running PostGIS

Quick way to deploy all services `kubectl apply -f deployment/`.

### Module Structure
Contains 5 modules in system:
- `modules/frontend`: UdaConnect Web
- `modules/person-api`: a service to interact with Person resource (using RestAPI)
- `modules/connection-api`: a service to interact with Connection resource (using RestAPI)
- `modules/location-service`: a service to interact with Location resource (using gRPC)
- `modules/location-consumer-service`: a consumer service to create new location (using message queue)

### Build & deploy location-related service
You need move to `modules` folder
- `frontend`:
```
docker build -t hoanhtung/udaconnect-app:2912 -f ./frontend/Dockerfile .
docker push hoanhtung/udaconnect-app:2912
kubectl apply -f ./frontend/deployment.yaml
```
- `person-api`:
```
docker build -t hoanhtung/udaconnect-person-api:2912 -f ./api/Dockerfile .
docker push hoanhtung/udaconnect-person-api:2912
kubectl apply -f ./person-api/deployment.yaml
```
- `connection-api`:
```
docker build -t hoanhtung/udaconnect-connection-api:2912 -f ./api/Dockerfile .
docker push hoanhtung/udaconnect-connection-api:2912
kubectl apply -f ./connection-api/deployment.yaml
```
- `location-service`:
```
docker build -t hoanhtung/location-service:2912 -f ./location-service/Dockerfile .
docker push hoanhtung/location-service:2912
kubectl apply -f ./location-service/deployment.yaml
```
- `location-consumer-service`:
```
docker build -t hoanhtung/location-consumer-service:2912 -f ./location-consumer-service/Dockerfile .
docker push hoanhtung/location-consumer-service:2912
kubectl apply -f ./location-consumer-service/deployment.yaml
```

## PostgreSQL Database
The database uses a plug-in named PostGIS that supports geographic queries. It introduces `GEOMETRY` types and functions that we leverage to calculate distance between `ST_POINT`'s which represent latitude and longitude.

_You may find it helpful to be able to connect to the database_. In general, most of the database complexity is abstracted from you. The Docker container in the starter should be configured with PostGIS. Seed scripts are provided to set up the database table and some rows.
### Database Connection
While the Kubernetes service for `postgres` is running (you can use `kubectl get services` to check), you can expose the service to connect locally:
```bash
kubectl port-forward svc/postgres 5432:5432
```
This will enable you to connect to the database at `localhost`. You should then be able to connect to `postgresql://localhost:5432/geoconnections`. This is assuming you use the built-in values in the deployment config map.
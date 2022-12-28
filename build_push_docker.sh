APP_PATH="./modules/frontend/Dockerfile"
API_PATH="./modules/api/Dockerfile"

#docker build -t hoanhtung/nd064-udaconnect-app:2812 -f ./modules/frontend/Dockerfile . --platform=linux/amd64
docker build -t hoanhtung/nd064-udaconnect-app:2812 . --platform=linux/amd64
#docker push hoanhtung/nd064-udaconnect-app:2812
#docker build -t hoanhtung/nd064-udaconnect-api:2812 -f $API_PATH .
#docker push hoanhtung/nd064-udaconnect-api:2812

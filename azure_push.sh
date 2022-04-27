#/bin/bash!
docker context use default
docker-compose --file docker-compose.test.yml up --build
docker tag vivienda-service_vivienda-api-test cchcdev.azurecr.io/vivienda-service:latest
docker push cchcdev.azurecr.io/vivienda-service:latest
docker context use azuretest2
docker compose --file docker-compose.azure.yml up --build
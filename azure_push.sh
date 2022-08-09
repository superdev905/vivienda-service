#/bin/bash!
docker context use default
docker-compose --file docker-compose.image.yml up --build
docker tag vivienda-service_vivienda-api cchcdev.azurecr.io/vivienda-service:latest
docker push cchcdev.azurecr.io/vivienda-service:latest
#az acr login --name  cchcprod
docker context use azureprod
docker compose --file docker-compose.prod.yml up --build
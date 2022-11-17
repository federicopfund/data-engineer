# Para ejecutar se necesita un config.json, se adjunta un config.example.json de muestra

**Levantar servidor en DOCKER**
docker build -t fastapi-image .

docker run -d --name softtek-api-container -p 8000:8000 fastapi-image
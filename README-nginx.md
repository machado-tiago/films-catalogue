# Configuração Nginx
- `nginx.conf`

# Compilar a aplicação Java (automatizado no GithubActions)
./mvnw package

# Criar a imagem Docker (automatizado no GithubActions)
docker build -f src/main/docker/Dockerfile.jvm -t machado-tiago/films-catalogue:latest .

# Executar
## 1. Iniciar PostgreSQL (roda usando imagem oficial pronta)
docker run -d --name films-db -e POSTGRES_DB=filmsdb -e POSTGRES_USER=films -e POSTGRES_PASSWORD=films123 -p 5432:5432 -v films-data:/var/lib/postgresql/data postgres:15-alpine

## 2. Iniciar aplicação
docker run -d --name films-app -p 8080:8080 machado-tiago/films-catalogue:latest

## Iniciar Nginx aplicando configuração (roda usando imagem oficial pronta)
docker run -d --name films-nginx -p 80:80 -v "%cd%\nginx.conf:/etc/nginx/conf.d/default.conf" --network host nginx:alpine

# Acessar
- Aplicação: http://localhost (porta 80 por padrão)
- Para parar: `docker stop films-nginx films-app films-db`
- Para limpar: `docker rm films-nginx films-app films-db`
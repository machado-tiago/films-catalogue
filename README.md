# films-catalogue

This project uses Quarkus, the Supersonic Subatomic Java Framework.
If you want to learn more about Quarkus, please visit its website: <https://quarkus.io/>.
> **_NOTE:_**  Quarkus now ships with a Dev UI, which is available in dev mode only at <http://localhost:8080/q/dev/>.

# Configuração Nginx
- arquivo `nginx.conf`

# Compilar a aplicação Java
./mvnw package

# Criar a imagem Docker (automatizado no GithubActions, com push para DockerHub)
docker build -f src/main/docker/Dockerfile.jvm -t machado-tiago/films-catalogue:latest .

# Executar
## 1. Iniciar PostgreSQL (roda usando imagem oficial pronta)
docker run -d --name films-db -e POSTGRES_DB=filmsdb -e POSTGRES_USER=films -e POSTGRES_PASSWORD=films123 -p 5432:5432 -v films-data:/var/lib/postgresql/data postgres:15-alpine

## 2. Iniciar aplicação
docker run -d --name films-app -p 8080:8080 machado-tiago/films-catalogue:latest

## 3. Criar rede
docker network create films-net 2>nul
docker network connect films-net films-db
docker network connect films-net films-app

## 4. Iniciar Nginx aplicando configuração (roda usando imagem oficial pronta)
docker run -d --name films-nginx --network films-net -p 80:80 -v "%cd%\nginx.conf:/etc/nginx/conf.d/default.conf" nginx:alpine

# Acessar
- Aplicação: http://localhost (porta 80 por padrão)
- Para parar: `docker stop films-nginx films-app films-db`
- Para limpar: `docker rm films-nginx films-app films-db`

# Scripts - Films Catalogue
## `csv_to_sql_all.py`
**Função:** Converte todos os CSVs do Data Lake para comandos SQL INSERT

**Entrada:**
- `data-lake/movies.csv`
- `data-lake/users.csv`
- `data-lake/ratings.csv`

**Saída:**
- `import.sql`

## Como Usar

### Script Python
```bash
cd "c:\Desenvolvimento\14_GIT_LOCAL\ADA\films-catalogue"
python src\main\resources\scripts\csv_to_sql_all.py
```

### Import
O `import.sql` é executado automaticamente pelo Quarkus:
```bash
.\mvnw quarkus:dev
```

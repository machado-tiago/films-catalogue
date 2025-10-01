@echo off
setlocal
echo ============================================
echo 🚀 Iniciando ambiente do Films Catalogue...
echo ============================================

REM === Caminho base (diretório onde o script está) ===
set SCRIPT_DIR=%~dp0

REM === 0. Login no Docker Hub ===
echo [0/6] Realizando login no Docker Hub...
docker login
if %errorlevel% neq 0 (
    echo ERRO: falha no login Docker Hub
    pause
    exit /b 1
)

REM === 1. Criar rede Docker (se não existir) ===
echo [1/6] Criando rede films-net...
docker network create films-net 2>nul

REM === 2. Subir o banco de dados PostgreSQL ===
echo [2/6] Subindo container do banco (films-db)...
docker rm -f films-db 2>nul
docker run -d ^
  --name films-db ^
  --network films-net ^
  -e POSTGRES_DB=filmsdb ^
  -e POSTGRES_USER=films ^
  -e POSTGRES_PASSWORD=films123 ^
  -p 5432:5432 ^
  -v films-data:/var/lib/postgresql/data ^
  postgres:15-alpine

REM === Aguardar inicialização do banco ===
echo Aguardando inicializacao do banco...
timeout /t 10 /nobreak >nul

REM === 3. Subir a aplicação Quarkus ===
echo [3/6] Subindo aplicacao Quarkus (films-app)...
docker rm -f films-app 2>nul
docker run -d ^
  --name films-app ^
  --network films-net ^
  -p 8080:8080 ^
  -e QUARKUS_DATASOURCE_JDBC_URL=jdbc:postgresql://films-db:5432/filmsdb ^
  -e QUARKUS_DATASOURCE_USERNAME=films ^
  -e QUARKUS_DATASOURCE_PASSWORD=films123 ^
  machadotiago/films-catalogue:latest

REM === 4. Subir o Nginx como proxy reverso ===
echo [4/6] Subindo proxy reverso (films-nginx)...
docker rm -f films-nginx 2>nul
docker run -d ^
  --name films-nginx ^
  --network films-net ^
  -p 80:80 ^
  -v "%SCRIPT_DIR%nginx.conf:/etc/nginx/conf.d/default.conf:ro" ^
  nginx:alpine

REM === 5. Mostrar containers ativos ===
echo [5/6] Containers em execucao:
docker ps

echo ============================================
echo ✅ Ambiente iniciado com sucesso!
echo 🌐 Acesse: http://localhost
echo ============================================

pause
endlocal

#!/usr/bin/env python3
"""
🎬 CSV to SQL Converter - Films Catalogue
Converte todos os CSVs (movies, users, ratings) para comandos SQL INSERT

Uso: 
cd "c:\\Desenvolvimento\\14_GIT_LOCAL\\ADA\\films-catalogue"
python src\\main\\resources\\scri    movies_count = len(movie_commands    print(f"📁 Arquivo gerado: {sql_path}")
    print("")
    print("🚀 Para testar:")
    print("   mvnw quarkus:dev")
    print("   curl http://localhost:8080/movie")
    print("")
    print("📊 Para acessar views analíticas:")
    print("   SELECT * FROM vw_top_filmes_por_genero;")
    print("   SELECT * FROM vw_nota_por_faixa_etaria;")
    print("   SELECT * FROM vw_avaliacoes_por_pais;")
    print("   SELECT * FROM vw_analise_por_genero;")
    print("   SELECT * FROM vw_estatisticas_gerais;") if movie_commands else 0
    users_count = len(user_commands) - 1 if user_commands else 0
    ratings_count = len(rating_commands) - 1 if rating_commands else 0
    views_count = len([v for v in views_commands if 'CREATE OR REPLACE VIEW' in v])
    
    print("✅ Conversão concluída!")
    print("")
    print("📊 Dados importados:")
    print(f"   📽️  {movies_count} filmes")
    print(f"   👥 {users_count} usuários") 
    print(f"   ⭐ {ratings_count} avaliações")
    print(f"   📈 {views_count} views analíticas")
    print("")
    print(f"📁 Arquivo gerado: {sql_path}")
    print("")
    print("🚀 Para testar:")
    print("   mvnw quarkus:dev")
    print("   curl http://localhost:8080/movie")
    print("")
    print("📊 Para acessar views analíticas:")
    print("   SELECT * FROM vw_top_filmes_por_genero;")
    print("   SELECT * FROM vw_nota_por_faixa_etaria;")
    print("   SELECT * FROM vw_avaliacoes_por_pais;")
    print("   SELECT * FROM vw_analise_por_genero;")
    print("   SELECT * FROM vw_estatisticas_gerais;")all.py

"""

import csv
import os

def convert_movies_csv():
    """Converte movies.csv para SQL INSERT para Movie entity"""
    csv_path = "src/main/resources/data-lake/movies.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo {csv_path} não encontrado!")
        return []
    
    sql_commands = []
    sql_commands.append("-- Importação dos filmes")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            id_movie = row['id']
            titulo = row['titulo'].replace("'", "''")
            diretor = row['diretor'].replace("'", "''")
            ano = row['anoLancamento']
            genero = row['genero']
            
            sql = f"INSERT INTO Movie (id, titulo, diretor, anoLancamento, genero) VALUES ({id_movie}, '{titulo}', '{diretor}', {ano}, '{genero}');"
            sql_commands.append(sql)
    
    return sql_commands

def convert_users_csv():
    """Converte users.csv para SQL INSERT para Usuario entity"""
    csv_path = "src/main/resources/data-lake/users.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo {csv_path} não encontrado!")
        return []
    
    sql_commands = []
    sql_commands.append("-- Importação dos usuários")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            user_id = row['id']
            nome = row['nome'].replace("'", "''")
            data_nascimento = row['dataNascimento']
            pais = row['pais']
            
            sql = f"INSERT INTO Usuario (id, nome, dataNascimento, pais) VALUES ({user_id}, '{nome}', '{data_nascimento}', '{pais}');"
            sql_commands.append(sql)
    
    return sql_commands

def convert_ratings_csv():
    """Converte ratings.csv para SQL INSERT para Avaliacao entity"""
    csv_path = "src/main/resources/data-lake/ratings.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ Arquivo {csv_path} não encontrado!")
        return []
    
    sql_commands = []
    sql_commands.append("-- Importação das avaliações")
    
    with open(csv_path, 'r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        
        for row in reader:
            rating_id = row['id']
            user_id = row['user_id']
            movie_id = row['movie_id']
            nota = row['nota']
            data_avaliacao = f"{row['dataAvaliacao']} 12:00:00"  # Adicionar hora para LocalDateTime
            
            sql = f"INSERT INTO Avaliacao (id, usuario_id, movie_id, nota, dataAvaliacao) VALUES ({rating_id}, {user_id}, {movie_id}, {nota}, '{data_avaliacao}');"
            sql_commands.append(sql)
    
    return sql_commands

def add_analytical_views():
    """Adiciona views analíticas e consultas para o Data Mart"""
    views_sql = [
        "",
        "-- ===============================================",
        "-- 📊 DATA MART - VIEWS ANALÍTICAS", 
        "-- ===============================================",
        "",
        "-- 🏆 VIEW: Top 10 filmes mais bem avaliados por gênero",
        "CREATE OR REPLACE VIEW vw_top_filmes_por_genero AS",
        "WITH ranking_por_genero AS (",
        "    SELECT ",
        "        m.genero,",
        "        m.titulo,",
        "        m.diretor,",
        "        m.anoLancamento,",
        "        AVG(a.nota) as nota_media,",
        "        COUNT(a.id) as total_avaliacoes,",
        "        ROW_NUMBER() OVER (PARTITION BY m.genero ORDER BY AVG(a.nota) DESC, COUNT(a.id) DESC) as ranking",
        "    FROM Movie m",
        "    LEFT JOIN Avaliacao a ON m.id = a.movie_id",
        "    GROUP BY m.id, m.genero, m.titulo, m.diretor, m.anoLancamento",
        "    HAVING COUNT(a.id) > 0",
        ")",
        "SELECT ",
        "    genero,",
        "    ranking as posicao,",
        "    titulo,",
        "    diretor,",
        "    anoLancamento,",
        "    ROUND(nota_media, 2) as nota_media,",
        "    total_avaliacoes",
        "FROM ranking_por_genero",
        "WHERE ranking <= 10",
        "ORDER BY genero, ranking;",
        "",
        "-- 📊 VIEW: Nota média por faixa etária dos usuários",
        "CREATE OR REPLACE VIEW vw_nota_por_faixa_etaria AS",
        "SELECT ",
        "    CASE ",
        "        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 25 THEN 'Jovem (18-24)'",
        "        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 35 THEN 'Adulto Jovem (25-34)'",
        "        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 45 THEN 'Adulto (35-44)'",
        "        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 55 THEN 'Meia-idade (45-54)'",
        "        ELSE 'Sênior (55+)'",
        "    END as faixa_etaria,",
        "    COUNT(DISTINCT u.id) as total_usuarios,",
        "    COUNT(a.id) as total_avaliacoes,",
        "    ROUND(AVG(a.nota), 2) as nota_media,",
        "    MIN(a.nota) as nota_minima,",
        "    MAX(a.nota) as nota_maxima",
        "FROM Usuario u",
        "LEFT JOIN Avaliacao a ON u.id = a.usuario_id",
        "GROUP BY faixa_etaria",
        "ORDER BY nota_media DESC;",
        "",
        "-- 🌍 VIEW: Número de avaliações por país",
        "CREATE OR REPLACE VIEW vw_avaliacoes_por_pais AS",
        "SELECT ",
        "    u.pais,",
        "    COUNT(DISTINCT u.id) as total_usuarios,",
        "    COUNT(a.id) as total_avaliacoes,",
        "    ROUND(AVG(a.nota), 2) as nota_media,",
        "    ROUND(COUNT(a.id) * 1.0 / COUNT(DISTINCT u.id), 1) as avaliacoes_por_usuario,",
        "    COUNT(DISTINCT a.movie_id) as filmes_distintos_assistidos",
        "FROM Usuario u",
        "LEFT JOIN Avaliacao a ON u.id = a.usuario_id",
        "GROUP BY u.pais",
        "ORDER BY total_avaliacoes DESC;",
        "",
        "-- 🎭 VIEW: Análise por gênero de filme",
        "CREATE OR REPLACE VIEW vw_analise_por_genero AS",
        "SELECT ",
        "    m.genero,",
        "    COUNT(DISTINCT m.id) as total_filmes,",
        "    COUNT(a.id) as total_avaliacoes,",
        "    ROUND(AVG(a.nota), 2) as nota_media,",
        "    ROUND(COUNT(a.id) * 1.0 / COUNT(DISTINCT m.id), 1) as avaliacoes_por_filme,",
        "    MIN(m.anoLancamento) as ano_mais_antigo,",
        "    MAX(m.anoLancamento) as ano_mais_recente",
        "FROM Movie m",
        "LEFT JOIN Avaliacao a ON m.id = a.movie_id",
        "GROUP BY m.genero",
        "ORDER BY nota_media DESC;",
        "",
        "-- 📈 VIEW: Estatísticas gerais do sistema",
        "CREATE OR REPLACE VIEW vw_estatisticas_gerais AS",
        "SELECT ",
        "    'Total de Filmes' as metrica, ",
        "    COUNT(*)::text as valor ",
        "FROM Movie",
        "UNION ALL",
        "SELECT ",
        "    'Total de Usuários', ",
        "    COUNT(*)::text ",
        "FROM Usuario",
        "UNION ALL",
        "SELECT ",
        "    'Total de Avaliações', ",
        "    COUNT(*)::text ",
        "FROM Avaliacao",
        "UNION ALL",
        "SELECT ",
        "    'Nota Média Geral', ",
        "    ROUND(AVG(nota), 2)::text ",
        "FROM Avaliacao",
        "UNION ALL",
        "SELECT ",
        "    'Gêneros Disponíveis', ",
        "    COUNT(DISTINCT genero)::text ",
        "FROM Movie",
        "UNION ALL",
        "SELECT ",
        "    'Países Representados', ",
        "    COUNT(DISTINCT pais)::text ",
        "FROM Usuario;"
    ]
    return views_sql

def main():
    print("🎬 Convertendo todos os CSVs para SQL...")
    print("📁 Processando:")
    print("   📽️ movies.csv")
    print("   👥 users.csv") 
    print("   ⭐ ratings.csv")
    print("")
    
    # Converter todos os CSVs
    all_sql_commands = []
    
    all_sql_commands.append("-- 🎬 Films Catalogue - Import SQL")
    all_sql_commands.append("-- Gerado automaticamente a partir dos CSVs do Data Lake")
    all_sql_commands.append("-- Este arquivo é executado automaticamente pelo Quarkus na inicialização")
    all_sql_commands.append("")
    
    # Movies primeiro (referenciado por outras tabelas)
    movie_commands = convert_movies_csv()
    all_sql_commands.extend(movie_commands)
    all_sql_commands.append("")
    
    # Users (referenciado por Avaliacao)
    user_commands = convert_users_csv()
    all_sql_commands.extend(user_commands)
    all_sql_commands.append("")
    
    # Ratings (depende de Movies e Users)
    rating_commands = convert_ratings_csv()
    all_sql_commands.extend(rating_commands)
    all_sql_commands.append("")
    
    # Adicionar views analíticas do Data Mart
    views_commands = add_analytical_views()
    all_sql_commands.extend(views_commands)
    
    # Escrever arquivo SQL
    sql_path = "src/main/resources/import.sql"
    with open(sql_path, 'w', encoding='utf-8') as file:
        file.write('\n'.join(all_sql_commands))
    
    movies_count = len(movie_commands) - 1 if movie_commands else 0
    users_count = len(user_commands) - 1 if user_commands else 0
    ratings_count = len(rating_commands) - 1 if rating_commands else 0
    views_count = len([v for v in views_commands if 'CREATE OR REPLACE VIEW' in v])
    
    print("✅ Conversão concluída!")
    print("")
    print("📊 Dados importados:")
    print(f"   📽️  {movies_count} filmes")
    print(f"   👥 {users_count} usuários") 
    print(f"   ⭐ {ratings_count} avaliações")
    print(f"   📈 {views_count} views analíticas")
    print("")
    print(f"📁 Arquivo gerado: {sql_path}")
    print("")
    print("� Para testar:")
    print("   mvnw quarkus:dev")
    print("   curl http://localhost:8080/movie")

if __name__ == "__main__":
    main()
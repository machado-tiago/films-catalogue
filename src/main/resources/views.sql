-- VIEW: Top 10 filmes mais bem avaliados por gênero
CREATE OR REPLACE VIEW vw_top_filmes_por_genero AS
WITH ranking_por_genero AS (
    SELECT
        m.genero,
        m.titulo,
        AVG(a.nota) as nota_media,
        COUNT(a.id) as total_avaliacoes,
        ROW_NUMBER() OVER (PARTITION BY m.genero ORDER BY AVG(a.nota) DESC, COUNT(a.id) DESC) as ranking
    FROM Movie m
    LEFT JOIN Avaliacao a ON m.id = a.movie_id
    GROUP BY m.id, m.genero, m.titulo
    HAVING COUNT(a.id) > 0
)
SELECT
    genero,
    ranking as posicao,
    titulo,
    ROUND(nota_media, 2) as nota_media,
    total_avaliacoes
FROM ranking_por_genero
WHERE ranking <= 10
ORDER BY genero, ranking;

-- VIEW: Nota média por faixa etária dos usuários
CREATE OR REPLACE VIEW vw_nota_por_faixa_etaria AS
SELECT
    CASE
        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 25 THEN 'Jovem (18-24)'
        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 35 THEN 'Adulto Jovem (25-34)'
        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 45 THEN 'Adulto (35-44)'
        WHEN EXTRACT(YEAR FROM CURRENT_DATE) - EXTRACT(YEAR FROM u.dataNascimento) < 55 THEN 'Meia-idade (45-54)'
        ELSE 'Sênior (55+)'
    END as faixa_etaria,
    COUNT(DISTINCT u.id) as total_usuarios,
    COUNT(a.id) as total_avaliacoes,
    ROUND(AVG(a.nota), 2) as nota_media,
FROM Usuario u
LEFT JOIN Avaliacao a ON u.id = a.usuario_id
GROUP BY faixa_etaria
ORDER BY nota_media DESC;

-- VIEW: Número de avaliações por país
CREATE OR REPLACE VIEW vw_avaliacoes_por_pais AS
SELECT
    u.pais,
    COUNT(a.id) as total_avaliacoes,
    COUNT(DISTINCT u.id) as total_usuarios,
    COUNT(DISTINCT a.movie_id) as filmes
FROM Usuario u
LEFT JOIN Avaliacao a ON u.id = a.usuario_id
GROUP BY u.pais
ORDER BY total_avaliacoes DESC;

-- VIEW: 5 filmes mais populares
CREATE OR REPLACE VIEW vw_top5_filmes_populares AS
SELECT
    m.titulo,
    m.diretor,
    m.anoLancamento,
    m.genero,
    COUNT(a.id) as total_avaliacoes,
    ROUND(AVG(a.nota), 2) as nota_media
FROM Movie m
JOIN Avaliacao a ON m.id = a.movie_id
GROUP BY m.id, m.titulo, m.diretor, m.anoLancamento, m.genero
ORDER BY total_avaliacoes DESC
LIMIT 5;

-- VIEW: gênero com melhor avaliação média
CREATE OR REPLACE VIEW vw_melhor_genero AS
SELECT
    m.genero,
    ROUND(AVG(a.nota), 2) as nota_media,
    COUNT(a.id) as total_avaliacoes,
    COUNT(DISTINCT m.id) as total_filmes
FROM Movie m
JOIN Avaliacao a ON m.id = a.movie_id
GROUP BY m.genero
ORDER BY nota_media DESC
LIMIT 1;

-- VIEW: país assiste mais filmes
CREATE OR REPLACE VIEW vw_pais_mais_ativo AS
SELECT
    u.pais,
    COUNT(a.id) as total_avaliacoes,
    COUNT(DISTINCT u.id) as total_usuarios,
    COUNT(DISTINCT a.movie_id) as filmes_assistidos,
    ROUND(AVG(a.nota), 2) as nota_media
FROM Usuario u
JOIN Avaliacao a ON u.id = a.usuario_id
GROUP BY u.pais
ORDER BY total_avaliacoes DESC
LIMIT 1;
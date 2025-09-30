# 🎬 Scripts - Films Catalogue
## `csv_to_sql_all.py` 
**Função:** Converte todos os CSVs do Data Lake para comandos SQL INSERT

**Entrada:**
- `data-lake/movies.csv`
- `data-lake/users.csv`
- `data-lake/ratings.csv`

**Saída:**
- `import.sql`

## 🚀 Como Usar

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
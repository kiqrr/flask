# Database configuration
# Change DB_TYPE to 'MYSQL' for local development or 'SQLSERVER' for SENAI
DB_TYPE = 'MYSQL'

# MySQL (XAMPP) configuration
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': '',  # default xampp password is empty
    'database': 'cademeupet'
}

# SQL Server configuration
SQLSERVER_CONFIG = {
    'driver': '{ODBC Driver 17 for SQL Server}',
    'server': 'ALUNO33\\MSSQLSERVER03',
    'database': 'cademeupet',
    'trusted_connection': 'yes'
}

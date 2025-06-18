# Projeto de fim de semestre SENAI
## Desenvolvedores
-- Caique
-- Carlos Eduardo
-- Kleber

### Objetivo do Projeto
O objetivo desse projeto é de desenvolver nossas habilidades em python e a biblioteca Flask para o desenvolvimento de um site com um banco de dados integrado utilizando a ferramenta de SQL da microsoft, o SQL Server. Neste repositorio podemos encontrar diversos arquivos que demonstram as etapas de desenvolvimento de nosso banco de dados, expecificamente as tabelas conceituais e lógicas criadas usando br_modelo

### Como executar o código
1. Instalar dependências
```
pip install -r requirements.txt
```
2. Configurar banco de dados
```
MySQL (XAMPP):
Start XAMPP MySQL service
Import schema: mysql -u root < backend/mysql_schema.sql
Set DB_TYPE = 'MYSQL' in backend/config.py

SQL Server:
Set DB_TYPE = 'SQLSERVER' in backend/config.py
```
3. Rodar a aplicação (Em 2 terminais diferentes)
```
python server.py
python backend/app.py
```
4. Acessar o site
```
Por padrão: http://localhost:8000
```

### Backend:
> Python - Linguagem principal
> Flask - Framework web principal para APIs REST
> Flask-CORS - Para permitir requisições cross-origin
> pyodbc - Driver para conexão com banco de dados SQL Server
> Werkzeug - Para manipulação segura de uploads de arquivos
### Banco de Dados:
> Microsoft SQL Server - Sistema de gerenciamento de banco de dados principal
### Frontend:
> HTML5 - Estrutura das páginas
> CSS3 - Estilização
> JavaScript - Lógica do frontend
> Tailwind CSS - Framework CSS para estilização
> Font Awesome - Biblioteca de ícones
### Servidor:
> Python HTTP Server - Servidor proxy customizado (server.py) que:
> Serve arquivos estáticos do frontend na porta 8000
> Faz proxy das requisições /api/* para o backend Flask na porta 5000
> Gerencia CORS
### Ferramentas de Desenvolvimento:
> br_modelo - Para modelagem conceitual e lógica do banco de dados
### Arquitetura:
O projeto segue uma arquitetura de separação frontend/backend:

> Backend Flask (porta 5000) - API REST
> Frontend estático (porta 8000) - Interface do usuário
> Servidor proxy para integração entre frontend e backend
### Funcionalidades Principais:
> Sistema de cadastro e busca de pets perdidos/encontrados
> Upload e gerenciamento de fotos
> Filtros por localização (estado/cidade), status e outras características
> Interface responsiva
-- 1. Criar o banco de dados
CREATE DATABASE EventoGeekDB;
GO

-- 2. Usar o banco
USE EventoGeekDB;
GO

-- 3. Criar a tabela de inscrições
CREATE TABLE Inscricoes (
    id INT PRIMARY KEY IDENTITY(1,1),
    nome_completo NVARCHAR(100),
    email NVARCHAR(100),
    categoria NVARCHAR(50),
    personagem_jogo NVARCHAR(100),
    nivel_experiencia NVARCHAR(50)
);
GO

-- 4. Criar usuário com permissão total (se ainda não tiver criado)
CREATE LOGIN flask_user WITH PASSWORD = 'SenhaSegura123!';
CREATE USER flask_user FOR LOGIN flask_user;
ALTER ROLE db_owner ADD MEMBER flask_user;

SELECT*FROM Inscricoes;


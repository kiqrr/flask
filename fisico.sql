CREATE DATABASE cademeupet;
USE cademeupet;

CREATE TABLE endereco (
    Cod_endereco INT IDENTITY(1,1) PRIMARY KEY,
    Estado NVARCHAR(50) NOT NULL,
    Cidade NVARCHAR(100) NOT NULL,
    Bairro NVARCHAR(100) NOT NULL,
    Numero INT NOT NULL,
    Complemento NVARCHAR(100),
    CEP INT NOT NULL
);

CREATE TABLE usuario (
    Cod_usuario INT IDENTITY(1,1) PRIMARY KEY,
    cod_endereco INT NOT NULL,
    Nome_usuario NVARCHAR(100) NOT NULL,
    sobrenome_usuario NVARCHAR(100) NOT NULL,
    telefone NVARCHAR(20),
    email NVARCHAR(150),
    CONSTRAINT FK_usuario_endereco FOREIGN KEY (cod_endereco) REFERENCES endereco(Cod_endereco)
);

CREATE TABLE pets (
    Cod_animal INT IDENTITY(1,1) PRIMARY KEY,
    cod_usuario INT NOT NULL,
    Nome_animal NVARCHAR(100) NOT NULL,
    data_registro DATE NOT NULL,
    data_perda DATE,
    data_encontro DATE,
    observacoes NVARCHAR(MAX),
    status NVARCHAR(20) NOT NULL,
    CONSTRAINT FK_pets_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(Cod_usuario),
    CONSTRAINT CK_pets_status CHECK (status IN ('perdido', 'encontrado', 'resgatado', 'adotado'))
);

-- Limpar dados existentes (se houver)
DELETE FROM pets;
DELETE FROM usuario;  
DELETE FROM endereco;

-- Resetar IDENTITY das tabelas
DBCC CHECKIDENT ('endereco', RESEED, 0);
DBCC CHECKIDENT ('usuario', RESEED, 0); 
DBCC CHECKIDENT ('pets', RESEED, 0);

-- Inserir dados na tabela endereco
SET IDENTITY_INSERT endereco ON;
INSERT INTO endereco (Cod_endereco, Estado, Cidade, Bairro, Numero, Complemento, CEP) VALUES
(1, 'SP', 'São Paulo', 'Vila Madalena', 123, 'Apto 45', 05433020),
(2, 'SP', 'São Paulo', 'Jardins', 456, NULL, 01401001),
(3, 'SP', 'São Paulo', 'Moema', 789, 'Casa 2', 04077020),
(4, 'SP', 'São Paulo', 'Pinheiros', 321, 'Cobertura', 05422011),
(5, 'SP', 'São Paulo', 'Perdizes', 654, NULL, 05015010),
(6, 'SP', 'Campinas', 'Cambuí', 987, 'Apto 12', 13025320),
(7, 'RJ', 'Rio de Janeiro', 'Copacabana', 147, 'Apto 801', 22070900),
(8, 'MG', 'Belo Horizonte', 'Savassi', 258, NULL, 30112000),
(9, 'SP', 'Santos', 'Gonzaga', 369, 'Casa', 11055300),
(10, 'SP', 'São Paulo', 'Ipiranga', 741, 'Apto 23', 04263000);
SET IDENTITY_INSERT endereco OFF;

-- Inserir dados na tabela usuario
SET IDENTITY_INSERT usuario ON;
INSERT INTO usuario (Cod_usuario, cod_endereco, Nome_usuario, sobrenome_usuario, telefone, email) VALUES
(1, 1, 'Maria', 'Silva', '11987654321', 'maria.silva@email.com'),
(2, 2, 'João', 'Santos', '11976543210', 'joao.santos@email.com'),
(3, 3, 'Ana', 'Costa', '11965432109', 'ana.costa@email.com'),
(4, 4, 'Carlos', 'Oliveira', '11954321098', 'carlos.oliveira@email.com'),
(5, 5, 'Lucia', 'Ferreira', '11943210987', 'lucia.ferreira@email.com'),
(6, 6, 'Pedro', 'Almeida', '19987654321', 'pedro.almeida@email.com'),
(7, 7, 'Juliana', 'Rodrigues', '21987654321', 'juliana.rodrigues@email.com'),
(8, 8, 'Rafael', 'Martins', '31987654321', 'rafael.martins@email.com'),
(9, 9, 'Patricia', 'Lima', '13987654321', 'patricia.lima@email.com'),
(10, 10, 'Ricardo', 'Pereira', '11912345678', 'ricardo.pereira@email.com');
SET IDENTITY_INSERT usuario OFF;

-- Inserir dados na tabela pets
SET IDENTITY_INSERT pets ON;
INSERT INTO pets (Cod_animal, cod_usuario, Nome_animal, data_registro, data_perda, data_encontro, observacoes, status) VALUES
(1, 1, 'Rex', '2024-01-15', '2024-06-01', NULL, 'Cão golden retriever, muito dócil, usa coleira azul', 'perdido'),
(2, 2, 'Mimi', '2024-02-20', NULL, '2024-05-15', 'Gata siamesa encontrada no Parque Ibirapuera', 'encontrado'),
(3, 3, 'Thor', '2024-03-10', '2024-05-20', '2024-05-25', 'Cão pastor alemão, foi resgatado com ferimentos leves', 'resgatado'),
(4, 4, 'Luna', '2024-01-05', NULL, NULL, 'Cadela vira-lata adotada da ONG local', 'adotado'),
(5, 5, 'Bolt', '2024-04-12', '2024-06-05', NULL, 'Cão pequeno porte, muito ativo, sem coleira', 'perdido'),
(6, 6, 'Nala', '2024-02-28', NULL, '2024-04-10', 'Gata persa encontrada em Campinas', 'encontrado'),
(7, 7, 'Max', '2024-03-22', '2024-05-30', NULL, 'Cão labrador preto, muito amigável', 'perdido'),
(8, 8, 'Bella', '2024-01-18', NULL, NULL, 'Cadela adotada em feira de adoção', 'adotado'),
(9, 9, 'Simba', '2024-04-05', NULL, '2024-05-12', 'Gato laranja encontrado no centro de Santos', 'encontrado'),
(10, 10, 'Nina', '2024-02-14', '2024-06-02', '2024-06-07', 'Cadela resgatada com ajuda de bombeiros', 'resgatado'),
(11, 1, 'Toby', '2024-05-01', NULL, NULL, 'Cão adotado para fazer companhia ao Rex', 'adotado'),
(12, 3, 'Mel', '2024-03-25', '2024-06-03', NULL, 'Gata amarela, muito carinhosa, usa coleira com guizo', 'perdido'),
(13, 5, 'Bruno', '2024-04-20', NULL, '2024-05-28', 'Cão encontrado na região de Perdizes', 'encontrado'),
(14, 7, 'Lola', '2024-02-10', '2024-05-25', '2024-06-01', 'Cadela pequena resgatada de situação de risco', 'resgatado'),
(15, 9, 'Charlie', '2024-01-30', NULL, NULL, 'Cão adotado por família em Santos', 'adotado');
SET IDENTITY_INSERT pets OFF;

-- Verificar os dados inseridos
SELECT 'Total de endereços cadastrados:' AS Informacao, COUNT(*) AS Quantidade FROM endereco
UNION ALL
SELECT 'Total de usuários cadastrados:', COUNT(*) FROM usuario
UNION ALL  
SELECT 'Total de pets cadastrados:', COUNT(*) FROM pets;

-- Consulta para verificar pets por status
SELECT 
    status,
    COUNT(*) as quantidade
FROM pets 
GROUP BY status
ORDER BY quantidade DESC;

SELECT *  FROM pets;
SELECT *  FROM endereco;
SELECT *  FROM usuario;
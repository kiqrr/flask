-- Criar e usar o banco de dados
CREATE DATABASE IF NOT EXISTS cademeupet;
USE cademeupet;

-- Remover tabelas se existirem (para recriar)
DROP TABLE IF EXISTS pet_photos;
DROP TABLE IF EXISTS pets;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS endereco;

-- Criar tabela endereco
CREATE TABLE endereco (
    Cod_endereco INT AUTO_INCREMENT PRIMARY KEY,
    Estado VARCHAR(50) NOT NULL,
    Cidade VARCHAR(100) NOT NULL,
    Bairro VARCHAR(100) NOT NULL,
    Numero INT NOT NULL,
    Complemento VARCHAR(100),
    CEP INT NOT NULL
);

-- Criar tabela usuario
CREATE TABLE usuario (
    Cod_usuario INT AUTO_INCREMENT PRIMARY KEY,
    cod_endereco INT NOT NULL,
    Nome_usuario VARCHAR(100) NOT NULL,
    sobrenome_usuario VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(150),
    CONSTRAINT FK_usuario_endereco FOREIGN KEY (cod_endereco) REFERENCES endereco(Cod_endereco)
);

-- Criar tabela pets
CREATE TABLE pets (
    Cod_animal INT AUTO_INCREMENT PRIMARY KEY,
    cod_usuario INT NOT NULL,
    Nome_animal VARCHAR(100) NOT NULL,
    data_registro DATE NOT NULL,
    data_perda DATE,
    data_encontro DATE,
    observacoes TEXT,
    status VARCHAR(20) NOT NULL,
    CONSTRAINT FK_pets_usuario FOREIGN KEY (cod_usuario) REFERENCES usuario(Cod_usuario),
    CONSTRAINT CK_pets_status CHECK (status IN ('perdido', 'encontrado', 'resgatado', 'adotado'))
);

-- Criar tabela pet_photos
CREATE TABLE pet_photos (
    photo_id INT AUTO_INCREMENT PRIMARY KEY,
    pet_id INT NOT NULL,
    photo_path VARCHAR(500) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT FALSE,
    CONSTRAINT FK_pet_photos_pets FOREIGN KEY (pet_id) REFERENCES pets(Cod_animal)
);

-- Inserir dados na tabela endereco
INSERT INTO endereco (Estado, Cidade, Bairro, Numero, Complemento, CEP) VALUES
('SP', 'São Paulo', 'Vila Madalena', 123, 'Apto 45', 05433020),
('SP', 'São Paulo', 'Jardins', 456, NULL, 01401001),
('SP', 'São Paulo', 'Moema', 789, 'Casa 2', 04077020),
('SP', 'São Paulo', 'Pinheiros', 321, 'Cobertura', 05422011),
('SP', 'São Paulo', 'Perdizes', 654, NULL, 05015010),
('SP', 'Campinas', 'Cambuí', 987, 'Apto 12', 13025320),
('RJ', 'Rio de Janeiro', 'Copacabana', 147, 'Apto 801', 22070900),
('MG', 'Belo Horizonte', 'Savassi', 258, NULL, 30112000),
('SP', 'Santos', 'Gonzaga', 369, 'Casa', 11055300),
('SP', 'São Paulo', 'Ipiranga', 741, 'Apto 23', 04263000);

-- Inserir dados na tabela usuario
INSERT INTO usuario (cod_endereco, Nome_usuario, sobrenome_usuario, telefone, email) VALUES
(1, 'Maria', 'Silva', '11987654321', 'maria.silva@email.com'),
(2, 'João', 'Santos', '11976543210', 'joao.santos@email.com'),
(3, 'Ana', 'Costa', '11965432109', 'ana.costa@email.com'),
(4, 'Carlos', 'Oliveira', '11954321098', 'carlos.oliveira@email.com'),
(5, 'Lucia', 'Ferreira', '11943210987', 'lucia.ferreira@email.com'),
(6, 'Pedro', 'Almeida', '19987654321', 'pedro.almeida@email.com'),
(7, 'Juliana', 'Rodrigues', '21987654321', 'juliana.rodrigues@email.com'),
(8, 'Rafael', 'Martins', '31987654321', 'rafael.martins@email.com'),
(9, 'Patricia', 'Lima', '13987654321', 'patricia.lima@email.com'),
(10, 'Ricardo', 'Pereira', '11912345678', 'ricardo.pereira@email.com');

-- Inserir dados na tabela pets
INSERT INTO pets (cod_usuario, Nome_animal, data_registro, data_perda, data_encontro, observacoes, status) VALUES
(1, 'Rex', '2024-01-15', '2024-06-01', NULL, 'Cão golden retriever, muito dócil, usa coleira azul', 'perdido'),
(2, 'Mimi', '2024-02-20', NULL, '2024-05-15', 'Gata siamesa encontrada no Parque Ibirapuera', 'encontrado'),
(3, 'Thor', '2024-03-10', '2024-05-20', '2024-05-25', 'Cão pastor alemão, foi resgatado com ferimentos leves', 'resgatado'),
(4, 'Luna', '2024-01-05', NULL, NULL, 'Cadela vira-lata adotada da ONG local', 'adotado'),
(5, 'Bolt', '2024-04-12', '2024-06-05', NULL, 'Cão pequeno porte, muito ativo, sem coleira', 'perdido'),
(6, 'Nala', '2024-02-28', NULL, '2024-04-10', 'Gata persa encontrada em Campinas', 'encontrado'),
(7, 'Max', '2024-03-22', '2024-05-30', NULL, 'Cão labrador preto, muito amigável', 'perdido'),
(8, 'Bella', '2024-01-18', NULL, NULL, 'Cadela adotada em feira de adoção', 'adotado'),
(9, 'Simba', '2024-04-05', NULL, '2024-05-12', 'Gato laranja encontrado no centro de Santos', 'encontrado'),
(10, 'Nina', '2024-02-14', '2024-06-02', '2024-06-07', 'Cadela resgatada com ajuda de bombeiros', 'resgatado'),
(1, 'Toby', '2024-05-01', NULL, NULL, 'Cão adotado para fazer companhia ao Rex', 'adotado'),
(3, 'Mel', '2024-03-25', '2024-06-03', NULL, 'Gata amarela, muito carinhosa, usa coleira com guizo', 'perdido'),
(5, 'Bruno', '2024-04-20', NULL, '2024-05-28', 'Cão encontrado na região de Perdizes', 'encontrado'),
(7, 'Lola', '2024-02-10', '2024-05-25', '2024-06-01', 'Cadela pequena resgatada de situação de risco', 'resgatado'),
(9, 'Charlie', '2024-01-30', NULL, NULL, 'Cão adotado por família em Santos', 'adotado');

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

-- Consultar todas as tabelas
SELECT * FROM pets;
SELECT * FROM endereco;
SELECT * FROM usuario;

-- Inserir fotos para pets existentes na tabela pet_photos
INSERT INTO pet_photos (photo_id, pet_id, photo_path, is_primary) VALUES
(1, 1, '7RY3HEH2QJNTTFD7SNMFVZNRYY.jpg', TRUE),
(2, 2, '17_20250612193623113553_9d365d06-6a18-46d3-98cd-09ff208a1183.jpeg', TRUE),
(3, 3, '23_20250616203004924445_vida-de-gato.jpg', TRUE),
(4, 4, 'animais_imagem889575.jpg', TRUE),
(5, 5, 'c93ce1e212290cf4082d8d44228cff44.jpg', TRUE),
(6, 6, 'cachorro perdido 1.jpg', TRUE),
(7, 7, 'cachorro perdido.jpg', TRUE),
(8, 8, 'cachorro-perdido-topo.jpg', TRUE),
(9, 9, 'GettyImages-1553905584.jpg', TRUE),
(10, 10, 'imag.jpg', TRUE),
(11, 11, 'image.jpg', TRUE),
(12, 12, 'images.jpg', TRUE),
(13, 13, 'naom_5d49f9dbcf8bb.jpg', TRUE),
(14, 14, 'pet-gato-perdido-av-afonso-pena-tirol-theo-srd-laranja-1ano-e1681170190153.jpg', TRUE),
(15, 15, 'sumico-de-gato-que-motivou-ate-outdoor-e-recompensa-em-joinville-tem-desfecho-inusitado-1.jpg', TRUE);

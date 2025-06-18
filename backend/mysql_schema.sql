-- MySQL schema for cademeupet database
CREATE DATABASE IF NOT EXISTS cademeupet;
USE cademeupet;

CREATE TABLE endereco (
    Cod_endereco INTEGER PRIMARY KEY AUTO_INCREMENT,
    Estado VARCHAR(50) NOT NULL,
    Cidade VARCHAR(100) NOT NULL,
    Bairro VARCHAR(100) NOT NULL,
    Numero INTEGER NOT NULL,
    Complemento VARCHAR(100),
    CEP VARCHAR(8) NOT NULL
);

CREATE TABLE usuario (
    Cod_usuario INTEGER PRIMARY KEY AUTO_INCREMENT,
    cod_endereco INTEGER NOT NULL,
    Nome_usuario VARCHAR(100) NOT NULL,
    sobrenome_usuario VARCHAR(100) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    FOREIGN KEY (cod_endereco) REFERENCES endereco(Cod_endereco)
);

CREATE TABLE pets (
    Cod_animal INTEGER PRIMARY KEY AUTO_INCREMENT,
    cod_usuario INTEGER NOT NULL,
    Nome_animal VARCHAR(100) NOT NULL,
    data_registro DATE NOT NULL,
    data_perda DATE,
    data_encontro DATE,
    observacoes TEXT,
    status VARCHAR(20) NOT NULL CHECK (status IN ('perdido', 'encontrado', 'resgatado', 'adotado')),
    FOREIGN KEY (cod_usuario) REFERENCES usuario(Cod_usuario)
);

CREATE TABLE pet_photos (
    photo_id INTEGER PRIMARY KEY AUTO_INCREMENT,
    pet_id INTEGER NOT NULL,
    photo_path VARCHAR(255) NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (pet_id) REFERENCES pets(Cod_animal)
);

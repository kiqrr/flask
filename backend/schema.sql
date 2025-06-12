CREATE TABLE endereco (
    Cod_endereco INTEGER PRIMARY KEY AUTOINCREMENT,
    Estado TEXT NOT NULL,
    Cidade TEXT NOT NULL,
    Bairro TEXT NOT NULL,
    Numero INTEGER NOT NULL,
    Complemento TEXT,
    CEP INTEGER NOT NULL
);

CREATE TABLE usuario (
    Cod_usuario INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_endereco INTEGER NOT NULL,
    Nome_usuario TEXT NOT NULL,
    sobrenome_usuario TEXT NOT NULL,
    telefone TEXT,
    email TEXT,
    FOREIGN KEY (cod_endereco) REFERENCES endereco(Cod_endereco)
);

CREATE TABLE pets (
    Cod_animal INTEGER PRIMARY KEY AUTOINCREMENT,
    cod_usuario INTEGER NOT NULL,
    Nome_animal TEXT NOT NULL,
    data_registro DATE NOT NULL,
    data_perda DATE,
    data_encontro DATE,
    observacoes TEXT,
    status TEXT NOT NULL CHECK (status IN ('perdido', 'encontrado', 'resgatado', 'adotado')),
    FOREIGN KEY (cod_usuario) REFERENCES usuario(Cod_usuario)
);

CREATE TABLE pet_photos (
    photo_id INTEGER PRIMARY KEY AUTOINCREMENT,
    pet_id INTEGER NOT NULL,
    photo_path TEXT NOT NULL,
    is_primary BOOLEAN NOT NULL DEFAULT 0,
    FOREIGN KEY (pet_id) REFERENCES pets(Cod_animal)
);

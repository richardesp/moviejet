CREATE TABLE Usuario (
	nick VARCHAR(64) PRIMARY KEY,
    email VARCHAR(64) UNIQUE NOT NULL,
    nombre_y_apellidos varchar(128) NOT NULL,
    es_admin BOOLEAN NOT NULL DEFAULT FALSE
);

CREATE TABLE Pelicula ( -- DONE
	titulo VARCHAR(64) PRIMARY KEY,
    categoria varchar(64) NOT NULL,
    descripcion varchar(128) NOT NULL
);

CREATE TABLE Valoracion (
    titulo_pelicula VARCHAR(64) NOT NULL,
    puntuacion FLOAT NOT NULL,
    comentario VARCHAR(256) NOT NULL,
    nick_autor VARCHAR(64) NOT NULL,
    PRIMARY KEY(titulo_pelicula, nick_autor),
    FOREIGN KEY Critica_Usuario (nick_autor) REFERENCES Usuario (nick),
    FOREIGN KEY Critica_pelicula (titulo_pelicula) REFERENCES Pelicula (titulo)
);

CREATE TABLE Alquiler (
    titulo_pelicula VARCHAR(64) NOT NULL,
    nick_propietario VARCHAR(64) NOT NULL,
    tipo_alquiler ENUM("DIA", "SEMANA") NOT NULL,
    PRIMARY KEY(titulo_pelicula, nick_propietario),
    FOREIGN KEY Alquiler_Pelicula (titulo_pelicula) REFERENCES Pelicula (titulo),
    FOREING KEY Alquiler_Usuario (nick_propietario) REFERENCES Usuario (nick)
);


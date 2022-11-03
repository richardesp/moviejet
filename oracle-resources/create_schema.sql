DROP TABLE Usuario CASCADE CONSTRAINTS;
DROP TABLE Pelicula CASCADE CONSTRAINTS;
DROP TABLE Valoracion CASCADE CONSTRAINTS;
DROP TABLE PRoveedor CASCADE CONSTRAINTS;
DROP TABLE Alquiler CASCADE CONSTRAINTS;

CREATE TABLE Usuario
(
    nick               VARCHAR(64) PRIMARY KEY,
    email              VARCHAR(64) UNIQUE NOT NULL,
    nombre_y_apellidos varchar(128)       NOT NULL
);

CREATE TABLE Proveedor
(
    empresa  VARCHAR(64) PRIMARY KEY,
    NIF      NUMBER,
    telefono VARCHAR(32)
);

CREATE TABLE Pelicula
( -- DONE
    titulo             VARCHAR(64) PRIMARY KEY,
    categoria          varchar(64)  NOT NULL,
    descripcion        varchar(128) NOT NULL,
    empresa_proveedora VARCHAR(64)  NOT NULL,
    unidades           NUMBER       NOT NULL,
    CONSTRAINT FK_Pelicula_Proveedor FOREIGN KEY (empresa_proveedora) REFERENCES Proveedor (empresa)
);

CREATE TABLE Valoracion
(
    titulo_pelicula VARCHAR(64)  NOT NULL,
    puntuacion      FLOAT        NOT NULL,
    comentario      VARCHAR(256) NOT NULL,
    nick_autor      VARCHAR(64)  NOT NULL,
    PRIMARY KEY (titulo_pelicula, nick_autor),
    CONSTRAINT FK_Valoracion_Usuario foreign key (nick_autor) REFERENCES Usuario (nick),
    CONSTRAINT FK_Valoracion_pelicula foreign key (titulo_pelicula) REFERENCES Pelicula (titulo)
);

CREATE TABLE Alquiler
(
    titulo_pelicula  VARCHAR(64) NOT NULL,
    nick_propietario VARCHAR(64) NOT NULL,
    alquiler_inicio  DATE        NOT NULL,
    alquiler_fin     DATE        NOT NULL,
    tipo_alquiler    VARCHAR(6)  NOT NULL,
    PRIMARY KEY (titulo_pelicula, nick_propietario),
    CONSTRAINT FK_Alquiler_Pelicula foreign key (titulo_pelicula) REFERENCES Pelicula (titulo),
    CONSTRAINT FK_Alquiler_Usuario foreign key (nick_propietario) REFERENCES Usuario (nick),
    CONSTRAINT CK_TIPO_ALQUILER CHECK (tipo_alquiler in ('PLAZO', 'TOTAL'))
);


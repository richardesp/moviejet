instructions = [
    "SET FOREIGN_KEY_CHECKS = 0",
    "DROP TABLE IF EXISTS Usuario",
    "DROP TABLE IF EXISTS Pelicula",
    "DROP TABLE IF EXISTS Valoracion",
    "DROP TABLE IF EXISTS Proveedor",
    "DROP TABLE IF EXISTS Alquiler",
    "SET FOREIGN_KEY_CHECKS = 1",
    """
    CREATE TABLE Usuario (
        nick                VARCHAR(64) PRIMARY KEY,
        email               VARCHAR(64) UNIQUE NOT NULL,
        nombre_y_apellidos  VARCHAR(128)       NOT NULL
    )
    """,
    """
    CREATE TABLE Proveedor (
    empresa  VARCHAR(64) PRIMARY KEY,
    NIF      INTEGER,
    telefono VARCHAR(32)
    )
    """,
    """
    CREATE TABLE Pelicula ( 
    titulo             VARCHAR(64) PRIMARY KEY,
    categoria          varchar(64)  NOT NULL,
    descripcion        varchar(128) NOT NULL,
    empresa_proveedora VARCHAR(64)  NOT NULL,
    unidades           INT       NOT NULL,
    CONSTRAINT FOREIGN KEY (empresa_proveedora) REFERENCES Proveedor (empresa)
    )
    """,
    """
    CREATE TABLE Valoracion (
        titulo_pelicula VARCHAR(64)  NOT NULL,
        puntuacion      FLOAT        NOT NULL,
        comentario      VARCHAR(256) NOT NULL,
        nick_autor      VARCHAR(64)  NOT NULL,
        PRIMARY KEY (titulo_pelicula, nick_autor),
        CONSTRAINT FOREIGN KEY (titulo_pelicula) REFERENCES Pelicula (titulo),
        CONSTRAINT FOREIGN KEY (nick_autor) REFERENCES Usuario (nick)
    )
    """,
    """
    CREATE TABLE Alquiler (
    titulo_pelicula  VARCHAR(64) NOT NULL,
    nick_propietario VARCHAR(64) NOT NULL,
    alquiler_inicio  DATE        NOT NULL,
    alquiler_fin     DATE        NOT NULL,
    tipo_alquiler ENUM ("PLAZO", "TOTAL") NOT NULL,
    PRIMARY KEY (titulo_pelicula, nick_propietario),
    CONSTRAINT FOREIGN KEY (titulo_pelicula) REFERENCES Pelicula (titulo),
    CONSTRAINT FOREIGN KEY (nick_propietario) REFERENCES Usuario (nick)
    )
    """
]

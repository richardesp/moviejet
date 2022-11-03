INSERT INTO USUARIO
VALUES ('nicklodel', 'nicklodel@gmail.com', 'Nicolás López Delgado');
INSERT INTO USUARIO
VALUES ('javice22', 'javice@uco.es', 'Javier Casado Eliche');
INSERT INTO USUARIO
VALUES ('alvarogamingcode', 'avocado@outlook.com', 'Álvaro Cortés González');
INSERT INTO USUARIO
VALUES ('richardesp', 'richardesp@outlook.es', 'Ricardo Espantaleón Pérez');

INSERT INTO PROVEEDOR
VALUES ('Sony', 6578123, '768-312-768');
INSERT INTO PROVEEDOR
VALUES ('Warner Bros', 576172, '678-325-542');
INSERT INTO PROVEEDOR
VALUES ('Walt Disney', 568135, '957-324-361');
INSERT INTO PROVEEDOR
VALUES ('Lemendu', 671831, '957-827-231');

INSERT INTO PELICULA
VALUES ('El Padrino', 'Mafias', 'La apasionante vida de Don Vito Corleone', 'Warner Bros', 10);
INSERT INTO PELICULA
VALUES ('Piratas del Caribe', 'Piratas', 'Jack Sparrow recorriendo El Caribe', 'Walt Disney', 10);
INSERT INTO PELICULA
VALUES ('Tesis', 'Thriller', 'Un profesor redimido de Universidad esconde un oscuro presente', 'Lemendu', 10);
INSERT INTO PELICULA
VALUES ('Cars', 'Infantil', 'La aventura de Rayo McQueen en apasionantes carreras en la ruta 69', 'Walt Disney', 10);

INSERT INTO VALORACION
VALUES ('El Padrino', 9.0, 'Una de las mejores películas de la historia', 'javice22');
INSERT INTO VALORACION
VALUES ('El Padrino', 10.0, 'Mejorable, a veces me duermo', 'nicklodel');
INSERT INTO VALORACION
VALUES ('Cars', 10, 'Buenísima', 'nicklodel');
INSERT INTO VALORACION
VALUES ('Tesis', 9.5, 'Gran película del cine español', 'richardesp');

INSERT INTO ALQUILER
VALUES ('El Padrino', 'nicklodel', SYSDATE, SYSDATE + 7, 'PLAZO');
INSERT INTO ALQUILER
VALUES ('El Padrino', 'javice22', SYSDATE, SYSDATE + 7, 'PLAZO');
INSERT INTO ALQUILER
VALUES ('El Padrino', 'richardesp', SYSDATE, SYSDATE + 7, 'PLAZO');
DELETE
FROM ALQUILER
WHERE titulo_pelicula = 'El Padrino'
  AND nick_propietario = 'richardesp';
UPDATE ALQUILER
SET alquiler_fin = alquiler_fin + 7
WHERE nick_propietario = 'nicklodel';

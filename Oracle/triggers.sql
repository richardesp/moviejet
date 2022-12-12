SET SERVEROUTPUT ON;

-- Trigger 1: Trigger de auditoría para controlar los alquileres que se van realizando en la base de datos

CREATE OR REPLACE TRIGGER trigger_auditoria BEFORE INSERT OR DELETE OR UPDATE
      ON Alquiler FOR EACH ROW
DECLARE
    stock INTEGER;
BEGIN
    IF INSERTING THEN
        SELECT unidades INTO stock FROM Pelicula WHERE titulo = :new.titulo_pelicula;
    
        dbms_output.put_line(USER || ' está insertando' ||
        ' nuevo alquiler: ' || :new.titulo_pelicula || ' de ' 
        || :new.nick_propietario || ' (stock actual: ' || (stock - 1) || ')');
    ELSIF DELETING THEN
        SELECT unidades INTO stock FROM Pelicula WHERE titulo = :old.titulo_pelicula;
    
        dbms_output.put_line(USER || ' está borrando' ||
        ' antiguo alquiler: ' || :old.titulo_pelicula || ' de ' 
        || :old.nick_propietario || ' (stock actual: ' || (stock + 1) || ')');
    ELSIF UPDATING('ALQUILER_FIN') THEN
        dbms_output.put_line(USER || ' está actualizando la fecha del alquiler de la película ' || :old.titulo_pelicula || ' de ' || :old.nick_propietario ||
        ' con anterior fecha final de alquiler ' || :old.alquiler_fin || ' a la siguiente fecha ' || :new.alquiler_fin);
    END IF;
END;

-- Trigger 2: Trigger para comprobar que las inserciones de alquileres se realizen con fechas posteriores a la actual

CREATE OR REPLACE TRIGGER trigger_fecha_alquiler BEFORE INSERT OR UPDATE
    ON ALQUILER FOR EACH ROW
BEGIN
    IF :new.alquiler_fin < SYSDATE THEN
        RAISE_APPLICATION_ERROR(-20002, 'La fecha de alquiler no puede ser menor a la fecha actual');
    ELSIF :new.alquiler_fin < :new.alquiler_inicio + 1 THEN
        RAISE_APPLICATION_ERROR(-20003, 'El alquiler debe ser de al menos 1 día');
    END IF;
END;

-- Trigger 3: Trigger para comprobar que la valoración actual de una película es un número comprendido entre 0 y 10

CREATE OR REPLACE TRIGGER trigger_valoracion_pelicula BEFORE INSERT OR UPDATE
    ON Valoracion FOR EACH ROW
BEGIN
    IF :new.puntuacion < 0 OR :new.puntuacion > 10 THEN
        RAISE_APPLICATION_ERROR(-20005, 'La puntuación de la película debe estar comprendida entre 0 y 10');
    END IF;
END;

-- Trigger 4: Trigger para comprobar una restricción por clave foránea, donde en la tabla alquiler tiene que haber un usuario que debe existir en la base de datos
CREATE OR REPLACE TRIGGER trigger_alquiler_usuario BEFORE INSERT OR UPDATE
    ON ALQUILER FOR EACH ROW
DECLARE
    CURSOR usuarios_cursor IS SELECT nick FROM Usuario;
    flag BOOLEAN := False;
BEGIN   
    FOR usuario in usuarios_cursor LOOP
        IF usuario.nick = :new.nick_propietario THEN -- Como existe el usuario podemos referenciarlo mediante
        -- clave foránea
            flag := True;
        END IF;
    END LOOP;
    
    IF flag = False THEN
        RAISE_APPLICATION_ERROR(-20004, 'Violación de integridad de referencia: El usuario que va a realizar el alquiler no existe en la base de datos.');
    END IF;
END;

-- Trigger 5: Para que se pueda efectuar un alquiler, será necesario que haya stock de dicha película para posteriormente reducirlo
CREATE OR REPLACE TRIGGER trigger_stock_alquiler BEFORE INSERT 
    ON Alquiler FOR EACH ROW
DECLARE    
    stock INTEGER;
BEGIN
    SELECT unidades INTO stock FROM Pelicula WHERE titulo = :new.titulo_pelicula;

    IF stock <= 0 then
        RAISE_APPLICATION_ERROR(-20001, 'No queda stock disponible de la película solicitada');
    END IF;
    
    -- Si queda todavía stock disponible debemos actualizar la tabla
    UPDATE Pelicula SET unidades = unidades - 1 where titulo = :new.titulo_pelicula;
END;

CREATE OR REPLACE FUNCTION update_edificio(
    p_id INTEGER,
    p_nombre VARCHAR DEFAULT NULL,
    p_calle VARCHAR DEFAULT NULL,
    p_altura INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    UPDATE edificio
    SET
        nombre = COALESCE(p_nombre, nombre),
        calle = COALESCE(p_calle, calle),
        altura = COALESCE(p_altura, altura)
    WHERE id = p_id;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

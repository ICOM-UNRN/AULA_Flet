CREATE OR REPLACE FUNCTION update_evento(
    p_id INTEGER,
    p_nombre VARCHAR DEFAULT NULL,
    p_descripcion TEXT DEFAULT NULL,
    p_comienzo DATE DEFAULT NULL,
    p_fin DATE DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    UPDATE evento
    SET
        nombre = COALESCE(p_nombre, nombre),
        descripcion = COALESCE(p_descripcion, descripcion),
        comienzo = COALESCE(p_comienzo, comienzo),
        fin = COALESCE(p_fin, fin)
    WHERE id = p_id;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

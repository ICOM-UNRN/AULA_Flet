CREATE OR REPLACE FUNCTION update_recurso(
    p_id_recurso INTEGER,
    p_nombre VARCHAR DEFAULT NULL,
    p_descripcion TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    UPDATE recurso
    SET
        nombre = COALESCE(p_nombre, nombre),
        descripcion = COALESCE(p_descripcion, descripcion)
    WHERE id_recurso = p_id_recurso;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

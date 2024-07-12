CREATE OR REPLACE FUNCTION update_aula(
    p_id_aula INTEGER,
    p_nombre VARCHAR DEFAULT NULL,
    p_id_edificio INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    IF p_id_edificio IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM edificio WHERE id = p_id_edificio) THEN
            RETURN -1;
        END IF;
    END IF;

    UPDATE aula
    SET
        nombre = COALESCE(p_nombre, nombre),
        id_edificio = COALESCE(p_id_edificio, id_edificio)
    WHERE id_aula = p_id_aula;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

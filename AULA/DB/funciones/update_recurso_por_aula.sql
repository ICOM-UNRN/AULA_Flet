CREATE OR REPLACE FUNCTION update_recurso_por_aula(
    p_id_aula INTEGER,
    p_id_recurso INTEGER,
    p_cantidad INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    IF p_id_aula IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM aula WHERE id_aula = p_id_aula) THEN
            RETURN -1;
        END IF;
    END IF;

    IF p_id_recurso IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM recurso WHERE id_recurso = p_id_recurso) THEN
            RETURN -1;
        END IF;
    END IF;

    UPDATE recurso_por_aula
    SET
        cantidad = COALESCE(p_cantidad, cantidad)
    WHERE id_aula = p_id_aula AND id_recurso = p_id_recurso;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

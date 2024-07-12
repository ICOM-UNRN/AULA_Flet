CREATE OR REPLACE FUNCTION update_profesor_por_materia(
    p_id_materia INTEGER,
    p_id_profesor INTEGER,
    p_alumnos_esperados INTEGER DEFAULT NULL,
    p_tipo_clase VARCHAR DEFAULT NULL,
    p_activo BOOLEAN DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    IF p_id_materia IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM materia WHERE id = p_id_materia) THEN
            RETURN -1;
        END IF;
    END IF;

    IF p_id_profesor IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM profesor WHERE id = p_id_profesor) THEN
            RETURN -1;
        END IF;
    END IF;

    UPDATE profesor_por_materia
    SET
        alumnos_esperados = COALESCE(p_alumnos_esperados, alumnos_esperados),
        tipo_clase = COALESCE(p_tipo_clase, tipo_clase),
        activo = COALESCE(p_activo, activo)
    WHERE id_materia = p_id_materia AND id_profesor = p_id_profesor;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

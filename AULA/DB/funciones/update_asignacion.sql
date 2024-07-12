CREATE OR REPLACE FUNCTION update_asignacion(
    p_id INTEGER,
    p_id_aula INTEGER DEFAULT NULL,
    p_id_materia INTEGER DEFAULT NULL,
    p_id_evento INTEGER DEFAULT NULL,
    p_dia Tnombre DEFAULT NULL,
    p_horario_comienzo INTEGER DEFAULT NULL,
    p_horario_fin INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    IF p_id_aula IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM aula WHERE id_aula = p_id_aula) THEN
            RETURN -1;
        END IF;
    END IF;

    IF p_id_materia IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM materia WHERE id = p_id_materia) THEN
            RETURN -1;
        END IF;
    END IF;

    IF p_id_evento IS NOT NULL THEN
        IF NOT EXISTS (SELECT 1 FROM evento WHERE id = p_id_evento) THEN
            RETURN -1;
        END IF;
    END IF;

    UPDATE asignacion
    SET
        id_aula = COALESCE(p_id_aula, id_aula),
        id_materia = COALESCE(p_id_materia, id_materia),
        id_evento = COALESCE(p_id_evento, id_evento),
        dia = COALESCE(p_dia, dia),
        horario_comienzo = COALESCE(p_horario_comienzo, horario_comienzo),
        horario_fin = COALESCE(p_horario_fin, horario_fin)
    WHERE id = p_id;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

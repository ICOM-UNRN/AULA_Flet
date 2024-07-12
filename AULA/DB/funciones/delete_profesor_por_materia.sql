CREATE OR REPLACE FUNCTION delete_profesor_por_materia(
    p_id_materia INTEGER,
    p_id_profesor INTEGER
) RETURNS INTEGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM profesor_por_materia WHERE id_materia = p_id_materia AND id_profesor = p_id_profesor) THEN
        RETURN -1;
    END IF;

    DELETE FROM profesor_por_materia WHERE id_materia = p_id_materia AND id_profesor = p_id_profesor;
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

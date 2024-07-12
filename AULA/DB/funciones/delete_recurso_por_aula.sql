CREATE OR REPLACE FUNCTION delete_recurso_por_aula(
    p_id_aula INTEGER,
    p_id_recurso INTEGER
) RETURNS INTEGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM recurso_por_aula WHERE id_aula = p_id_aula AND id_recurso = p_id_recurso) THEN
        RETURN -1;
    END IF;

    DELETE FROM recurso_por_aula WHERE id_aula = p_id_aula AND id_recurso = p_id_recurso;
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

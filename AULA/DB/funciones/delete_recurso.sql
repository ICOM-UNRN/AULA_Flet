CREATE OR REPLACE FUNCTION delete_recurso(p_id_recurso INTEGER) RETURNS INTEGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM recurso WHERE id_recurso = p_id_recurso) THEN
        RETURN -1;
    END IF;

    DELETE FROM recurso WHERE id_recurso = p_id_recurso;
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

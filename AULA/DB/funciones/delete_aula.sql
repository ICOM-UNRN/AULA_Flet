CREATE OR REPLACE FUNCTION delete_aula(p_id_aula INTEGER) RETURNS INTEGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM aula WHERE id_aula = p_id_aula) THEN
        RETURN -1;
    END IF;

    DELETE FROM aula WHERE id_aula = p_id_aula;
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

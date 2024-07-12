CREATE OR REPLACE FUNCTION delete_materia(p_id INTEGER) RETURNS INTEGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM materia WHERE id = p_id) THEN
        RETURN -1;
    END IF;

    DELETE FROM materia WHERE id = p_id;
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

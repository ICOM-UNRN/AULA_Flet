CREATE OR REPLACE FUNCTION get_all_profesores_nombres()
RETURNS text[] AS $$
DECLARE
    profesor RECORD;
    profesores text[] := '{}';
BEGIN
    -- Iterar sobre cada elemento del array
    FOR profesor IN SELECT nombre FROM profesor
    LOOP
        profesores := array_append(profesores, profesor.nombre);
    END LOOP;
    
    return profesores;
END;
$$ LANGUAGE plpgsql;
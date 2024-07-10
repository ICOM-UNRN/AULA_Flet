CREATE OR REPLACE FUNCTION public.insert_profesor_por_materia(
	p_id_materia integer,
    p_id_profesor integer,
    p_alumnos_esperados integer,
    p_tipo_clase VARCHAR(50))
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_materia RECORD;
    existe_profesor RECORD;
    existe_profesor_por_materia RECORD;
BEGIN
    SELECT * FROM materia WHERE id = p_id_materia into existe_materia;

    if existe_materia is NULL then
        return 2; -- NO existe la materia
    end if;
    
    SELECT * FROM profesor WHERE id = p_id_profesor into existe_profesor;

    if existe_profesor is NULL then
        return 2; -- NO existe el profesor
    end if;

    SELECT * FROM profesor_por_materia WHERE id_materia = p_id_materia AND id_profesor = p_id_profesor AND alumnos_esperados = p_alumnos_esperados AND tipo_clase = p_tipo_clase into existe_profesor_por_materia;

    if existe_profesor_por_materia is not NULL then
        return 1; -- Ya existe el profesor de ese tipo de clase para esa materia
    end if;
    
    insert into profesor_por_materia (id_materia, id_profesor, alumnos_esperados, tipo_clase) 
    values (p_id_materia, p_id_profesor, p_alumnos_esperados, p_tipo_clase);
    return 0;
END;
$BODY$;

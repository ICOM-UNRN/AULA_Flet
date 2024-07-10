CREATE OR REPLACE FUNCTION public.insert_asignacion(
	p_id_aula integer,
    p_dia varchar,
    p_horario_comienzo integer,
    p_horario_fin integer,
	p_id_materia integer default null,
    p_id_evento integer default null)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_materia RECORD;
    existe_aula RECORD;
    existe_evento RECORD;
BEGIN
    SELECT * FROM aula WHERE id_aula = p_id_aula into existe_aula;

    if existe_aula is NULL then
        return 1; -- NO existe el aula
    end if;
    
    if p_id_materia is not null then
        SELECT * FROM materia WHERE id = p_id_materia into existe_materia;

        if existe_materia is NULL then
            return 2; -- NO existe la materia
        end if;
    end if;
    
    if p_id_evento is not null then
        SELECT * FROM evento WHERE id = p_id_evento into existe_evento;

        if existe_evento is NULL then
            return 3; -- NO existe el evento
        end if;
    end if;
    
    
    insert into asignacion (id_aula, id_materia, id_evento, dia, horario_comienzo, horario_fin) 
    values (p_id_aula, p_id_materia, p_id_evento, p_dia, p_horario_comienzo, p_horario_fin);
    return 0;
END;
$BODY$;

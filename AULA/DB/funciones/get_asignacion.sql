CREATE OR REPLACE FUNCTION get_asignacion(
    p_id_aula INTEGER,
    p_dia VARCHAR,
    p_horario_comienzo INTEGER,
    p_horario_fin INTEGER default NULL
)
RETURNS TABLE (
    id_materia integer,
    id_evento integer
) AS $$
BEGIN
    return query
    select id_materia, id_evento
    from asignacion
    where id_aula = p_id_aula
    and LOWER(dia) = LOWER(p_dia)
    and horario_comienzo = p_horario_comienzo
    and case 
        when p_horario_fin is null then true
        else horario_fin = p_horario_fin
        end;
END;
$$ LANGUAGE plpgsql;
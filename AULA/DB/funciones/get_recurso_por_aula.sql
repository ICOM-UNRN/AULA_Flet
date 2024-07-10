CREATE OR REPLACE FUNCTION get_recurso_por_aula(
    p_id_aula INTEGER default NULL,
    p_id_recurso INTEGER default NULL,
    p_cantidad INTEGER default NULL
)
RETURNS TABLE (
    id_aula INTEGER,
    id_recurso INTEGER,
    cantidad INTEGER
) AS $$
BEGIN
    return query
    select id_aula, id_recurso, cantidad
    from recurso_por_aula
    where case 
        when p_id_aula is null then true
        else id_aula = p_id_aula
        end
    and case 
        when p_id_recurso is null then true
        else id_recurso = p_id_recurso
        end
    and case 
        when p_cantidad is null then true
        else cantidad = p_cantidad
        end;
END;
$$ LANGUAGE plpgsql;
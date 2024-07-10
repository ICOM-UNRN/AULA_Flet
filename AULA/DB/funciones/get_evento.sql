CREATE OR REPLACE FUNCTION get_evento(
    p_id_evento INTEGER default NULL,
    p_nombre VARCHAR default NULL,
    p_descripcion VARCHAR default NULL,
    p_comienzo date default NULL,
    p_fin date default NULL
)
RETURNS TABLE (
    id integer,
    nombre tnombre,
    descripcion tnombre,
    comienzo date,
    fin date
) AS $$
BEGIN
    return query
    select e.id, e.nombre, e.descripcion, e.comienzo, e.fin
    from evento e
    where case 
        when p_id_evento is null then true
        else e.id = p_id_evento
        end
    and case 
        when p_nombre is null then true
        else e.nombre = p_nombre
        end
    and case 
        when p_descripcion is null then true
        else e.descripcion = p_descripcion
        end
    and case 
        when p_comienzo is null then true
        else e.comienzo = p_comienzo
        end
    and case 
        when p_fin is null then true
        else e.fin = p_fin
        end;
END;
$$ LANGUAGE plpgsql;
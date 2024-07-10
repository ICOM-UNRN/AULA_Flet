CREATE OR REPLACE FUNCTION get_recurso(
    p_id_recurso INTEGER default NULL,
    p_nombre VARCHAR default NULL,
    p_descripcion text default NULL
)
RETURNS TABLE (
    id_recurso INTEGER,
    nombre tnombre,
    descripcion text
) AS $$
BEGIN
    return query
    select id_recurso, nombre, descripcion
    from recurso
    where case 
        when p_id_recurso is null then true
        else id_recurso = p_id_recurso
        end
    and case 
        when p_nombre is null then true
        else nombre = p_nombre
        end
    and case 
        when p_descripcion is null then true
        else descripcion = p_descripcion
        end;
END;
$$ LANGUAGE plpgsql;
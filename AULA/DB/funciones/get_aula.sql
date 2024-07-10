CREATE OR REPLACE FUNCTION get_aula(
    p_id_aula INTEGER default NULL,
    p_id_edificio INTEGER default NULL,
    p_nombre VARCHAR default NULL
)
RETURNS TABLE (
    id_aula INTEGER,
    id_edificio INTEGER,
    nombre tnombre
) AS $$
BEGIN
    return query
    select id_aula, id_edificio, nombre
    from aula
    where case 
        when p_id_aula is null then true
        else id_aula = p_id_aula
        end
    and case 
        when p_id_edificio is null then true
        else id_edificio = p_id_edificio
        end
    and case 
        when p_nombre is null then true
        else nombre = p_nombre
        end;
END;
$$ LANGUAGE plpgsql;
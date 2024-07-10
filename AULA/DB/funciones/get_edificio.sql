CREATE OR REPLACE FUNCTION get_edificio(
    p_id_edificio INTEGER default NULL,
    p_nombre VARCHAR default NULL,
    p_calle VARCHAR default NULL,
    p_altura INTEGER default NULL
)
RETURNS TABLE (
    id integer,
    nombre tnombre,
    calle tnombre,
    altura integer
) AS $$
BEGIN
    return query
    select e.id, e.nombre, e.calle, e.altura
    from edificio e
    where case 
        when p_id_edificio is null then true
        else e.id = p_id_edificio
        end
    and case 
        when p_nombre is null then true
        else e.nombre = p_nombre
        end
    and case 
        when p_calle is null then true
        else e.calle = p_calle
        end
    and case 
        when p_altura is null then true
        else e.altura = p_altura
        end;
END;
$$ LANGUAGE plpgsql;
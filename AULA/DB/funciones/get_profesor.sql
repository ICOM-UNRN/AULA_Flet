CREATE OR REPLACE FUNCTION public.get_profesor(
    p_id_profesor integer default null, 
    p_documento integer default null, 
    p_nombre varchar default null, 
    p_apellido varchar default null, 
    p_condicion varchar default null, 
    p_categoria varchar default null, 
    p_dedicacion varchar default null, 
    p_periodo_a_cargo text default null
)
    RETURNS TABLE(
        id integer, 
        documento integer, 
        nombre tnombre, 
        apellido tnombre, 
        condicion tnombre, 
        categoria tnombre, 
        dedicacion tnombre, 
        periodo_a_cargo text) 
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE PARALLEL UNSAFE
    ROWS 1000

AS $BODY$
BEGIN
RETURN QUERY
    select pr.id, pr.documento, pr.nombre, pr.apellido, 
           pr.condicion, pr.categoria, pr.dedicacion, pr.periodo_a_cargo
    from profesor pr
    where case 
        when p_id_profesor is null then true
        else pr.id = p_id_profesor
        end
    and case 
        when p_documento is null then true
        else pr.documento = p_documento
        end
    and case 
        when p_nombre is null then true
        else pr.nombre = p_nombre
        end
    and case 
        when p_apellido is null then true
        else pr.apellido = p_apellido
        end
    and case 
        when p_condicion is null then true
        else pr.condicion = p_condicion
        end
    and case 
        when p_categoria is null then true
        else pr.categoria = p_categoria
        end
    and case 
        when p_dedicacion is null then true
        else pr.dedicacion = p_dedicacion
        end
    and case 
        when p_periodo_a_cargo is null then true
        else pr.periodo_a_cargo = p_periodo_a_cargo
        end;
END;
$BODY$;

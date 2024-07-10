CREATE OR REPLACE FUNCTION public.insert_recurso_por_aula(
	p_id_aula integer,
	p_id_recurso integer,
    p_cantidad integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_edificio RECORD;
    existe_aula RECORD;
    existe_recurso_por_aula RECORD;
BEGIN
    SELECT * FROM edificio WHERE id = p_edificio into existe_edificio;

    if existe_edificio is NULL then
        return 2; -- NO existe el edificio
    end if;

    SELECT * FROM aula WHERE id_aula = p_id_aula into existe_aula;

    if existe_aula is NULL then
        return 2; -- NO existe el aula
    end if;

    SELECT * FROM recurso_por_aula WHERE id_aula = p_id_aula AND id_recurso = p_id_recurso into existe_recurso_por_aula;

    if existe_recurso_por_aula is not NULL then
        return 1; -- Ya existe el recurso en ese aula
        -- se puede modificar para que agregue la nueva cantidad a la ya existente pero depende de votacion general entre integrantes del proyecto.
    end if;
    
    insert into recurso_por_aula (id_aula, id_edificio, cantidad) 
    values (p_id_aula, p_id_recurso, p_cantidad);
    return 0;
END;
$BODY$;

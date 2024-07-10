CREATE OR REPLACE FUNCTION public.insert_aula(
	p_edificio integer,
	p_nombre VARCHAR(50))
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_edificio RECORD;
    existe_aula RECORD;
BEGIN
    SELECT * FROM edificio WHERE id = p_edificio into existe_edificio;

    if existe_edificio is NULL then
        return 2; -- NO existe el edificio
    end if;
    
    SELECT * FROM aula WHERE id_edificio = p_edificio AND nombre = p_nombre into existe_aula;

    if existe_aula is not NULL then
        return 1; -- Ya existe el aula
    end if;
    
    insert into aula (id_edificio, nombre) 
    values (p_edificio, p_nombre);
    return 0;
END;
$BODY$;

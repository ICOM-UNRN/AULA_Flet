-- FUNCTION: public.insert_recurso(tnombre, text)

-- DROP FUNCTION IF EXISTS public.insert_recurso(tnombre, text);

CREATE OR REPLACE FUNCTION public.insert_recurso(
	p_nombre tnombre,
	p_descripcion text)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_recurso RECORD;
BEGIN
    SELECT * FROM recurso WHERE nombre = p_nombre into existe_recurso;
    
    if existe_recurso is not NULL then
        return 1; -- Ya existe el recurso
    end if;
    
    insert into recurso (nombre, descripcion) 
    values (p_nombre, p_descripcion);
    return 0;
END;
$BODY$;

ALTER FUNCTION public.insert_recurso(tnombre, text)
    OWNER TO "default";

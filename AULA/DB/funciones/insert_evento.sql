-- FUNCTION: public.insert_evento(character varying, text, date, date)

-- DROP FUNCTION IF EXISTS public.insert_evento(character varying, text, date, date);

CREATE OR REPLACE FUNCTION public.insert_evento(
	p_nombre character varying,
	p_descripcion text,
	p_comienzo date,
	p_fin date)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_evento RECORD;
BEGIN
    SELECT * FROM evento 
    WHERE nombre LIKE p_nombre 
    and descripcion LIKE p_descripcion
    and comienzo = p_comienzo
    and fin = p_fin    
    into existe_evento;
    
    if existe_evento is not NULL then
        return 1; -- Ya existe el evento
    end if;
    
    insert into evento (nombre, descripcion, comienzo, fin) 
    values (p_nombre, p_descripcion, p_comienzo, p_fin);
    return 0;
END;
$BODY$;

ALTER FUNCTION public.insert_evento(character varying, text, date, date)
    OWNER TO "default";

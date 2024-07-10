CREATE OR REPLACE FUNCTION public.insert_edificio(
	p_nombre VARCHAR(50),
	p_calle VARCHAR(50),
	p_altura integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_edificio RECORD;
BEGIN
    SELECT * FROM edificio 
    WHERE nombre LIKE p_nombre 
    and calle LIKE p_calle
    and altura = p_altura
    into existe_edificio;
    
    if existe_edificio is not NULL then
        return 1; -- Ya existe el edificio
    end if;
    
    insert into edificio (nombre, calle, altura) 
    values (p_nombre, p_calle, p_altura);
    return 0;
END;
$BODY$;

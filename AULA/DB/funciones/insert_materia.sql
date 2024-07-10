-- FUNCTION: public.insert_materia(character varying, character varying, character varying, integer, integer, character varying, integer)

-- DROP FUNCTION IF EXISTS public.insert_materia(character varying, character varying, character varying, integer, integer, character varying, integer);

CREATE OR REPLACE FUNCTION public.insert_materia(
	p_codigo_guarani character varying,
	p_carrera character varying,
	p_nombre character varying,
	p_anio integer,
	p_cuatrimestre integer,
	p_taxonomia character varying,
	p_horas_semanales integer,
    p_comisiones integer)
    RETURNS integer
    LANGUAGE 'plpgsql'
    COST 100
    VOLATILE SECURITY DEFINER PARALLEL UNSAFE
AS $BODY$
DECLARE
    existe_materia RECORD;
BEGIN
    SELECT * FROM materia WHERE codigo_guarani LIKE p_codigo_guarani into existe_materia;
    
    if existe_materia is not NULL then
        return 1; -- Ya existe la materia
    end if;
    
    insert into materia (codigo_guarani, carrera, nombre, anio, cuatrimestre, taxonomia, horas_semanales, comisiones) 
    values (p_codigo_guarani, p_carrera, p_nombre, p_anio, p_cuatrimestre, p_taxonomia, p_horas_semanales, p_comisiones);
    return 0;
END;
$BODY$;

ALTER FUNCTION public.insert_materia(character varying, character varying, character varying, integer, integer, character varying, integer)
    OWNER TO "default";

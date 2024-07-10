CREATE OR REPLACE FUNCTION insert_profesor(
    p_documento INTEGER,
    p_nombre VARCHAR(50),
    p_apellido VARCHAR(50),
    p_condicion VARCHAR(50),
    p_categoria VARCHAR(50),
    p_dedicacion VARCHAR(50),
    p_periodo_a_cargo VARCHAR(50))
RETURNS INTEGER
AS $$
DECLARE
    existe_profesor RECORD;
BEGIN
    SELECT * FROM profesor WHERE documento = p_documento into existe_profesor;
    
    if existe_profesor is not NULL then
        return 1; -- Ya existe el profesor
    end if;
    
    insert into profesor (documento, nombre, apellido, condicion, categoria, dedicacion, periodo_a_cargo) 
    values (p_documento, p_nombre, p_apellido, p_condicion, p_categoria, p_dedicacion, p_periodo_a_cargo);
    return 0;
END;
$$ 
SECURITY definer
LANGUAGE plpgsql;
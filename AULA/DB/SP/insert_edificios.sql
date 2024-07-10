CREATE OR REPLACE PROCEDURE insert_edificios(p_edificios_array text[])
AS $$
DECLARE
    edificio text;
    direccion text;
    altura int;
BEGIN
    -- Iterar sobre cada elemento del array
    FOREACH edificio IN ARRAY p_edificios_array
    LOOP
        SELECT split_part(edificio, ',', 1) INTO direccion;
        SELECT split_part(edificio, ',', 2)::int INTO altura;
        
        -- Insertar el registro en la tabla users
        INSERT INTO edificio (direccion, altura) VALUES (direccion, altura);
    END LOOP;
END;
$$ 
SECURITY definer
LANGUAGE plpgsql;
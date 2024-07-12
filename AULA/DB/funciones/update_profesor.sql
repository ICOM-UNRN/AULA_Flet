CREATE OR REPLACE FUNCTION update_profesor(
    p_id INTEGER,
    p_documento INTEGER DEFAULT NULL,
    p_nombre VARCHAR DEFAULT NULL,
    p_apellido VARCHAR DEFAULT NULL,
    p_condicion VARCHAR DEFAULT NULL,
    p_categoria VARCHAR DEFAULT NULL,
    p_dedicacion VARCHAR DEFAULT NULL,
    p_periodo_a_cargo TEXT DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    UPDATE profesor
    SET
        documento = COALESCE(p_documento, documento),
        nombre = COALESCE(p_nombre, nombre),
        apellido = COALESCE(p_apellido, apellido),
        condicion = COALESCE(p_condicion, condicion),
        categoria = COALESCE(p_categoria, categoria),
        dedicacion = COALESCE(p_dedicacion, dedicacion),
        periodo_a_cargo = COALESCE(p_periodo_a_cargo, periodo_a_cargo)
    WHERE id = p_id;
    
    RETURN 0;
END;
$$ LANGUAGE plpgsql;

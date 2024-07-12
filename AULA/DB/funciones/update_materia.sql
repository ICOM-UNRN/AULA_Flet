CREATE OR REPLACE FUNCTION update_materia(
    p_id INTEGER,
    p_codigo_guarani VARCHAR(50) DEFAULT NULL,
    p_carrera VARCHAR DEFAULT NULL,
    p_nombre VARCHAR DEFAULT NULL,
    p_anio INTEGER DEFAULT NULL,
    p_cuatrimestre INTEGER DEFAULT NULL,
    p_taxonomia VARCHAR DEFAULT NULL,
    p_horas_semanales INTEGER DEFAULT NULL,
    p_comisiones INTEGER DEFAULT NULL
) RETURNS INTEGER AS $$
BEGIN
    UPDATE materia
    SET
        codigo_guarani = COALESCE(p_codigo_guarani, codigo_guarani),
        carrera = COALESCE(p_carrera, carrera),
        nombre = COALESCE(p_nombre, nombre),
        anio = COALESCE(p_anio, anio),
        cuatrimestre = COALESCE(p_cuatrimestre, cuatrimestre),
        taxonomia = COALESCE(p_taxonomia, taxonomia),
        horas_semanales = COALESCE(p_horas_semanales, horas_semanales),
        comisiones = COALESCE(p_comisiones, comisiones)
    WHERE id = p_id;

    RETURN 0;
END;
$$ LANGUAGE plpgsql;

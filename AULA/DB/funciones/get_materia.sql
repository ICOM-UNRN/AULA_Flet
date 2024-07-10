CREATE OR REPLACE FUNCTION get_materia(
    p_id_materia INTEGER default NULL,
    p_codigo_guarani VARCHAR default NULL,
    p_carrera VARCHAR default NULL,
    p_nombre VARCHAR default NULL,
    p_anio INTEGER default NULL,
    p_cuatrimestre INTEGER default NULL,
    p_taxonomia VARCHAR default NULL,
    p_horas_semanales INTEGER default NULL,
    p_comisiones INTEGER default NULL
)
RETURNS TABLE (
    id INTEGER,
    codigo_guarani VARCHAR(50),
    carrera tnombre,
    nombre tnombre,
    anio INTEGER,
    cuatrimestre INTEGER,
    taxonomia tnombre,
    horas_semanales INTEGER,
    comisiones INTEGER
) AS $$
BEGIN
    return query
    select ma.id, ma.codigo_guarani, ma.carrera, ma.nombre, 
           ma.anio, ma.cuatrimestre, ma.taxonomia, ma.horas_semanales, ma.comisiones
    from materia ma
    where case 
        when p_id_materia is null then true
        else ma.id = p_id_materia
        end
    and case 
        when p_codigo_guarani is null then true
        else ma.codigo_guarani = p_codigo_guarani
        end
    and case 
        when p_carrera is null then true
        else ma.carrera = p_carrera
        end
    and case 
        when p_nombre is null then true
        else ma.nombre = p_nombre
        end
    and case 
        when p_anio is null then true
        else ma.anio = p_anio
        end
    and case 
        when p_cuatrimestre is null then true
        else ma.cuatrimestre = p_cuatrimestre
        end
    and case 
        when p_taxonomia is null then true
        else ma.taxonomia = p_taxonomia
        end
    and case 
        when p_horas_semanales is null then true
        else ma.horas_semanales = p_horas_semanales
        end
    and case 
        when p_comisiones is null then true
        else ma.comisiones = p_comisiones
        end;
END;
$$ LANGUAGE plpgsql;
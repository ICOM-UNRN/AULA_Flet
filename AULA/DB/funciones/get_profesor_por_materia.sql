CREATE OR REPLACE FUNCTION get_profesor_por_materia(
    p_id_materia INTEGER default NULL,
    p_id_profesor INTEGER default NULL,
    p_alumnos_esperados INTEGER default NULL,
    p_tipo_clase VARCHAR default NULL,
    p_activo BOOLEAN default NULL
)
RETURNS TABLE (
    id_materia INTEGER,
    id_profesor INTEGER,
    alumnos_esperados INTEGER,
    tipo_clase tnombre,
    activo BOOLEAN
) AS $$
BEGIN
    return query
    select id_materia, id_profesor, alumnos_esperados, tipo_clase, activo
    from profesor_por_materia
    where case 
        when p_id_materia is null then true
        else id_materia = p_id_materia
        end
    and case 
        when p_id_profesor is null then true
        else id_profesor = p_id_profesor
        end
    and case 
        when p_alumnos_esperados is null then true
        else alumnos_esperados = p_alumnos_esperados
        end
    and case 
        when p_tipo_clase is null then true
        else tipo_clase = p_tipo_clase
        end
    and case 
        when p_activo is null then true
        else activo = p_activo
        end;
END;
$$ LANGUAGE plpgsql;
CREATE OR REPLACE FUNCTION asignar_profesor_a_materia(
    p_codigo_guarani VARCHAR(50),
    p_documento INTEGER,
    p_alumnos_esperados INTEGER,
    p_tipo_clase VARCHAR(50))
RETURNS INTEGER
AS $$
DECLARE
    v_id_materia INTEGER;
    v_id_profesor INTEGER;
    asignacion_existe RECORD;
BEGIN
    SELECT id FROM materia 
    WHERE codigo_guarani LIKE p_codigo_guarani 
    into v_id_materia;
    
    if v_id_materia is NULL then
        return 1; -- NO existe la materia
    end if;
    
    SELECT id FROM profesor 
    WHERE documento = p_documento 
    into v_id_profesor;
    
    if v_id_profesor is NULL then
        return 2; -- NO existe el profesor
    end if;
    
    SELECT * FROM profesor_por_materia 
    WHERE id_materia = v_id_materia
    and id_profesor = v_id_profesor
    and alumnos_esperados = p_alumnos_esperados
    and tipo_clase LIKE p_tipo_clase
    into asignacion_existe;
    
    if asignacion_existe is not NULL then
        return 3; -- Ya existe esta asignación de profesor a materia
    end if;
    
    insert into profesor_por_materia (id_materia, id_profesor, alumnos_esperados, tipo_clase) 
    values (v_id_materia, v_id_profesor, p_alumnos_esperados, p_tipo_clase);
    return 0;
END;
$$ 
SECURITY definer
LANGUAGE plpgsql;
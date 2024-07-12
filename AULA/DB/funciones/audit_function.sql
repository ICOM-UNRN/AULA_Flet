CREATE OR REPLACE FUNCTION audit_function() RETURNS trigger AS $$
BEGIN
    IF (TG_OP = 'DELETE') THEN
        INSERT INTO audit_log (user_name, database_name, client_addr, operation, table_name, record_id, old_data)
        VALUES (current_user, current_database(), inet_client_addr(), TG_OP, TG_TABLE_NAME, OLD.id, row_to_json(OLD));
        RETURN OLD;
    ELSIF (TG_OP = 'INSERT') THEN
        INSERT INTO audit_log (user_name, database_name, client_addr, operation, table_name, record_id, new_data)
        VALUES (current_user, current_database(), inet_client_addr(), TG_OP, TG_TABLE_NAME, NEW.id, row_to_json(NEW));
        RETURN NEW;
    ELSIF (TG_OP = 'UPDATE') THEN
        INSERT INTO audit_log (user_name, database_name, client_addr, operation, table_name, record_id, old_data, new_data)
        VALUES (current_user, current_database(), inet_client_addr(), TG_OP, TG_TABLE_NAME, NEW.id, row_to_json(OLD), row_to_json(NEW));
        RETURN NEW;
    END IF;
END;
$$ LANGUAGE plpgsql;

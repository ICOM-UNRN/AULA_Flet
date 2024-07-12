DO $$
DECLARE
    rec RECORD;
BEGIN
    FOR rec IN
        SELECT table_name
        FROM information_schema.tables
        WHERE table_schema = 'public'
    LOOP
        EXECUTE format('CREATE TRIGGER audit_trigger
                        AFTER INSERT OR UPDATE OR DELETE
                        ON %I
                        FOR EACH ROW
                        EXECUTE FUNCTION audit_function();',
                        rec.table_name);
    END LOOP;
END;
$$;

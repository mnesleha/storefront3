def execute_sql_script(cursor, sql_script):
    # Splits the script by semicolon, handling potential empty strings at the end
    sql_statements = [s.strip() for s in sql_script.split(';') if s.strip()]
    for statement in sql_statements:
        cursor.execute(statement)

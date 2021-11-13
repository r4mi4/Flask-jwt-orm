"""
    DEFINE QUERY WE NEEDED ON THIS PROJECTS
"""

CREATE_TABLE_SQL = """IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{name}' AND xtype='U')
                                            CREATE TABLE {name} ({fields});"""
INSERT_SQL = "INSERT INTO {name} ({fields}) VALUES ({placeholders});"
SELECT_WHERE_SQL = "SELECT {fields} FROM {name} WHERE {query};"
UPDATE_WHERE_SQL = "UPDATE {name} SET {fields} WHERE {conditions}"
SQL_TYPE_MAP = {
    int: "int",
    str: "varchar(255)",
    'uniqe': "varchar(255) NOT NULL UNIQUE",
}

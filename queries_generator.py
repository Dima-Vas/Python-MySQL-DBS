received_descr = ('tfn', b'varchar(36)', 'NO', 'PRI', None, ''), \
('first_name', b'varchar(32)', 'NO', '', None, ''), \
('last_name', b'varchar(32)', 'NO', '', None, ''), \
('dob', b'date', 'YES', '', None, ''), \
('timbre', b'varchar(16)', 'YES', '', None, ''), \
('in_band', b'tinyint(1)', 'YES', '', None, '')
received_values = ('3', 'Yo', 'First', '2012-01-01', 'soprano', '1')
received_columns = ["timbre", "in_band"]

received_descr = ""
received_values = ""
received_columns = ""
received_attribute = ""
received_value = ""

attributes_where_list = []
values_where_list = []

dbname = ""
tablename = ""
descr = ""
values = ""
tablecolumns = ""


insert_query = f"INSERT INTO `database_name`.`table_name` (table_description) VALUES (values_to_insert);"
select_query = f"SELECT table_columns FROM database_name.table_name "
delete_query = f"DELETE FROM database_name.table_name "
describe_query = f"DESCRIBE database_name.table_name;"

def set_description() :
    global descr, received_descr
    descr = ""
    for i in received_descr :
        descr += f"`{i[0]}`,"
    descr = descr[:-1]

def set_values() :
    global values, received_values
    values = ""
    for i in received_values :
        values += f"'{i}',"
    values = values[:-1]

def set_tablecolumns() :
    global tablecolumns, received_value
    tablecolumns = ",".join(received_columns)

def generate_where_statement() :
    global attributes_where_list
    global values_where_list
    if len(attributes_where_list) == 0 or attributes_where_list[0]=='':
        return "WHERE 1"
    return f"WHERE (" + " AND ".join([f"`{attributes_where_list[i]}`='{values_where_list[i]}'" for i in range(len(attributes_where_list))]) + ")"

insert_fn_list = [set_description, set_values]
select_fn_list = [set_tablecolumns]
delete_fn_list = []

def update_query(query_type) :
    global insert_query
    global select_query
    global delete_query

    if not query_type : # INSERT
        for i in insert_fn_list :
            i()
        return insert_query.replace("database_name", dbname).replace("table_name", tablename).replace("table_description", descr).\
replace("values_to_insert", values)

    elif query_type == 1 : # SELECT
        for i in select_fn_list :
            i()
        return select_query.replace("database_name", dbname).replace("table_name", tablename).replace("table_columns", tablecolumns if len(tablecolumns) > 0 else "*") + generate_where_statement() + ";"

    elif query_type == 2 : # DELETE
        for i in delete_fn_list :
            i()
        return delete_query.replace("database_name", dbname).replace("table_name", tablename)  + generate_where_statement() + ";"
    elif query_type == 3 : # DESCRIBE
        return describe_query.replace("database_name", dbname).replace("table_name", tablename)

def get_query(query_type, change_data) :
    """
    0 - INSERT
    1 - SELECT
    2 - DELETE
    3 - DESCRIBE
    """
    global received_descr
    global received_values
    global received_columns
    global attributes_where_list
    global values_where_list
    global dbname
    global tablename

    dbname = change_data[0]
    tablename = change_data[1]
    if not query_type : # INSERT
        assert len(change_data) == 4
        received_descr = change_data[2]
        received_values = change_data[3]
        return update_query(query_type)

    elif query_type == 1 : # SELECT
        assert len(change_data) >= 3
        received_columns = change_data[2]
        if len(change_data) > 3 :
            attributes_where_list = change_data[3]
            values_where_list = change_data[4]
        else :
            attributes_where_list = []
            values_where_list = []
        return update_query(query_type)

    elif query_type == 2 : # DELETE
        assert len(change_data) >= 2
        if len(change_data) == 4 :
            attributes_where_list = change_data[2]
            values_where_list = change_data[3]
        else :
            attributes_where_list = []
            values_where_list = []
        return update_query(query_type)

    elif query_type == 3 : # DESCRIBE
        assert len(change_data) == 2
        return update_query(query_type)

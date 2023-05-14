from getpass import getpass
from mysql.connector import connect, Error
from queries_generator import get_query

database_name = "" # "mydb"
table_name = "" # "consumer"
inserted_values = [] # ["nn@gmail.com", "Nick", "1941-01-01"]
inserted_columns = ["*"] # ["email", "nickname"]
inserted_atributes_where_list = [] # ["email"]
inserted_values_where_list = [] # ["na@gmail.com"]

def execute_select_query(cursor, query) :
    try :
        cursor.execute(query)
    except Error : 
        print(f"Error in the query : {query}\n")
        return []
    return cursor.fetchall()

def execute_describe_query(cursor, query) :
    try :
        cursor.execute(query)
    except Error : 
        print(f"Error in the query : {query}\n")
    return cursor.fetchall()

def execute_insert_query(cursor, query) :
    try :
        cursor.execute(query)
    except Error : 
        print(f"Error in the query : {query}\n")

def execute_delete_query(cursor, query) :
    try :
        cursor.execute(query)
    except Error : 
        print(f"Error in the query : {query}\n")


def main() :
    global database_name
    global table_name
    database_name = input("Type the name of the database you want to use :\n>>> ")
    try :
        with connect(
            host="localhost",
            user=input("Enter username: "),
            password=getpass("Enter password: "), # DoctoraCuraTeIpsum
            database=database_name
        ) as connection :
            switch_table(connection)
            runtime(connection) # actually the main function
    except Error as e :
        print(e + "\n")

def insert_itself(connection) :
    cursor = connection.cursor()
    descr = execute_describe_query(cursor, get_query(3, [database_name, table_name]))
    query = get_query(0, [
        database_name,
        table_name,
        descr,
        input(f"Insert the new row data {[x[0] for x in descr]} delimited by spaces :\n>>> ").split(" ")
    ])
    execute_insert_query(cursor, query)
    connection.commit()
    return

def select_itself(connection) :
    cursor = connection.cursor()
    descr = execute_describe_query(cursor, get_query(3, [database_name, table_name]))
    to_get_list = [
        database_name,
        table_name,
        input(f"Type the columns of {[x[0] for x in descr]} delimited by spaces. If all are needed, press Enter :\n>>> ").split(" "),
        input(f"Type the properties of {[x[0] for x in descr]} you want to be conditioned delimited by spaces. If all are needed, press Enter :\n>>> ").split(" ")
    ]
    to_get_list.append(
        [] if len(to_get_list[3]) == 0 or to_get_list[3][0]=='' else 
        input(f"Insert the expected values of columns {to_get_list[3]} delimited by spaces :\n>>> ").split(" ")
    )
    query = get_query(1, to_get_list)

    show_table(execute_select_query(cursor, query))

def delete_itself(connection) :
    cursor = connection.cursor()
    descr = execute_describe_query(cursor, get_query(3, [database_name, table_name]))
    to_get_list = [
        database_name,
        table_name,
        input(f"Type the properties of {[x[0] for x in descr]} you want to be conditioned delimited by spaces. If all are needed, press Enter :\n>>> ").split(" ")
    ]
    to_get_list.append(
        [] if len(to_get_list[2]) == 0 else 
        input(f"Insert the expected values of columns {to_get_list[2]} delimited by spaces :\n>>> ").split(" ")
    )
    query = get_query(2, to_get_list)
    execute_delete_query(cursor, query)
    connection.commit()
    return

def describe_itself(connection) :
    cursor = connection.cursor()
    query = get_query(3, [
        database_name,
        table_name
    ])
    show_table(execute_describe_query(cursor, query))


def show_table(data_received) :
    global table_name
    if len(data_received) == 0 :
        return
    longest_field = [0 for x in range(len(data_received[0]))]
    output = ["" for x in range(len(data_received)+1)]

    for i in range(len(data_received)) :
        output[i+1] = list(map(lambda x:str(x), data_received[i]))

    for i in range(len(data_received[0])) :
        longest_field[i] = max(longest_field[i], max(
            [len(y[i]) for y in output[1:]]))

    for i in range(len(output)) :
        for j in range(len(output[i])) :
            output[i][j] += " " * (longest_field[j] - len(output[i][j]))
        output[i] = " | ".join(output[i])
    
        if len(output[0]) < len(output[i]):
            output[0] += "-" * (len(output[i]) - len(output[0]))
    output.append(output[0])
    print(f"---------{database_name}.{table_name}---------")
    print("\n".join(output) + "\n")

def switch_table(connection) :
    global database_name
    global table_name
    table_name = input("Type the name of the table to use :\n>>> ")
    cursor = connection.cursor()
    cursor.execute(f"SHOW TABLES LIKE '{table_name}';")
    if len(cursor.fetchall()) == 0 :
        print(f"There is no table {table_name} in database {database_name}\n")
        switch_table(connection)

def runtime(connection) :
    while True :
        print(f"---------{database_name}.{table_name}---------")
        rqt = input("Your request type (0 for INSERT, 1 for SELECT, 2 for DELETE and 3 for DESCRIBE). To switch the table, enter 4:\n>>> ")
        try :
            rqt = int(rqt)
        except ValueError :
            print(f"Wrong request type : {rqt}\n")
            continue
        if rqt == 0 : # INSERT
            insert_itself(connection)

        elif rqt == 1 : # SELECT
            select_itself(connection)

        elif rqt == 2 : # DELETE
            delete_itself(connection)

        elif rqt == 3 :
            describe_itself(connection)

        elif rqt == 4 :
            switch_table(connection)

# TODO : create an interface to input the data
if __name__=="__main__" :
    main()


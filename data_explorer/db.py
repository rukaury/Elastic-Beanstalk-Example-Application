import copy
import os
from flask import g
import mysql.connector
from mysql.connector.errors import ProgrammingError
from data_explorer import memo_dict
from data_explorer.config import Config


def query_mysql(query, args=None, dict_=False):
    """Retrieve query if memoized else execute query on connection
    stored in g.
    """
    # Check if query already cached in memo_dict
    query_pkey = _query_pkey(query, args)
    if query_pkey in memo_dict:
        # Return a deepcopy to avoid mutating and affecting future queries
        return copy.deepcopy(memo_dict[query_pkey])
    else:
        cnx = get_db(local=Config.LOCAL_DB)
        cursor = cnx.cursor(dictionary=dict_)
        cursor.execute(query, args)
        results = cursor.fetchall()
        cursor.close()
        # Save query in memo_dict for future use
        memo_dict[query_pkey] = results
        return results


def _query_pkey(query, args):
    """Append 'query' and 'args' into a string for use as a primary key
    to represent the query. No risk of SQL injection as memo_dict will
    simply store memo_dict['malicious_query'] = None.
    """
    return query + '.' + str(args)


def get_db(local):
    """Connect to db and store connection in g for
    life of request.
    """
    if 'db' not in g:
        try:
            if local:
                g.db = mysql.connector.connect(
                                            host='localhost',
                                            user=os.environ.get('DB_USER'),
                                            password=os.environ.get('DB_PASSWORD'),
                                            database=os.environ.get('DB_DATABASE_NAME')
                                        )
            else:
                g.db = mysql.connector.connect(
                                        host=os.environ.get('DB_HOST'),
                                        user=os.environ.get('DB_USER'),
                                        password=os.environ.get('DB_PASSWORD'),
                                        database=os.environ.get('DB_DATABASE_NAME')
                                    )

        except mysql.connector.Error:
            if local:
                server_connection = mysql.connector.connect(
                    host = "localhost",
                    user = os.environ.get("DB_USER"),
                    password = os.environ.get("DB_PASSWORD")
                )
            else:
                server_connection = mysql.connector.connect(
                                        host=os.environ.get('DB_HOST'),
                                        user=os.environ.get('DB_USER'),
                                        password=os.environ.get('DB_PASSWORD')
                                    )

            initialise_database(connection = server_connection)
            if local:
                g.db = mysql.connector.connect(
                    host='localhost',
                    user=os.environ.get('DB_USER'),
                    password=os.environ.get('DB_PASSWORD'),
                    database=os.environ.get('DB_DATABASE_NAME')
                )
            else:
                g.db = mysql.connector.connect(
                                        host=os.environ.get('DB_HOST'),
                                        user=os.environ.get('DB_USER'),
                                        password=os.environ.get('DB_PASSWORD'),
                                        database=os.environ.get('DB_DATABASE_NAME')
                                    )
    return g.db


def close_db(e=None):
    """Remove connection to db from g and close."""
    db = g.pop('db', None)
    if db is not None:
        db.close()


def init_app(app):
    """In factory function, register the close_db function so
    that connections closed at end of request.
    """
    app.teardown_appcontext(close_db)
    with app.app_context():
        get_db(local = Config.LOCAL_DB)

def initialise_database(local = False, connection = None):
    """
    This will initialise the database.

    WARNING: calling this method will completely erase the db

    must have a admin account on db
    """
    if connection is None:
        cnx = get_db(local)
    else:
        cnx = connection 
    cursor = cnx.cursor(dictionary = True)
    try:
        cursor.execute(
            "DROP DATABASE IF EXISTS {DB};".format(
                DB = os.environ["DB_DATABASE_NAME"]
            )
        )
        cursor.execute(
            "CREATE DATABASE {DB} CHARACTER SET utf8mb4 COLLATE utf8mb4_bin;".format(
                DB = os.environ["DB_DATABASE_NAME"]
            )
        )
        cursor.execute(
            "USE {DB};".format(
                DB = os.environ["DB_DATABASE_NAME"]
            )
        )
    except mysql.connector.Error as err:
        print(f"Failed to create database with the following error {err.msg}")
    cursor.execute("DROP TABLE IF EXISTS comments, lsr_last_year, lsr_this_year, product_info, ratings")
    from .sql_schemas.table_def import get_table_def
    tables = get_table_def()
    count = 1
    for table in tables:
        print(f"Creating table {count} of {len(tables)}: {table}")
        try:
            cursor.execute(tables[table])
        except mysql.connector.Error as err:
            print(f"An error occured creating table {table} with message {err.msg}")
        count += 1
    cnx.commit()
    cursor.close()



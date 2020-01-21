#!/usr/bin/env python
import psycopg2
from programlibrary.db_config import config
 

GET_PROGRAMS_QUERY = """select * from programs;"""
GET_PROGRAM_QUERY = """select * from public.programs where id = {};"""
GET_SECTIONS_QUERY = """select * from sections where program_id = {}"""
GET_ACTIVITIES_QUERY = """select * from activities where section_id = {}"""

def format_query(query, query_params):
    if query_params:
        return query.format(*query_params)
    else:
        return query

def makeQuery(query, *argv):
    """ Connect to the PostgreSQL database server once per query so things are as stateless / don't affect one another as much as possible"""
    conn = None
    return_value = None
    try:
        # read connection parameters
        params = config()
 
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params)

        # create a cursor
        cur = conn.cursor()

        db_query = format_query(query, argv)

        print("executing: " , db_query)
        
        # execute a statement
        cur.execute(db_query)
 
        return_value = cur.fetchall()
       
       # close the communication with the PostgreSQL
        cur.close()
        
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
    return return_value
    
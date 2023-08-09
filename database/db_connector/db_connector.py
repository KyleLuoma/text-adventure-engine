import json
import pandas as pd
from collections import defaultdict

class db_connector:
    def __init__(self):
        pass
    def do_query(self, query):
        pass
    def close_connection(self):
        pass


class sql_server_connector(db_connector):

    def __init__(self):
        import pyodbc
        f = open('./.local/sql_server.json')
        sql_server_params = json.load(f)
        f.close()
        self.con = pyodbc.connect(sql_server_params['sql_server_connect_params'])
        self.cur = self.con.cursor()

    


class sqlite_connector(db_connector):

    def __init__(self, db_path):
        import sqlite3
        self.db_path = db_path
        self.con = sqlite3.connect(self.db_path)
        self.con.text_factory = lambda b: b.decode(errors = 'ignore')
        self.cur = self.con.cursor()

    def do_query(self, query):
        res = self.cur.execute(query)
        if self.cur.description != None:
            columns = [desc[0] for desc in self.cur.description]
            rows = res.fetchall()
            result_df = pd.DataFrame(data = rows, columns = columns)
        else:
            result_df = pd.DataFrame()
        self.con.commit()
        return result_df


    
class db2_connector(db_connector):

    def __init__(self):
        import ibm_db
        f = open('./.local/db2.json')
        db2_params = json.load(f)
        f.close()
        self.con = ibm_db.connect(db2_params['db2_connect_params'], "", "")

    def do_query(self, query):

        def default_value():
            return []

        stmt = ibm_db.exec_immediate(self.con, query)
        dict = ibm_db.fetch_assoc(stmt)
        results = defaultdict(default_value)
        while dict != False:
            for column in dict.keys():
                results[column].append(dict[column])
        result_df = pd.DataFrame(results)
        return result_df

    def close_connection(self):
        ibm_db.close(self.con)



class postgresql_connector(db_connector):

    def __init__(self):
        import psycopg2
        f = open('./.local/postgresql.json')
        postgresql_params = json.load(f)
        f.close()
        self.con = psycopg2.connect(
            host = "localhost",
            port = 5432,
            user = postgresql_params['username'],
            password = postgresql_params['password']
            )
        self.cur = self.con.cursor()

    def do_query(self, query):

        def default_value():
            return []
        self.con.commit()
        self.cur.execute(query)
        if self.cur.description == None:
            self.con.commit()
            return pd.DataFrame()
        columns = [d[0] for d in self.cur.description]
        results = self.cur.fetchall()
        result_dict = defaultdict(default_value)
        for i in range(0, len(columns)):
            for tuple in results:
                result_dict[columns[i]].append(tuple[i])
        result_df = pd.DataFrame(result_dict)
        self.con.commit()
        return result_df

    def close_connection(self):
        self.cur.close()
        self.con.close()

import pyodbc

class DBConnUtil:
    @staticmethod
    def get_connection(connection_string):
        return pyodbc.connect(connection_string)

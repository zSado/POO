import pymysql
from Credencial import credencial as c

class Conexion:
    def __init__(self):
        self.__conexion = None
        self.__cursor = None

    def conectar(self):
        self.__conexion = pymysql.connect(
            host=c['host'],
            user=c['user'],
            password=c['password'],
            database=c['database'],
            cursorclass=pymysql.cursors.DictCursor
        )
        self.__cursor = self.__conexion.cursor()
        return self.__conexion, self.__cursor

    def desconectar(self):
        if self.__conexion:
            self.__conexion.close()


    def connection(self):
        return self.__conexion


    def cursor(self):
        return self.__cursor

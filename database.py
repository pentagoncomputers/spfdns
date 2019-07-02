'''
Created on 1 Jul 2019

@author: dermot@pentagoncomputers.com
@copyright: Pentagon Computers Ltd, 2019.
'''


import mysql.connector  # pip install mysql-connector
import six

from settings import DB_LOCAL_DATABASE, DB_LOCAL_HOST, DB_LOCAL_PASSWORD, DB_LOCAL_USERNAME


def get_db():
    '''
    Important: you must call .close() on the connection returned here to return it to the pool.
    '''
    # in python3 we use our converter class to ensure that strings come back as strings
    # (otherwise they tend to come back as bytearray).  Note needed for python2.
    if six.PY3:
        cnx = mysql.connector.connect(converter_class=MyConverter, pool_name="mypool",
                                      pool_size=4, user=DB_LOCAL_USERNAME,
                                      password=DB_LOCAL_PASSWORD, database=DB_LOCAL_DATABASE,
                                      host=DB_LOCAL_HOST)
    else:
        cnx = mysql.connector.connect(pool_name="mypool_local", pool_size=4,
                                      user=DB_LOCAL_USERNAME, password=DB_LOCAL_PASSWORD,
                                      database=DB_LOCAL_DATABASE, host=DB_LOCAL_HOST)
    cnx.time_zone = '+00:00' # force utc
    return cnx




class MyConverter(mysql.connector.conversion.MySQLConverter):

    def row_to_python(self, row, fields):
        row = super(MyConverter, self).row_to_python(row, fields)

        def to_unicode(col):
            if type(col) == bytearray:
                return col.decode('utf-8')
            return col

        return[to_unicode(col) for col in row]

from config import *
import pymysql


def get_mysql_conn(host=MYSQL_HOST, user=MYSQL_USER, password=MYSQL_PASSWORD, db=MYSQL_DB, charset=MYSQL_CHARSET):
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            db=db,
            charset=charset,
            # cursorclass=pymysql.cursors.DictCursor
        )
        return conn
    except Exception as e:
        raise Exception('Fail on connecting to mysql! ' + e.message)

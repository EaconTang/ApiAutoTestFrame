# coding=utf-8


class Table(object):
    """
    Mysql表的增删改查抽象类，阉割版的ORM?
    """

    def __init__(self, conn, table_name):
        self.conn = conn
        self._table = table_name
        self._sql = ''

    @property
    def statement(self):
        """仅返回SQL语句"""
        return self._sql

    @property
    def result(self):
        """SELECT的查询结果集"""
        if not self._sql:
            return None
        with self.conn.cursor() as _cursor:
            _cursor.execute(self._sql)
            res = _cursor.fetchall()
        self.conn.close()
        return res

    def next(self):
        res = self.result
        for r in res:
            yield r

    def commit(self):
        """提交UPDATE/INSERT的操作"""
        if not self._sql:
            return False
        try:
            with self.conn.cursor() as _cursor:
                _cursor.execute(self._sql)
            self.conn.commit()
            self.conn.close()
            return True
        except:
            return False

    def where(self, **kwargs):
        if kwargs:
            self._sql += ' '
            self._sql += """WHERE {0}""".format(
                ' AND '.join(['{0}={1}'.format(k, v) for k, v in kwargs.iteritems()])
            )
        else:
            pass
        return self

    def to_str(self, _str):
        """
        在INSERT、UPDATE语句中，如果值是字符串，需要加单/双引号
        :param _str:
        :return:
        """
        if isinstance(_str, basestring):
            return '"{0}"'.format(self.escape_sql(_str))
        else:
            return str(_str)

    def escape_sql(self, text):
        """对于字符串的值，如果里面有单/双引号，需要转义"""
        return str(text).replace('"', '\\"').replace("'", "\\'")


class QueryTable(Table):
    """
    QueryTable(table_name).select(col1, col2).where(id=1)
    """

    def select(self, *args):
        if args:
            self._sql += """SELECT {0} FROM {1}""".format(', '.join(args), self._table)
        else:
            self._sql += """SELECT * FROM {0}""".format(self._table)
        return self


class UpdateTable(Table):
    """
    UpdateTable(table_name).set(k1=v1, k2=v2).where(id=1)
    """

    def set(self, **kwargs):
        if kwargs:
            kv_list = ['{0}={1}'.format(k, self.to_str(v)) for k, v in kwargs.iteritems()]
            self._sql += """UPDATE {0} SET {1}""".format(
                self._table,
                ', '.join(kv_list)
            )
        else:
            raise Exception('Kwargs should not be null!')
        return self


class InsertTable(Table):
    """
    InsertTable(table_name).values(k1=v1, k2=v2)
    """

    def values(self, **kwargs):
        if kwargs:
            keys = kwargs.keys()
            values = [self.to_str(kwargs.get(key)) for key in keys]
            self._sql += """INSERT INTO {0} ({1}) VALUES ({2})""".format(
                self._table,
                ', '.join(keys),
                ', '.join(values)
            )
        else:
            raise Exception('Kwargs should not be bull!')
        return self


if __name__ == '__main__':
    # print QueryTable('tsd_alert_definition').select('id', 'alertName').where(status=1).result
    print InsertTable('tsd_alert_run').values(
        id=100,
        runResultConfig='#...\n#...'
    ).commit()

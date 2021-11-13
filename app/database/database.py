"""
    simple orm :)
"""

from config import DATABASE_SETTINGS
from app.database.query import CREATE_TABLE_SQL,SELECT_WHERE_SQL,INSERT_SQL,SQL_TYPE_MAP,UPDATE_WHERE_SQL
import pymssql
import inspect


class Database:
    def __init__(self):
        self.conn = pymssql.connect(**DATABASE_SETTINGS)
        self.cur = self.conn.cursor()

    """
        execute sql coommand
    """
    def _execute(self, sql, params=None):
        if params:
            return self.cur.executemany(sql, params)
        return self.cur.execute(sql)

    """
        Create a new table if it does not exist
    """
    def create(self, table):
        self._execute(table._create_sql())

    """
        actually create a new  table when we saving a first instance ! 
    """
    def save(self, instance):
        sql, values = instance._insert_sql()
        self._execute(sql, values)
        self.conn.commit()

    """
         get data on our server
         We can use it like the code below :
            db.get(Post,title='ramin', body='ali')
    """
    def get(self, table,**kwargs):
        sql, fields = table._select_where_sql(**kwargs)
        self._execute(sql)
        row = self.cur.fetchone()
        if row:
            data = dict(zip(fields, row))
            return table(**data)
        else:
            return None
    """
        update data on our server
        We can use it like the code below :
            db.update(Post,conditions={'title':post1.title},title='ramin mahmmoo', body='ali')
    """
    def update(self,instance, conditions, **kwargs):
        sql = instance._update_where_sql(conditions,**kwargs)
        self._execute(sql)
        self.conn.commit()


class Table:
    def __init__(self, **kwargs):
        self._data = {
            'id': None,
        }
        for key, value in kwargs.items():
            self._data[key] = value

    def __getattribute__(self, key):
        _data = object.__getattribute__(self, '_data')
        # print(_data)
        if key in _data:
            return _data[key]
        return object.__getattribute__(self, key)

    @classmethod
    def _get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def _create_sql(cls):
        fields = [
            ("id", "INT NOT NULL IDENTITY(1,1) PRIMARY KEY")
        ]
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append((name, field.sql_type))
        fields = [" ".join(x) for x in fields]
        sql = CREATE_TABLE_SQL.format(name=cls._get_name(),
                                      fields=", ".join(fields))
        return sql

    def _insert_sql(self):
        cls = self.__class__
        fields = []
        placeholders = []
        values = ()
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
                values += (getattr(self, name),)
                placeholders.append('%s')
        sql = INSERT_SQL.format(name=cls._get_name(),
                                fields=", ".join(fields),
                                placeholders=", ".join(placeholders))
        return sql, [values]

    @classmethod
    def _select_where_sql(cls, **kwargs):
        fields = ['id']
        for name, field in inspect.getmembers(cls):
            if isinstance(field, Column):
                fields.append(name)
        filters = []
        for key, value in kwargs.items():
            filters.append(f"{key} LIKE '%{value}%'")
        sql = SELECT_WHERE_SQL.format(name=cls._get_name(),
                                      fields=", ".join(fields),
                                      query=" AND ".join(filters))
        return sql, fields

    @classmethod
    def _update_where_sql(cls,conditions, **kwargs):
        cond = ', '.join([f"{field_name} = '{value}'" for field_name, value in conditions.items()])
        values = []
        for key, value in kwargs.items():
            values.append(f"{key} = '{value}'")
        sql = UPDATE_WHERE_SQL.format(name=cls._get_name(),
                                        fields=", ".join(values),
                                        conditions=cond)
        return sql


class Column:
    def __init__(self, type):
        self.type = type

    """
        mange our data type 
    """
    @property
    def sql_type(self):
        return SQL_TYPE_MAP[self.type]




# class Post(Table):
#     title = Column('uniqe')
#     body = Column(str)


# db = Database()
# db.create(Post)
# post1 = Post(title='ramin mahmmoo', body='ali')
# post1.body = 'aliiiii'
# print(Post.body)
# db._execute("UPDATE {name} SET {fields} WHERE {conditions}")
# db.save(post1)
# x1 = db.get(Post,title='ramin', body='ali')
# db.update(Post,conditions={'title':post1.title},title='ramin mahmmoo', body='ali')
# print(x1.id)

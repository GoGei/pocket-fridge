from django.db import connection, connections, transaction


class Sequence(object):
    INITIAL_VALUE = 1
    MAX_SEQ_NAME = 64

    def __init__(self,
                 sequence_name,
                 initial_value=None,
                 database='default',
                 with_create=True,
                 ):
        initial_value = initial_value or self.INITIAL_VALUE
        if not sequence_name:
            raise ValueError('please, provide sequence name')

        if not (len(sequence_name) < 64):
            msg = 'Generated sequence name: %s is too long (%s), has to be no more then %s symbols!'
            raise ValueError(msg % (sequence_name, len(sequence_name), self.MAX_SEQ_NAME))

        self.sequence_name = sequence_name
        self.initial_value = initial_value
        self.database = database
        self.with_create = with_create

        if self.with_create:
            self.init_sequence()

    def init_sequence(self):
        sql = "CREATE SEQUENCE IF NOT EXISTS %s" % self.sequence_name
        if self.initial_value:
            sql += " START WITH %s" % self.initial_value
        if ';' not in sql:
            sql += ';'

        args = ()

        with transaction.atomic():
            self.exec_sql(sql=sql, args=args, database=self.database)

    @classmethod
    def exec_sql(cls, sql, args=(), database='default'):
        if database != 'default':
            cursor = connections[database].cursor()
        else:
            cursor = connection.cursor()

        cursor.execute(sql, args)

        if cursor.rowcount > 0:
            row = cursor.fetchone()
        else:
            row = None

        cursor.close()
        return row

    def get_last_value(self):
        args = (self.sequence_name,)
        sql = "SELECT last_value FROM %s;" % args

        with transaction.atomic():
            result = self.exec_sql(sql=sql, database=self.database)
            if result:
                return result[0]
            return result

    def get_next_value(self):
        sql = "SELECT nextval('%s');" % self.sequence_name

        with transaction.atomic():
            result = self.exec_sql(sql=sql, database=self.database)
            if result:
                return result[0]
            return result

    def __iter__(self):
        return self

    def __next__(self):
        return self.get_next_value()

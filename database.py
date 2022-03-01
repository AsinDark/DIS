from pymysql import connect, OperationalError, InterfaceError


class UseDatabase:
    def __init__(self, config: dict):
        self.config = config

    def __enter__(self):
        try:
            self.conn = connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except InterfaceError as err:
            return err
        except OperationalError as err:
            if err.args[0] == 1049:
                print('Invalid database name')
            if err.args[0] == 1045:
                print('Invalid user or password')
            if err.args[0] == 2003:
                print('Invalid host or port')

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            if exc_val.args[0] == 'Cursor not created':
                print('Cursor not created')
            if exc_val.args[0] == 1064:
                print('Invalid SQL syntax')
            if exc_val.args[0] == 1146:
                print('Table does not exist')
            if exc_val.args[0] == 1054:
                print('Unknown column')
            return True
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

def work_with_db(config: dict, _SQL: str):
    with UseDatabase(config) as cursor:
        if cursor is None:
            raise ValueError('Cursor not created')
            exit(1)
        else:
            cursor.execute(_SQL)
            result = []
            schema = [i[0] for i in cursor.description]
            for str in cursor.fetchall():
                result.append(dict(zip(schema, str)))
            return result

def make_update(config: dict, _SQL: str):
    with UseDatabase(config) as cursor:
        a = cursor.execute(_SQL)
    return a
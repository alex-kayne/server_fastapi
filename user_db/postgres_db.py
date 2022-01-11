import asyncpg
import asyncio
import datetime
import json


# создаю объект класса


class Connection():
    def __init__(self, database, user, password, host, port):
        self.database = database
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.pool = None


    async def connect(self):
        self.pool = await asyncpg.create_pool(database=self.database, user=self.user,
                                              password=self.password, host=self.host, port=self.port)

    # table_name = irr_ads
    async def insert(self, table_name, data):
        operand = '%s, '
        data['dt_created'] = data['dt_updated'] = datetime.datetime.now()
        placeholders = ', '.join([f'${i}' for i in range(1, len(data) + 1)])
        columns = ', '.join(data.keys())
        sql = f'''INSERT INTO %s (%s) VALUES (%s);''' % (table_name, columns, placeholders)
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    await connection.execute(sql, *[json.dumps(data) if isinstance(data, list) else data for data in data.values()])
        except asyncpg.exceptions.UniqueViolationError as err:
            return str(err)

    async def select(self, table_name, data: dict = {}):
        columns = ', '.join(data.keys())
        conditions_string = ''
        for key in data.keys():
            if isinstance(data[key], int):
                conditions_string += f'{key} = {data[key]}' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = {data[key]} and '
            elif isinstance(data[key], list):
                conditions_string += f'{key} in ({values})' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} in {values} and '
            else:
                values = data[key]
                conditions_string += f'{key} = \'{data[key]}\'' \
                    if list(data.keys()).index(key) == len(data.keys()) - 1 else f'{key} = \'{data[key]}\' and '
        sql = f'''SELECT * FROM %s WHERE %s;''' % (table_name, conditions_string) if len(data.keys()) != 0 \
            else f'''SELECT * FROM %s;''' % (table_name)
        print(sql)
        try:
            async with self.pool.acquire() as connection:
                async with connection.transaction():
                    result = await connection.fetch(sql)
            return result
        except:
            pass




    def get_connection(self):
        return self.conn

    async def update(self, table_name, data):
        pass

    async def delete(self, table_name, data):
        pass

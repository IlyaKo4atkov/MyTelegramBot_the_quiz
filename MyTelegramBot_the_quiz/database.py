import os
import ydb

YDB_ENDPOINT = os.getenv("YDB_ENDPOINT")
YDB_DATABASE = os.getenv("YDB_DATABASE")

def get_ydb_pool(ydb_endpoint, ydb_database, timeout=30):
    ydb_driver_config = ydb.DriverConfig(
        ydb_endpoint,
        ydb_database,
        credentials=ydb.credentials_from_env_variables(),
        root_certificates=ydb.load_ydb_root_certificate(),
    )

    ydb_driver = ydb.Driver(ydb_driver_config)
    ydb_driver.wait(fail_fast=True, timeout=timeout)
    return ydb.SessionPool(ydb_driver)


def _format_kwargs(kwargs):
    return {"${}".format(key): value for key, value in kwargs.items()}


# Заготовки из документации
# https://ydb.tech/en/docs/reference/ydb-sdk/example/python/#param-prepared-queries
def execute_update_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )

    return pool.retry_operation_sync(callee)


# Заготовки из документации
# https://ydb.tech/en/docs/reference/ydb-sdk/example/python/#param-prepared-queries
def execute_select_query(pool, query, **kwargs):
    def callee(session):
        prepared_query = session.prepare(query)
        result_sets = session.transaction(ydb.SerializableReadWrite()).execute(
            prepared_query, _format_kwargs(kwargs), commit_tx=True
        )
        return result_sets[0].rows

    return pool.retry_operation_sync(callee)    

# Зададим настройки базы данных 
pool = get_ydb_pool(YDB_ENDPOINT, YDB_DATABASE)


# Структура квиза
quiz_data = [
    {
        'question': 'Что такое Python?',
        'options': ['Язык программирования', 'Тип данных', 'Музыкальный инструмент', 'Змея на английском'],
        'correct_option': 0
    },
    {
        'question': 'Какой тип данных используется для хранения целых чисел?',
        'options': ['int', 'float', 'str', 'natural'],
        'correct_option': 0
    },
    {
        'question': 'В каком месяце 28 дней?',
        'options': ['В каждом', 'Январь', 'Февраль', 'Июнь', 'Июль'],
        'correct_option': 0
    },
    {
        'question': 'Какого объекта нет на рабочем столе компьютера?',
        'options': ['Панель управления', "Панель задач", "Корзина", "Сетевое окружение"],
        'correct_option': 0
    },
    {
        'question': 'Какая единица измерения не относится к измерению инфомации?',
        'options': ['герц', 'бит', 'байт', 'бод'],
        'correct_option': 0
    },
    {
        'question': 'Кто является основателем компании Microsoft?',
        'options': ['Билл Гейтс', 'Марк Цукерберг', 'Билл Клинтон', 'Стив Джобс'],
        'correct_option': 0
    },
    {
        'question': 'Какого свойства информации не существует?',
        'options': ['Турбулентность', 'Дискретность', 'Результативность', 'Детерминированность'],
        'correct_option': 0
    },
    {
        'question': 'Программа, управляющая работой внешних устройств называется',
        'options': ['Драйвер', 'Компилятор', 'Архиватор', 'Модулятор'],
        'correct_option': 0
    },
    {
        'question': 'Сколько языков программирования существует в наше время?',
        'options': ['Несколько тысяч', 'Один', '293', '550'],
        'correct_option': 0
    },
    {
        'question': 'Как называют специалистов, разрабатывающих программное обеспечение?',
        'options': ['Программистами', 'Хакерами', 'Верстальщиками', 'Системный администратор'],
        'correct_option': 0
    }]

from db.base import connect_db, commit_and_close

def check_user_exists(db_name , username):
    conn, cursor = connect_db(db_name)

    sql = "SELECT * from users where username = ?;"

    cursor.execute(sql, (username,))
    user = cursor.fetchone()
    # print(user)
    return True if user else False

# check_user_exists('../weather.db', 'asdf')


def add_user(db_name, username):
    conn, cursor = connect_db(db_name)
    sql = 'INSERT INTO users(username) VALUES (?);'
    cursor.execute(sql, (username,))
    commit_and_close(conn)


def add_weather(db_name, **weather_data):
    conn, cursor = connect_db(db_name)

    keys = ', '.join([key for key in weather_data.keys()])
    values = tuple(weather_data.values())
    _values = ', '.join(['?' for _ in range(len(weather_data.keys()))])
    sql = f'insert into weather({keys}) values ({_values})'
    cursor.execute(sql, values)
    commit_and_close(conn)
    print(keys, values)



import asyncio
import sqlite3 as sq


async def add_info_bd(name_table, *field, bd_name='bd_bot.db'):
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''INSERT INTO {name_table} VALUES(?, ?, ?, ?, ?, ?)''', field)
    db.commit()
    db.close()


async def add_info_bd_homework(name_table, *field, bd_name='bd_bot.db'):
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''INSERT INTO {name_table} VALUES(?, ?, ? )''', field)
    db.commit()
    db.close()


async def select_info_to_id(user_id, bd_name='bd_bot.db'):
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT id FROM users WHERE id = {user_id}''')
    result = cur.fetchone()
    db.close()
    return result


async def get_info_bd(name_table, *field, bd_name='bd_bot.db'):
    fields = str(field).replace('(', '').replace(')', '')
    async with sq.connect(bd_name) as db:
        cur = db.cursor()
        cur.execute(f'''SELECT {fields} FROM {name_table}''')


async def get_date_registr(id, bd_name='bd_bot.db'):
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT date_registr FROM users WHERE id = {id}''')
    resalt = cur.fetchone()
    db.close()
    return resalt[0]


async def add_info_bd_content(day, name_field, field):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    data = (field, day)
    cur.execute(f'''UPDATE content_history SET {name_field} = ? WHERE day=?''', data)
    db.commit()
    db.close()


async def fill_in_data_bd():
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT * FROM content_history''')
    resalt = cur.fetchall()
    db.close()
    return resalt


async def get_info_to_user():
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT DISTINCT id, surname, name FROM users JOIN 'users_homework' ON userId=id''')
    resalt = cur.fetchall()
    db.close()
    return resalt


async def get_homework_user_in_date(id):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT token_file, delivery_date FROM users JOIN 'users_homework' 
                    ON userId=id WHERE id = {id}''')
    resalt = cur.fetchall()
    db.close()
    return resalt


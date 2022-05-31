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


async def get_user_pay(id):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT pay FROM user_pay  WHERE id_us_pay = {id}''')
    resalt = cur.fetchone()
    db.close()
    return resalt


async def set_pay_status_yes(id):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    try:
        cur.execute(f'''INSERT INTO user_pay VALUES({id}, 1)''')
    except Exception as ex:
        cur.execute(f'''UPDATE user_pay SET pay = 1 WHERE id_us_pay={id}''')
    db.commit()
    db.close()


async def set_pay_status_none(id):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    try:
        cur.execute(f'''INSERT INTO user_pay VALUES({id}, 0)''')
    except Exception as ex:
        print(ex)
        cur.execute(f'''UPDATE user_pay SET pay = 0 WHERE id_us_pay={id}''')
    db.commit()
    db.close()



async def get_full_name_from_db(id):
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT name, surname FROM users WHERE id={id}''')
    resalt = cur.fetchone()
    db.close()
    full_name = resalt[0] + ' ' + resalt[1]

    return full_name



async def get_info_to_user_no_pay():
    bd_name = 'bd_bot.db'
    db = sq.connect(bd_name)
    cur = db.cursor()
    cur.execute(f'''SELECT id, surname, name FROM users JOIN 'user_pay' 
                        ON id=id_us_pay WHERE pay = 0''')
    resalt = cur.fetchall()
    db.close()
    return resalt




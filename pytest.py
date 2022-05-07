import sqlite3 as sq
bd_name = 'bd_bot.db'
field = (43,"sdfs", "sdfssd", 3, 3)
name_table = "users" \
             ""
db = sq.connect(bd_name)
cur = db.cursor()
#
#db.commit()
cur.execute(f'''SELECT * FROM content_history''')


print(cur.fetchmany())
db.close()
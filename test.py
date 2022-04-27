import sqlite3

db = sqlite3.connect("data/bot_db.db")

curs = db.cursor()
chan_id = 810566276182704198
elem = curs.execute(
    "SELECT delay,user_name_discriminator FROM slowmode_info WHERE channel_id = (?)",
    (chan_id,),
).fetchall()

print(elem)

elem_by_page = [elem[i : i + 5] for i in range(0, len(elem), 5)]

elem_by_page = list(
    map(lambda l: list(map(lambda i: (f"Delay: {i[0]}", i[1]), l)), elem_by_page)
)

db.close()

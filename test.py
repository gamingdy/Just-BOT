import sqlite3

db = sqlite3.connect("data/bot_db.db")

curs = db.cursor()
chan_id = 810566276182704198
elem = curs.execute(
    "SELECT delay,user_name_discriminator FROM slowmode_info WHERE channel_id = (?)",
    (chan_id,),
).fetchall()

elem_by_page = [elem[i : i + 5] for i in range(0, len(elem), 5)]

page = 0
while True:
    print(f"page {page}")
    print(elem_by_page[page])
    intpu = input("")
    if intpu == "1":
        if page == len(elem_by_page) - 1:
            continue
        page += 1
    else:
        if page == 0:
            continue
        page -= 1


db.close()

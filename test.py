import sqlite3

db = sqlite3.connect("data/bot_db.db")

curs = db.cursor()
chan_id = 810566276182704198
elem = curs.execute(
    "SELECT * FROM slowmode_info WHERE channel_id = (?)", (chan_id,)
).fetchall()

elem_by_page = {}
for i in range(0, len(elem), 5):
    t = 1 if i == 0 else (i // 5) + 1
    elem_by_page[t] = elem[i : i + 5]

page = 1
while True:
    print(f"page {page}")
    print(elem_by_page[page])
    intpu = input("")
    if intpu == "1":
        if page == len(elem_by_page):
            continue
        page += 1
    else:
        if page == 1:
            continue
        page -= 1


db.close()

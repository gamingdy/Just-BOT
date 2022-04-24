import sqlite3

def verify_db()
    sql_request = """
    CREATE TABLE "slowmode_info" (
    	"channel_id"	INTEGER,
    	"user_id"	INTEGER,
    	"delay"	INTEGER,
    	"last_slowmode"	INTEGER
    );
    """

    db = sqlite3.connect("data/bot_db.db")
    curs = db.cursor()
    try:
        curs.execute("SELECT channel_id,user_id,delay,last_slowmode FROM slowmode_info")
    except sqlite3.OperationalError:
        print("Database error")
        print("Try to create table in database")
        try:
            curs.execute(sql_request)
        except sqlite3.OperationalError:
            print("Table already exists, but an error occurred")
            print("Try to recreate table")

            curs.execute("DROP TABLE slowmode_info")
            curs.execute(sql_request)
        db.commit()


    db.close()

import sqlite3


db = sqlite3.connect("app.db")
c = db.cursor



db.close()

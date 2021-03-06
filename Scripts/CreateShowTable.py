import sqlite3

conn = sqlite3.connect("/home/pi/pishared/ShowApp/Databases/TopShows.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS TopShows")
c.execute("CREATE TABLE IF NOT EXISTS TopShows ( "
          "ShowKey INTEGER PRIMARY KEY, "
          "ShowName TEXT NOT NULL, "
          "IsNetflix INTEGER DEFAULT 0, "
          "IsHulu INTEGER DEFAULT 0);")

conn.commit()
conn.close()

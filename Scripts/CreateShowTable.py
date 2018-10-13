import sqlite3

conn = sqlite3.connect("C:\ShowApp\Databases\TopShows.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS TopShows")
c.execute("CREATE TABLE IF NOT EXISTS TopShows ( "
          "ShowKey INTEGER PRIMARY KEY, "
          "ShowName TEXT NOT NULL, "
          "IsNetflix INTEGER DEFAULT 0, "
          "IsHulu INTEGER DEFAULT 0);")

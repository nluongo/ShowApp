import sqlite3

conn = sqlite3.connect("C:\ShowApp\Databases\TopShows.db")
c = conn.cursor()

c.execute("DROP TABLE IF EXISTS Episodes")
c.execute("CREATE TABLE IF NOT EXISTS Episodes ( "
          "EpisodeKey INTEGER PRIMARY KEY, "
          "ShowName TEXT NOT NULL, "
          "OverallEpisodeNumber INTEGER, "
          "SeasonNumber INTEGER, "
          "EpisodeNumber INTEGER, "
          "EpisodeName TEXT, "
          "NetflixUrl TEXT DEFAULT NULL, "
          "HuluUrl TEXT DEFAULT NULL);")

conn.commit()
conn.close()
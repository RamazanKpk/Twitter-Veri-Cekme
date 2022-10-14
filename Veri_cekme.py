DB_Host = "localhost"
DB_Name = "Twitter Keywords"
DB_User = "postgres"
DB_Pass = "12345"

import psycopg2
import snscrape.modules.twitter as sns

DB_Connect = conn = psycopg2.connect(
    host=DB_Host,
    database=DB_Name,
    user=DB_User,
    password=DB_Pass)

cursor = conn.cursor()
maxtweet = 100
for ts,i in sns.TwitterSearchScraper("intihar").get_items():
    if ts > maxtweet:
        break
    else:
        try:
            print(i.id_str, i.from_user, i.text, i.created_at, i.user_lag, i.source)
            command = '''INSERT INTO tweet (id_str,from_user,text,created_at,user_lag,source) VALUES (%s,%s,%s,%s,%s,%s)'''
            cursor.execute(command, (i.id_str, i.from_user, i.text, i.created_at,i.user_lag, i.source))
            conn.commit()
            i += 1
        except Exception as e:
            print(e)

cursor.close()
conn.close()

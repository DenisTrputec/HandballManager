import sqlite3
import os


def create_new_database(db_name):
    db_name = 'save/' + db_name + '.db'
    if os.path.exists(db_name):
        os.remove(db_name)

    connection = sqlite3.connect(db_name)
    cursor = connection.cursor()

    cursor.execute("""CREATE TABLE nation
                    (id INTEGER PRIMARY KEY NOT NULL
                    ,name TEXT NOT NULL UNIQUE
                    ,nationality TEXT NOT NULL)
                    """)


    # cursor.execute("""CREATE TABLE person
    #                 (id INTEGER PRIMARY KEY NOT NULL
    #                 ,name TEXT NOT NULL UNIQUE
    #                 ,age INTEGER NOT NULL
    #                 ,loyalty INTEGER NOT NULL
    #                 ,nation_id INTEGER NOT NULL
    #                 ,club_id INTEGER
    #                 ,contract INTEGER
    #                 ,cost INTEGER)
    #                 """)

    connection.commit()
    connection.close()


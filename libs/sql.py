import sqlite3

def setup():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    SETUP_COMMAND = """CREATE TABLE IF NOT EXISTS game_data ( 
        wins INTEGER PRIMARY KEY, 
        loses INTEGER);"""
    SETUP_ZERO = """INSERT INTO game_data (wins, loses) VALUES (0, 0);"""
    crsr.execute(SETUP_COMMAND)
    crsr.execute(SETUP_ZERO)
    print("[DB] Done. Setup complete!")
    connection.commit()
    connection.close()
    return True

def check_if_first_time():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    try:
        crsr.execute("SELECT * FROM game_data")
        print("[DB] Found existing game data.")
        print("[DB] Assuming player has played before.")
        return False
    except sqlite3.OperationalError:
        print("[DB] Found no existing game data.")
        return True
    connection.close()

def get_data():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    crsr.execute("SELECT * FROM game_data")
    data = crsr.fetchall()
    if data:
        data = data[0]
    else:
        data = (0, 0)
    print("[DB] Requested updated data from disk.")
    connection.close()
    return data

def add_wins(values):
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    wins, loses = get_data()
    if(wins is not None):
        value = wins + values
        ADD_WINS_COMMAND = f"UPDATE game_data SET wins = {value} WHERE loses = {loses};" # sql injection, but for what purpose?
        crsr.execute(ADD_WINS_COMMAND)
        print("[DB] Done. Added a win!")
        connection.commit()
    connection.close()

def add_losses(values):
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    wins, loses = get_data()
    if(loses is not None):
        value = loses + values
        ADD_LOSS_COMMAND = f"UPDATE game_data SET loses = {value} WHERE wins = {wins};"
        crsr.execute(ADD_LOSS_COMMAND)
        print("[DB] Done. Added a loss!")
        connection.commit()
    connection.close()

def wipe_db():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    WIPE_COMMAND = "DELETE FROM game_data;"
    crsr.execute(WIPE_COMMAND)
    connection.commit()
    print("[DB] Done. All data is now wiped!")
    connection.close()

def get_ratio():
    wins, loses = get_data()
    if(wins is not None and loses is not None):
        try:
            ratio = wins / loses
            return ratio
        except ZeroDivisionError:
            return wins # good?
    else:
        return None

# setup() function is used to initialize the database storage, 
# it will hope that the database is fully cleared first, use wipe_db() or delete the database file.

# add_losses(1) function is used to add 1 loss to the database,
# i don't think add_losses(2) works, even though we don't need that (2)

# add_wins(1) function is used to add 1 win to the the database, same as the add_losses() function.

# get_data() function is used to get the data from the database, wins and the losses. Freshly from disk! 

# get_ratio() function is used to get the wins and the losses ratio, Idk for statistics purposes, i guess.

# wipe_db() function is used to drop all tables, or "delete the database".

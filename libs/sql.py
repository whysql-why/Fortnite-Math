import sqlite3
def setup():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    SETUP_COMMAND = """CREATE TABLE game_data ( 
        wins INTEGER PRIMARY KEY, 
        loses INTEGER);"""
    SETUP_ZERO = """INSERT INTO game_data (wins, loses) VALUES (0, 0);"""
    crsr.execute(SETUP_COMMAND)
    crsr.execute(SETUP_ZERO)
    print("[DB] Done. Setup complete!")
    connection.close()
    return True

def get_data():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    crsr.execute("SELECT * FROM game_data")
    data = crsr.fetchall(0)[0]
    print("[DB] Done. Returned updated data from disk.")
    connection.close() # close
    return data

def add_wins(values):
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    wins, loses = get_data() # get the new data from disk, if updated.
    if(wins != None):
        value = wins + values
        ADD_WINS_COMMAND = f"INSERT INTO game_data (wins) VALUES ({value});" # no one will think of sql injection right? why though?
        crsr.execute(ADD_WINS_COMMAND)
        print("[DB] Done. Added a win!")
        connection.close()

def add_losses(values):
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    wins, loses = get_data()
    if(loses != None):
        value = loses + values
        ADD_LOSS_COMMAND = f"INSERT INTO game_data (wins, loses) VALUES (wins, {value});"
        crsr.execute(ADD_LOSS_COMMAND)
        print("[DB] Done. Added a loss!")
        connection.close()

def wipe_db():
    connection = sqlite3.connect("stats.db")
    crsr = connection.cursor()
    print("[DB] Connected to the database")
    WIPE_COMMAND = "DELETE FROM game_data;"
    crsr.execute(WIPE_COMMAND)
    print("[DB] Done. All data is now wiped!")
    connection.close()

add_wins(1)
print(get_data())
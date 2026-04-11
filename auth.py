import sqlite3

def criar_tabelas():
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("CREATE TABLE IF NOT EXISTS users (user TEXT, password TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS fazendas (nome TEXT, user TEXT)")
    c.execute("CREATE TABLE IF NOT EXISTS talhoes (nome TEXT, user TEXT)")

    conn.commit()
    conn.close()

def cadastrar(user, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user=?", (user,))
    if c.fetchone():
        return False

    c.execute("INSERT INTO users VALUES (?,?)", (user, password))
    conn.commit()
    conn.close()
    return True

def login(user, password):
    conn = sqlite3.connect("database.db")
    c = conn.cursor()

    c.execute("SELECT * FROM users WHERE user=? AND password=?", (user, password))
    result = c.fetchone()

    conn.close()
    return result is not None
import sqlite3
import os
from datetime import datetime


def getboerse(aktion, anzahl, nick, discordid, desc=''):
    # print(aktion)
    # print(anzahl)
    # print(nick)
    # print(discordid)
    # print(desc)
    #os.remove('geld.db')
    now = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()

    #c.execute('''CREATE TABLE konto
    #                 (id integer primary key, date text, discordid text, hero text, amount real, bank real, desc text)''')

    #c.execute("INSERT INTO konto VALUES (NULL, '2019-04-30', '532616966935019530', 'Neibald Heribert', 1, 0, 'Test')  ")
    if aktion == 'g':
        inserttupel = (None, now, discordid, nick, anzahl, 0, desc)
    elif aktion == 'b':
        inserttupel = (None, now, discordid, nick, 0, anzahl, desc)
    else:
        print(
            'Error insterting values into SQLite, probably wrong aktion value')

    c.execute("INSERT INTO konto VALUES (?,?,?,?,?,?,?)", inserttupel)
    print('Inserttupel')
    print(inserttupel)
    conn.commit()

    abfragetupel = (discordid, nick)
    c.execute(
        "SELECT SUM(amount), SUM(bank) FROM konto k where k.discordid=(?) and k.hero=(?)",
        abfragetupel)
    stand = c.fetchone()

    # with conn:
    #     c.execute('SELECT * FROM konto')
    #     print(c.fetchall())
    conn.close()
    return stand

def dskboerse(anzahl, nick, discordid):

    now = datetime.today().strftime('%Y-%m-%d')
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()

    
    inserttupel = (None, now, discordid, nick, anzahl)
    c.execute("INSERT INTO DSK VALUES (?,?,?,?,?)", inserttupel)
    print('Inserttupel')
    print(inserttupel)
    conn.commit()

    abfragetupel = (discordid, nick)
    c.execute(
        "SELECT SUM(amount) FROM DSK dsk where dsk.discordid=(?) and dsk.hero=(?)",
        abfragetupel)
    stand = c.fetchone()

    conn.close()
    return stand


def dskkontoabfrage(nick, discordid):
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()

    abfragetupel = (discordid, nick)
    c.execute(
        "SELECT SUM(amount) FROM DSK k where k.discordid=(?) and k.hero=(?)",
        abfragetupel)
    stand = c.fetchone()
    conn.close()

    return stand


def kontoabfrage(nick, discordid):
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()

    abfragetupel = (discordid, nick)
    c.execute(
        "SELECT SUM(amount), SUM(bank) FROM konto k where k.discordid=(?) and k.hero=(?)",
        abfragetupel)
    stand = c.fetchone()
    conn.close()

    return stand


def gesamtkonten():
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()

    c.execute("SELECT hero, SUM(amount), SUM(bank) FROM konto GROUP BY hero")
    stand = c.fetchall()
    conn.close()

    return stand


def cleansaldo(amount):
    dukaten = amount // 100
    amount -= dukaten * 100
    silber = amount // 10
    amount -= silber * 10
    heller = amount
    return [dukaten, silber, heller]


def transaktionen(userid, nick):
    conn = sqlite3.connect('geld.db')
    c = conn.cursor()
    abfragetupel = (nick, userid)
    c.execute('''SELECT * FROM konto k WHERE k.hero=(?) and k.discordid=(?)''',
              abfragetupel)


import datetime
import sqlite3

conn = sqlite3.connect('cache.db')


# Contest Table
# id, name, start_time, duration, type, phase, prepared_by

def fetch_all_contests():
    return conn.execute('SELECT * FROM contest').fetchall()


def add_contest_to_db(params):
    query = ('INSERT OR REPLACE INTO contest '
        '(id, name, start_time, duration, type, phase, prepared_by) '
        'VALUES(?, ?, ?, ?, ?, ?, ?)')
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()


def update_other_contests():
    add_contest_to_db((
        50000, 'Google Code Jam 2020 Round 3',
        int(datetime.datetime(year=2020, month=6, day=6, hour=22).timestamp()),
        150*60, 'GCJ', 'BEFORE', None
    ))


if __name__ == '__main__':
    update_other_contests()

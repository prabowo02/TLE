import datetime
import sqlite3

conn = sqlite3.connect('cache.db')


# Contest Table
# id, name, start_time, duration, type, phase, prepared_by

def fetch_all_contests():
    return conn.execute('SELECT * FROM contest').fetchall()


def get_contest_id(name):
    conn.execute('INSERT OR REPLACE INTO contest_id_map(oj_id, link) '
                 'VALUES(?, ?)', (name,))
    return conn.execute('SELECT id FROM contest_id_map WHERE oj_id = ?', (name,)).fetchone()[0]


def add_contest_to_db(name, start_time, duration):
    conn.execute(
        'INSERT OR REPLACE INTO contest(id, name, start_time, duration, type, phase, prepared_by)'
        'VALUES(?, ?, ?, ?, ?, ?, ?)',
        (get_contest_id(name), name, start_time, duration, 'Others', 'BEFORE', None)
    )


def add_contests():
    add_contest_to_db(
        'Google Code Jam 2020 Round 3',
        int(datetime.datetime(year=2020, month=6, day=6, hour=22).timestamp()),
        150*60,
    )


def create_contest_id_table():
    conn.execute('''
        CREATE TABLE IF NOT EXISTS contest_id_map (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            oj_id VARCHAR(100) UNIQUE
        )
    ''')
    conn.execute('INSERT INTO contest_id_map VALUES(9999, "", "")')


def remove_non_cf_contests():
    conn.execute('DELETE FROM contest WHERE id >= 10000 AND id < 60000')


if __name__ == '__main__':
    remove_non_cf_contests()
    create_contest_id_table()
    add_contests()

    conn.commit()

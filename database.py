import sqlite3
import structure

con = sqlite3.connect('db.db')
cursor = con.cursor()


def get(user_id, part):
    return cursor.execute(f"SELECT {part} FROM user_info WHERE user_id = {user_id}").fetchall()[0][0]


def set_olymp(user_id):
    temp = get(user_id, 'olymp')
    if not temp:
        temp = 0
    temp = abs(temp - 1)
    cursor.execute(f'UPDATE user_info SET olymp = {temp} WHERE user_id = {user_id}')
    con.commit()
    return temp


def get_notif(user_id):
    return [int(i) for i in
            cursor.execute(f'SELECT subjects FROM user_info WHERE user_id = {user_id}').fetchall()[0][0]]


def start_command(user_id):
    if not (user_id,) in cursor.execute('SELECT user_id FROM user_info').fetchall():
        cursor.execute(f"INSERT INTO 'user_info'(user_id, subjects) VALUES('{user_id}', '{'0' * 28}')")
        con.commit()


def set_notif(user_id, subject):
    now = get_notif(user_id)
    now[subject] = abs(now[subject] - 1)

    cursor.execute(f'UPDATE user_info SET subjects = "{"".join(list(map(str, now)))}" WHERE user_id = {user_id}')
    con.commit()
    return now


def get_urls():
    return [i[0] for i in cursor.execute('SELECT url FROM sent').fetchall()]


def new_urls(urls):
    for url in urls:
        cursor.execute(f"INSERT INTO 'sent'(url) VALUES('{url}')")
    con.commit()


def send_program():
    result = {i: [] for i in structure.subjects}
    for subject in range(len(structure.subjects)):
        for i in cursor.execute('SELECT * FROM user_info').fetchall():
            if i[1][subject] == '1':
                result[structure.subjects[subject]].append(i[0])
    return result


def send_olymp():
    result = {i: [] for i in structure.subjects}
    for subject in range(len(structure.subjects)):
        for i in cursor.execute('SELECT * FROM user_info').fetchall():
            if i[1][subject] == '1' and i[2] == 1:
                result[structure.subjects[subject]].append(i[0])
    return result


if __name__ == '__main__':
    print(set_olymp(1132908805))

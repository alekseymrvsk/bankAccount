import sqlite3 as sq
from getpass import getpass
from secrets import compare_digest as compare_hash
import bcrypt as bc

global db
global sql
db = sq.connect('server.db')
sql = db.cursor()

sql.execute("""CREATE TABLE IF NOT EXISTS users (
     login TEXT,
     password TEXT,
     salt TEXT,
     cash BIGINT
)""")

db.commit()


def reg():
    user_login = input('Имя пользователя: ')
    user_password = input('Пароль: ')
    user_salt = bc.gensalt()
    user_password = bc.hashpw(user_password.encode('utf8'), user_salt)
    sql.execute(f"SELECT login FROM users WHERE login = '{user_login}'")
    if sql.fetchone() is None:
        sql.execute(f"INSERT INTO users VALUES (?,?,?,?)", (user_login, user_password, user_salt, 0))
        db.commit()
        print("Зарегистрирован")
        return user_login
    else:
        print('Такая запись уже имеется')
        return "0"



def authorization():
    user_login = input('Имя пользователя: ')
    password_hash = next(db.execute(f'select password from users where login = "{user_login}"'), [None])[0]
    user_salt = next(db.execute(f'select salt from users where login = "{user_login}"'), [None])[0]
    if password_hash:
        password = input('Пароль:')
        if compare_hash(bc.hashpw(password.encode('utf8'), user_salt), password_hash) == True:
            return user_login
    else:  # no user
        return "0"


def delete_user(user_login):
    sql.execute(f'DELETE FROM users WHERE login = "{user_login}"')
    db.commit()


def add_money(user_login):
    sql.execute(f"SELECT cash FROM users WHERE login = '{user_login}'")
    balance = sql.fetchone()[0]
    flag = input("Хотите полполнить или снять? 1 - пополнить, 2 - снять: ")
    if flag == "1":
        sum = int(input("Какую сумму хотите внести?"))
        sql.execute(f"UPDATE users SET cash = {sum + balance} WHERE login = '{user_login}'")
        db.commit()
    elif flag == "2":
        sum = int(input("Какую сумму хотите внести?"))
        if balance - sum >= 0:

            sql.execute(f"UPDATE users SET cash = {balance - sum} WHERE login = '{user_login}'")
            db.commit()
        else:
            print("Недостаточно средств!")
    else:
        print("Ошибка!")


def main():
    flag = 0
    while 0 < 1:
        regOrEnter = input("1 - регистрация, 2 - вход: ")
        if flag == 0:
            if regOrEnter == "1":
                user_login = reg()
                flag = 1
            elif regOrEnter == "2":
                user_login = authorization()
                flag = 1
            else:
                print("Ошибка")
        if flag == 1:
            operation = input("Желаете совершить операцию? 1 - да, 2 - нет: ")
            if operation == "1":
                add_money(user_login)
            elif operation == "2":
                pass




main()

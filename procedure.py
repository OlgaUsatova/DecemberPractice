import re
import mysql.connector

def check_email_address():
    # Подключение к базе данных MySQL
    conn = mysql.connector.connect(host='localhost', user='root', password='1234', database='zadanie2')
    cursor = conn.cursor()

    # Выбор всех адресов электронной почты из таблицы
    cursor.execute('SELECT email FROM customer_base')
    rows = cursor.fetchall()

    # Проверка каждого адреса на корректность
    for row in rows:
        email = row[0]
        valid = 1

        # Проверка наличия запрещенных символов [ " < > ' ]
        if re.search(r'["<>\']', email):
            valid = 0

        # Проверка структуры адреса электронной почты
        if not re.match(r'^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4}$', email):
            valid = 0

        # Вывод адреса электронной почты и признака валидности
        print(email, valid)

    # Закрытие соединения с базой данных
    cursor.close()
    conn.close()

# Вызов процедуры проверки
check_email_address()
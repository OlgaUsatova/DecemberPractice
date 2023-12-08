import mysql.connector

# Создание подключения к базе данных
connection = mysql.connector.connect(host='localhost',
                                     database='zadanie2',
                                     user='root',
                                     password='1234')

# Создание объекта курсора
cursor = connection.cursor()

# Создание триггера
trigger_query = '''
CREATE TRIGGER price_update_trigger
AFTER UPDATE ON product
FOR EACH ROW
BEGIN
    IF NEW.cost != OLD.cost THEN
        INSERT INTO historycost (product_article_number, date_change, old_price, new_price)
        VALUES (NEW.article_number, NOW(), OLD.cost, NEW.cost);
    END IF;
END
'''

# Выполнение запроса на создание триггера
cursor.execute(trigger_query)

# Применение изменений к базе данных
connection.commit()

# Закрытие подключения и курсора
cursor.close()
connection.close()
from tkinter import *
from tkinter import ttk
from tkinter.messagebox import showinfo, showerror
import pymysql
from datetime import datetime


def filter_orders():
    selected_fio = combobox.get()
    if selected_fio != "":
        # Очистить текущее содержимое таблицы
        table.delete(*table.get_children())

        # Получение отфильтрованных данных из базы данных
        try:
            database = pymysql.connect(host='localhost', user='root',
                                       password='1234', database='zadanie2')
            cursor = database.cursor()
            cursor.execute(f"SELECT fio, telephone, email, date_sale, status FROM orders WHERE fio='{selected_fio}'")
            orders = cursor.fetchall()

            # Вставка данных в таблицу
            for order in orders:
                table.insert('', 'end', values=order)

            cursor.close()
            database.close()

        except pymysql.Error as e:
            showerror('Ошибка', f'Произошла ошибка при получении данных: {str(e)}')


def show_all_orders():
    # Очистить текущее содержимое таблицы
    table.delete(*table.get_children())

    # Получение всех данных из базы данных
    try:
        database = pymysql.connect(host='localhost', user='root',
                                   password='1234', database='zadanie2')
        cursor = database.cursor()
        cursor.execute('SELECT fio, telephone, email, date_sale, status FROM orders')
        orders = cursor.fetchall()

        # Вставка данных в таблицу
        for order in orders:
            table.insert('', 'end', values=order)

        cursor.close()
        database.close()

    except pymysql.Error as e:
        showerror('Ошибка', f'Произошла ошибка при получении данных: {str(e)}')


def find_orders():
    search_query = search_lineedit.get()
    if search_query != "":
        # Снять выделение со всех строк таблицы
        for row_id in table.get_children():
            table.selection_remove(row_id)

        # Поиск и выделение строк, содержащих поисковый запрос
        for row_id in table.get_children():
            row_values = table.item(row_id)['values']
            for value in row_values:
                if search_query in str(value):
                    table.selection_add(row_id)
                    break


def sort_data(column):
    # Get the current data in the Treeview
    data = [(table.set(child, column), child) for child in table.get_children('')]

    # Sort the data based on the selected sorting option
    if sort_var.get() == 'increasing':
        if column == 'fio':
            data.sort(reverse=True)
        elif column == 'date_sale':
            data.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=False)
        elif column == 'status':
            data.sort(key=lambda x: ('Выполнен' not in x[0], 'В работе' not in x[0], 'Новый' not in x[0]))
    elif sort_var.get() == 'decreasing':
        if column == 'fio':
            data.sort(reverse=False)
        elif column == 'date_sale':
            data.sort(key=lambda x: datetime.strptime(x[0], '%Y-%m-%d'), reverse=True)
        elif column == 'status':
            data.sort(key=lambda x: ('Выполнен' not in x[0], 'В работе' not in x[0], 'Новый' not in x[0]), reverse=True)

    # Reorder the rows in the Treeview based on the sorted data
    for index, (value, child) in enumerate(data):
        table.move(child, '', index)


def on_listbox_select(event):
    selected_item = listbox.get(listbox.curselection())
    if selected_item == "Клиент":
        table.heading('fio', text='Клиент')
        if sort_var.get() != '':
            sort_data('fio')
    elif selected_item == "Дата заказа":
        table.heading('date_sale', text='Дата заказа')
        if sort_var.get() != '':
            sort_data('date_sale')
    elif selected_item == "Статус заказа":
        table.heading('status', text='Статус заказа')
        if sort_var.get() != '':
            sort_data('status')


# Создание окна
window = Tk()
window.title('Работа с заявками клиентов')
window.geometry('1000x380')

text_label = Label(window, text='Выберите клиента')
text_label.grid(row=1, column=0)

combobox = ttk.Combobox(window)
combobox.grid(row=1, column=1)

filter_button = Button(window, text='Фильтровать', command=filter_orders)
filter_button.grid(row=1, column=2)

show_all_button = Button(window, text='Показать все', command=show_all_orders)
show_all_button.grid(row=1, column=3)

text_label = Label(window, text='Введите строку поиска')
text_label.grid(row=2, column=0)

search_lineedit = Entry(window)
search_lineedit.grid(row=2, column=1)

find_button = Button(window, text='Найти', command=find_orders)
find_button.grid(row=2, column=2)

text_label = Label(window, text='Выберите поле для сортировки')
text_label.grid(row=0, column=4)

listbox = Listbox(window, height=3)
listbox.grid(row=1, column=4)
values = ["Клиент", "Дата заказа", "Статус заказа"]
for value in values:
    listbox.insert(END, value)
listbox.bind('<<ListboxSelect>>', on_listbox_select)

sort_var = StringVar()
radiobutton_increasing = ttk.Radiobutton(window, text='По возрастанию', variable=sort_var, value='increasing',
                                         command=lambda: sort_data('fio'))
radiobutton_decreasing = ttk.Radiobutton(window, text='По убыванию   ', variable=sort_var, value='decreasing',
                                         command=lambda: sort_data('fio'))

radiobutton_increasing.grid(row=1, column=5)
radiobutton_decreasing.grid(row=2, column=5)

text_label = Label(window, text='')
text_label.grid(row=3, column=0)

table = ttk.Treeview(window, columns=('fio', 'telephone', 'email', 'date_sale', 'status'))
table.heading('#0', text='О')  # Set the heading for the first column
table.column('#0', minwidth=0, width=0)
table.heading('fio', text='Клиент')
table.heading('telephone', text='Телефон')
table.heading('email', text='Электронная почта')
table.heading('date_sale', text='Дата заказа')
table.heading('status', text='Статус заказа')
table.grid(row=5, column=0, columnspan=6)

try:
    database = pymysql.connect(host='localhost', user='root',
                               password='1234', database='zadanie2')
    cursor = database.cursor()
    cursor.execute('SELECT DISTINCT fio FROM orders')
    fios = cursor.fetchall()

    combobox['values'] = [fio[0] for fio in fios]

    cursor.close()
    database.close()

except pymysql.Error as e:
    showerror('Ошибка', f'Произошла ошибка при получении данных: {str(e)}')

window.mainloop()

import psycopg2
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QTableWidget
from PyQt5 import uic, QtGui, QtWidgets
from PyQt5.QtWidgets import QListWidget, QListWidgetItem, QAbstractItemView
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QTextDocument, QPageSize, QPageLayout, QPdfWriter, QPainter
import re


Form, Windows = uic.loadUiType('connexion1.ui')


app = QApplication([])
windows = Windows()
form = Form()
form.setupUi(windows)

conn = None
db = 'System'
save_button = None


def login():
    global save_button
    form.listWidget.clear()
    first_name, password = form.lineEdit_2.text(), form.lineEdit_3.text()
    try:
        conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
        cur = conn.cursor()
        cur.execute("SELECT first_name, password FROM clients")
        clients = cur.fetchall()
        for client in clients:
            if (first_name, password) == client:
                form.listWidget.addItem(f'Здравствуйте {first_name} !')
                form.listWidget.addItem('Если у вас есть какие-либо вопросы, вы можете задать их в разделе (requests) !')
                form.listWidget.addItem('для добавления или удаления автомобиля сообщите об этом администратору')
                form.listWidget.addItem('Напишите в requests: марка, модель, год, идентификационный номер транспортного средства (VIN)  ' )
                form.label_4.setText('Cпасибо, что выбрали нас! ')
                cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' AND tablename IN ('cars', 'clients', 'policies', 'requests')")
                tables = cur.fetchall()
                if hasattr(form, 'table_combo'):
                    form.verticalLayout.removeWidget(form.table_combo)
                    form.table_combo.deleteLater()
                table_combo = QtWidgets.QComboBox()
                for table in tables:
                    table_combo.addItem(table[0])
                form.verticalLayout.addWidget(table_combo)
                form.table_combo = table_combo
                break
        else:
            if (first_name, password) == ('admin', '12345'):
                form.label_4.setText('Здравствуйте администратор !')
                cur.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' AND tablename IN ('cars', 'clients', 'policies', 'requests')")
                tables = cur.fetchall()
                if hasattr(form, 'table_combo'):
                    form.verticalLayout.removeWidget(form.table_combo)
                    form.table_combo.deleteLater()
                table_combo = QtWidgets.QComboBox()
                for table in tables:
                    table_combo.addItem(table[0])
                form.verticalLayout.addWidget(table_combo)
                form.table_combo = table_combo

        table_combo.currentIndexChanged.connect(lambda: display_table_data(table_combo.currentText()))

        if save_button is None:
            save_button = QtWidgets.QPushButton("Save")
            save_button.setEnabled(False)
            save_button.clicked.connect(save_table_data)
            form.verticalLayout.addWidget(save_button)

            def enable_save_button():
                save_button.setEnabled(True)

            form.tableWidget.itemChanged.connect(enable_save_button)

        selected_table = table_combo.currentText()
        display_table_data(selected_table)

        cur.close()
        conn.close()

    except Exception as e:
        form.listWidget.addItem('Ошибка')
        print(e)

def display_table_data(selected_table):
    conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
    cur = conn.cursor()

    # Retrieve attributes and values from the selected table
    query = ""
    if form.lineEdit_2.text() == "admin" and form.lineEdit_3.text() == "12345":
        query = f"SELECT * FROM {selected_table}"
    elif selected_table == "clients":
        query = f"SELECT * FROM {selected_table} WHERE first_name='{form.lineEdit_2.text()}' AND password='{form.lineEdit_3.text()}'"
    elif selected_table in ["cars", "requests"]:
        query = f"SELECT * FROM {selected_table} WHERE client_id = (SELECT client_id FROM clients WHERE first_name='{form.lineEdit_2.text()}' AND password='{form.lineEdit_3.text()}')"
    elif selected_table == "policies":
        query = f"SELECT * FROM {selected_table} WHERE car_id IN (SELECT car_id FROM cars WHERE client_id = (SELECT client_id FROM clients WHERE first_name='{form.lineEdit_2.text()}' AND password='{form.lineEdit_3.text()}'))"

    try:
        cur.execute(query)
        rows = cur.fetchall()
        attributes = [desc[0] for desc in cur.description]

        # Display attributes of the table
        form.tableWidget.setColumnCount(len(attributes))
        form.tableWidget.setHorizontalHeaderLabels(attributes)

        # Display values of attributes
        form.tableWidget.setRowCount(len(rows))
        for i, row in enumerate(rows):
            for j, value in enumerate(row):
                item = QtWidgets.QTableWidgetItem(str(value) if value else "")
                form.tableWidget.setItem(i, j, item)

        cur.close()
        conn.close()

    except Exception as e:
        form.listWidget.addItem('Ошибка')
        print(str(e))

def search():
    search_query = form.lineEdit.text()

    pattern = re.compile(search_query, re.IGNORECASE)

    for i in range(form.tableWidget.rowCount()):
        for j in range(form.tableWidget.columnCount()):

            cell_text = form.tableWidget.item(i, j).text()

            match = re.search(pattern, cell_text)

            if match:
                item = form.tableWidget.item(i, j)
                item.setBackground(QtGui.QColor('yellow'))
            else:
                item = form.tableWidget.item(i, j)
                item.setBackground(QtGui.QColor('white'))


def display_selected_row_data(selected_table, selected_id):
    try:
        conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
        cur = conn.cursor()

        cur.execute(f"SELECT * FROM {selected_table} WHERE id = {selected_id}")
        row = cur.fetchone()

        form.tableWidget.setColumnCount(len(attributes))
        form.tableWidget.setHorizontalHeaderLabels(attributes)
        form.tableWidget.setRowCount(1)
        for j, value in enumerate(row):
            item = QtWidgets.QTableWidgetItem(str(value) if value else "")
            form.tableWidget.setItem(0, j, item)

        cur.close()
        conn.close()

    except Exception as e:
        form.listWidget.addItem('Ошибка')
        print(str(e))

def save_table_data():
    first_name = form.lineEdit_2.text()
    password = form.lineEdit_3.text()
    try:
        conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
        cur = conn.cursor()

        # Get the selected table name and column names
        selected_table = form.table_combo.currentText()
        cur.execute(f"SELECT * FROM {selected_table} LIMIT 0")
        column_names = [desc[0] for desc in cur.description]

        # Update database with modified data
        for row in range(form.tableWidget.rowCount()):
            if not form.tableWidget.item(row, 0):
                continue
            item_values = []
            for col in range(form.tableWidget.columnCount()):
                item = form.tableWidget.item(row, col)
                if item is not None:
                    item_text = item.text()
                    if column_names[col] == "first_name" and item_text.isnumeric():
                        form.listWidget.addItem('Ошибка: поле first_name не должно содержать числа')
                        break
                    elif column_names[col] == "last_name" and item_text.isnumeric():
                        form.listWidget.addItem('Ошибка: поле last_name не должно содержать числа')
                        break
                    elif column_names[col] == "phone" and not item_text.isnumeric():
                        form.listWidget.addItem('Ошибка: поле phone должно содержать только числа')
                        break
                    else:
                        item_values.append(f"{column_names[col]}='{item_text}'")
            if len(item_values) > 0:
                if selected_table == "policies":
                    cur.execute(
                            f"UPDATE {selected_table} SET {', '.join(item_values)} WHERE policy_id={form.tableWidget.item(row, 0).text()}")
                else:
                    cur.execute(
                    f"UPDATE {selected_table} SET {', '.join(item_values)} WHERE client_id={form.tableWidget.item(row, 0).text()}")


        conn.commit()
        cur.close()
        conn.close()

    except Exception as e:
        form.listWidget.addItem('Ошибка')
        print(str(e))

def register_user():
    global conn
    Form3, Windows3 = uic.loadUiType('connexion.ui')
    windows3 = Windows3()
    form3 = Form3()
    form3.setupUi(windows3)

    def reg():
        try:
            user = form3.lineEdit.text()
            password = form3.lineEdit_5.text()
            email = form3.lineEdit_3.text()
            phone = form3.lineEdit_4.text()
            last_name = form3.lineEdit_2.text()

            if user.isnumeric():
                form.listWidget.addItem('Ошибка')
            if last_name.isnumeric():
                form.listWidget.addItem('Ошибка')
            if phone.isalpha():
                form.listWidget.addItem('Ошибка')
            else:

                conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
                cur = conn.cursor()

                cur.execute("SELECT * FROM clients WHERE email = %s OR phone = %s", (email, phone))
                existing_user = cur.fetchone()
                if existing_user is not None:
                    form3.listWidget_2.addItem('Этот электронный адрес или номер телефона уже зарегистрирован.')
                    return

                cur.execute("SELECT MAX(client_id) FROM clients;")
                max_client_id = cur.fetchone()[0]
                new_client_id = max_client_id + 1 if max_client_id is not None else 1

                insert_query = """ INSERT INTO clients (client_id, first_name, last_name, email, phone, password) VALUES (%s, %s, %s, %s, %s, %s)"""
                item_tuple = (new_client_id, user, last_name, email, phone, password)
                cur.execute(insert_query, item_tuple)


                insert_request_query = """ INSERT INTO requests (request_id, client_id)
                                                       VALUES (%s, %s)"""
                cur.execute(insert_request_query, (new_client_id, new_client_id))

                conn.commit()
                form.listWidget.addItem(f'Добро пожаловать {user} ,  ваш пароль это: {password} ')



            windows3.close()
        except Exception as error:
            print(str(error))
            form3.listWidget_2.addItem('Ошибка')

    form3.pushButton.clicked.connect(reg)
    windows3.show()


def add():
    global conn
    Form4, Windows4 = uic.loadUiType('connexion2.ui')
    windows4 = Windows()
    form4 = Form4()
    form4.setupUi(windows4)
    conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
    cur = conn.cursor()
    code = form.lineEdit_4.text()
    if code == '12345':
        def add_cars():

            try:
                make = form4.lineEdit_3.text()
                model= form4.lineEdit_4.text()
                year = form4.lineEdit_5.text()
                vin = form4.lineEdit_6.text()
                car_id = form4.lineEdit_14.text()
                client_id = form4.lineEdit_15.text()



                insert_query = """ INSERT INTO cars (car_id, make, model, year, vin, client_id) VALUES (%s, %s, %s, %s, %s, %s)"""
                item_tuple = (car_id, make, model, year, vin, client_id)
                cur.execute(insert_query, item_tuple)
                form.listWidget.addItem('добавление сделано')

                conn.commit()
                windows4.close()

            except Exception as error:
                print(str(error))
                form4.listWidget.addItem('Ошибка')
            pass
        form4.radioButton_2.clicked.connect(add_cars)

        windows4.show()


        def add_policies():
            global conn
            try:
                Policy_number = form4.lineEdit_7.text()
                start_date = form4.lineEdit_8.text()
                end_date = form4.lineEdit_9.text()
                premium = form4.lineEdit_10.text()
                deductible = form4.lineEdit_11.text()
                policy_id = form4.lineEdit_12.text()
                car_id =  form4.lineEdit_13.text()


                insert_query = """ INSERT INTO policies (policy_id, Policy_number, start_date, end_date, premium, deductible,  car_id) VALUES (%s, %s, %s, %s, %s, %s, %s)"""
                item_tuple = (
                    policy_id, Policy_number, start_date, end_date, premium, deductible, car_id)
                cur.execute(insert_query, item_tuple)
                form.listWidget.addItem('добавление сделано')
                conn.commit()
                windows4.close()

            except Exception as e:
                print(str(e))
                form4.listWidget.addItem('Ошибка')
            pass

        windows4.show()
        form4.radioButton_3.clicked.connect(add_policies)
    else:
        form.listWidget.addItem('Ошибка')

def delete():
    global conn
    Form5, Windows5 = uic.loadUiType('connexion3.ui')
    windows5 = Windows()
    form5 = Form5()
    form5.setupUi(windows5)
    conn = psycopg2.connect(dbname="System", user="staff01", password="0000")
    cur = conn.cursor()
    code = form.lineEdit_4.text()
    if code == '12345':
        def delete_policies():
            try:
                policy_id = form5.lineEdit_2.text()
                delete_query = """DELETE FROM Policies WHERE policy_id = %s;"""
                cur.execute(delete_query, (policy_id,))
                if cur.rowcount == 1:
                    form.listWidget.addItem('Удалено успешно')
                else:
                    form5.listWidget.addItem('Не удалось найти машину с таким ID')

                    conn.commit()
                    windows5.close()
            except Exception as error:
                print(str(error))
                form5.listWidget.addItem('Ошибка')
            pass
        form5.radioButton_3.clicked.connect(delete_policies)

        windows5.show()

        def delete_requests():
            try:
                request_id = form5.lineEdit.text()
                delete_query = """ DELETE FROM requests WHERE request_id = %s; """
                cur.execute(delete_query, (request_id,))
                if cur.rowcount == 1:
                    form.listWidget.addItem('Удалено успешно')

                else:
                    form5.listWidget.addItem('Не удалось найти машину с таким ID')
                    conn.commit()
                    windows5.close()

            except Exception as error:
                print(str(error))
                form5.listWidget.addItem('Ошибка')
            pass

        windows5.show()
        form5.radioButton_2.clicked.connect(delete_requests)
        def delete_cars():
            try:
                car_id = form5.lineEdit_3.text()
                delete_query = """ DELETE FROM cars WHERE car_id = %s;"""
                cur.execute(delete_query, (car_id))
                if cur.rowcount == 1:
                    form.listWidget.addItem('Удалено успешно')

                else:
                    form5.listWidget.addItem('Не удалось найти машину с таким ID')
                    conn.commit()
                    windows5.close()

            except Exception as error:
                print(str(error))
                form5.listWidget.addItem('Ошибка')
            pass

        windows5.show()
        form5.radioButton_4.clicked.connect(delete_cars)
        def delete_clients():
            try:
                client_id = form5.lineEdit_4.text()
                delete_query = """ DELETE FROM clients WHERE client_id = %s;"""
                cur.execute(delete_query, (client_id,))
                if cur.rowcount == 1:
                    form.listWidget.addItem('Удалено успешно')

                else:
                    form5.listWidget.addItem('Не удалось найти машину с таким ID')
                    conn.commit()
                    windows5.close()

            except Exception as error:
                print(str(error))
                form5.listWidget.addItem('Ошибка')
            pass
        form5.radioButton_5.clicked.connect(delete_clients)

        windows5.show()
    else:
        form.listWidget.addItem('Ошибка')


form.radioButton.clicked.connect(register_user)
form.radioButton_3.clicked.connect(login)
form.radioButton_4.clicked.connect(add)
form.radioButton_5.clicked.connect(delete)
form.radioButton_6.clicked.connect(search)
windows.show()
app.exec_()

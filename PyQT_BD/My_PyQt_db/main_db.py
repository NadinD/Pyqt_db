import sqlite3
import sys
from PyQt5 import QtCore, QtSql
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlRelation, QSqlRelationalDelegate
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QTableWidgetItem, QMessageBox
from PyQT_BD.My_PyQt_db.ui_main import Ui_MainWindow

from PyQT_BD.My_PyQt_db.ui_services import Ui_Dialog_services
from PyQT_BD.My_PyQt_db.ui_services_update import Ui_Dialog
from PyQT_BD.My_PyQt_db.ui_unit import Ui_Dialog_unit
from PyQT_BD.My_PyQt_db.ui_unit_new import Ui_Dialog_unit_new
from PyQT_BD.My_PyQt_db.ui_unit_update import Ui_Dialog_unit_update
from PyQT_BD.My_PyQt_db.ui_user import Ui_Dialog_user
from PyQT_BD.My_PyQt_db.ui_user_new import Ui_Dialog_user_new
from PyQT_BD.My_PyQt_db.ui_user_update import Ui_Dialog_user_update


class Window(QMainWindow, Ui_MainWindow):
    """
    Основное окно программы
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # Обработка действий по меню

        # нажата кнопка меню "Справочники -> Подразделения"
        self.unit_action.triggered.connect(self.unit_dialog)

        # нажата кнопка меню "Справочники -> Сотрудники"
        self.user_action.triggered.connect(self.user_dialog)

        # нажата кнопка меню "Справочники -> Сервисные службы"
        self.services_action.triggered.connect(self.services_dialog)

        # Работа с самой формой
        # Соединение с базой
        # con = sqlite3.connect('ProblemDB.db')
        myconnection = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
        myconnection.setDatabaseName("ProblemDB.db")
        myconnection.open()
        # if not myconnection.open():
        #     QMessageBox.critical(None, qApp.tr("Cannot open database"),
        #                          qApp.tr("Unable to establish a database connection.\n"
        #                                  "This example needs SQLite support. Please read "
        #                                  "the Qt SQL driver documentation for information "
        #                                  "how to build it.\n\n" "Click Cancel to exit."),
        #                          QMessageBox.Cancel)
        # создаём для неё модель данных
        # self.sqlModel = QtSql.QSqlTableModel(self)
        self.sqlModel = QtSql.QSqlRelationalTableModel(self)
        # указываем таблицу из БД для модели
        self.sqlModel.setTable('def_message')
        # Выбираем стратегию редактирвоания
        self.sqlModel.setEditStrategy(QtSql.QSqlTableModel.OnFieldChange)
        # связь
        self.sqlModel.setRelation(4, QSqlRelation("user", "id", "FIO"));
        self.sqlModel.setRelation(2, QSqlRelation("services", "id", "name"));

        # загружаем данные из таблицы в модель
        self.sqlModel.select()
        # указываем заголовки столбцов
        self.sqlModel.setHeaderData(0, QtCore.Qt.Horizontal, 'Номер заявки')
        self.sqlModel.setHeaderData(1, QtCore.Qt.Horizontal, 'Дата')
        self.sqlModel.setHeaderData(2, QtCore.Qt.Horizontal, 'Служба')
        self.sqlModel.setHeaderData(3, QtCore.Qt.Horizontal, 'Текст неисправности')
        self.sqlModel.setHeaderData(4, QtCore.Qt.Horizontal, 'Пользователь')
        # назначаем сетке-гриду-таблице-представлению модель данных
        self.tableView.setModel(self.sqlModel)

        self.tableView.setItemDelegate(QSqlRelationalDelegate(self.tableView))

        # self.tableView.setColumnHidden(0, True)
        # self.tableView.setColumnHidden(1, True)

        self.btProblemAdd.clicked.connect(self.addrow)
        self.btProblemDel.clicked.connect(self.delrow)
        self.btProblemFind.clicked.connect(self.findText)

        #
        # # создаём ссылку на модель-выбора (именно из неё можно получить текущий индекс ячейки) в сетке-гриде-таблице
        # selModel = self.tableView.selectionModel()

    def addrow(self):
        #  добавить строку
        ret = self.sqlModel.insertRows(self.sqlModel.rowCount(), 1)

    def delrow(self):
        self.sqlModel.removeRow(self.tableView.currentIndex().row())

    def findText(self):

        self.sqlModel.setFilter("Name='Anderson'")

    def unit_dialog(self):
        """
       Функция выполняется при нажатии кнопки меню "Справочники -> Подразделения"
       :return: Открывает окно с таблицей информации по подразделениям (Unit_win)
       """
        dialog_unit = Unit_win(self)
        dialog_unit.show()
        # Скрываем основное окно программы
        wnd.hide()

    def user_dialog(self):
        """
        Функция выполняется при нажатии кнопки меню "Справочники -> Сотрудники"
        :return: Открывает окно с таблицей информации по отрудникам (User_win)
        """
        dialog_user = User_win(self)
        dialog_user.show()
        # Скрываем основное окно программы
        wnd.hide()

    def services_dialog(self):
        """
         Функция выполняется при нажатии кнопки меню "Справочники -> Сервисные службы"
        :return: Открывает окно с таблицей информации по сервисным службам (Services_win)
        """
        dialog = Services_win(self)
        dialog.show()
        # Скрываем основное окно программы
        wnd.hide()


class Unit_win(QDialog, Ui_Dialog_unit):
    """
    Окно  "Подразделения"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        # Соединение с базой
        con = sqlite3.connect('ProblemDB.db')
        cur = con.cursor()
        # Заполнение таблицы
        for row_number, row in enumerate(cur.execute("""select u.id,u.name,u.shortName,u1.name
        from unit as  u
        LEFT JOIN unit as u1
        on u.unitId= u1.id""").fetchall()):
            self.tableUnit.insertRow(row_number)
            for col_number, col in enumerate(row):
                if col == None:
                    col = ''
                self.tableUnit.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.tableUnit.setSortingEnabled(True)
        # Подгоняем ширину столбцов таблицы под данные
        self.tableUnit.resizeColumnsToContents()

        # Нажата кнопка "Добавить строку" на форме "Подразделения"
        self.btUnitAdd.clicked.connect(self.bt_add_unit)
        # Нажата кнопка "Удалить строку" на форме "Подразделения"
        self.btUnitDel.clicked.connect(self.bt_del_unit)
        # Нажата кнопка "Обновить строку" на форме "Подразделения"
        self.btUnitUpdate.clicked.connect(self.bt_upd_unit)

        self.lineEdit.textChanged.connect(self.text_changed_find)

    def text_changed_find(self):
        items = self.tableUnit.findItems(self.lineEdit.text(), QtCore.Qt.MatchContains)
        if items:  # если список не пустой
            # установить текущей первую из найденых ячеек
            self.tableUnit.selectRow(items[0].row())

    def bt_add_unit(self):
        """
        Функция выполняется при нажатии кнопки "Добавить строку" на форме "Подразделения"
        :return: Открывает окно для ввода данных
        """
        dialog_unit_new = Unit_new_win(self)
        with sqlite3.connect('ProblemDB.db') as con:
            cur = con.cursor()
            data = cur.execute('SELECT name FROM unit').fetchall()
            # заполняем выпадающий список данными
            dialog_unit_new.CB_unit.clear()
            for row in data:
                dialog_unit_new.CB_unit.addItem(*row)
            # Устанвливаем "ПУСТУЮ" строку -ничего не выбрано из списка
            dialog_unit_new.CB_unit.setCurrentIndex(-1)
        # открываем окно
        dialog_unit_new.show()

        # Если в окне была нажата кнопка "Записать"
        if dialog_unit_new.exec() == QDialog.Accepted:
            # удаляем все строки из таблицы и заполняем заново
            self.tableUnit.setRowCount(0)
            for row_number, row in enumerate(cur.execute("""select u.id,u.name,u.shortName,u1.name
            from unit as  u
            LEFT JOIN unit as u1
            on u.unitId= u1.id""").fetchall()):
                self.tableUnit.insertRow(row_number)
                for col_number, col in enumerate(row):
                    if col == None:
                        col = ''
                    self.tableUnit.setItem(row_number, col_number, QTableWidgetItem(str(col)))

    def bt_del_unit(self):
        """
        Функция выполняется при нажатии кнопки "Удалить строку" на форме "Сотрудники"
        :return:
        """
        a = []
        if self.tableUnit.selectedItems():
            for currentQTableWidgetItem in self.tableUnit.selectedItems():
                a.append(currentQTableWidgetItem.text())
            # Удаление строки
            sql = 'DELETE FROM  unit WHERE id  =' + str(a[0])
            self.con = sqlite3.connect('ProblemDB.db')
            cur = self.con.cursor()
            self.cur.execute(sql)
            self.cur.commit()
            self.tableUnit.removeRow(currentQTableWidgetItem.row())
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_unit(self):
        """
        Функция выполняется при нажатии кнопки "Обновить строку" на форме "Сотрудники"
        :return: Открывает окно для обновления  данных
        """
        dialog_unit_update = Unit_update_win(self)
        dialog_unit_update.Edit_Id.hide()
        a = []

        table = self.tableUnit
        # Получаем строку с текущими данными
        if table.selectedItems():
            for currentQTableWidgetItem in table.selectedItems():
                a.append(currentQTableWidgetItem.text())
            # id
            dialog_unit_update.Edit_Id.setText(str(a[0]))
            # заполняем  текущее значение Подразделения
            dialog_unit_update.Edit_Unit_up.setText(str(a[1]))
            # заполняем  текущее значение сокращенного наименования
            dialog_unit_update.Edit_Short_Unit_up.setText(str(a[2]))
            # Заполняем список Подразделений
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                data = cur.execute('SELECT name FROM unit').fetchall()
            dialog_unit_update.CB_unit_up.clear()
            for row in data:
                dialog_unit_update.CB_unit_up.addItem(*row)
                # Устанавливаем текущее значение
                dialog_unit_update.CB_unit_up.setCurrentText(str(a[3]))
            # Показываем форму для изменения значений
            dialog_unit_update.show()

            # Если в окне была нажата кнопка "Записать"
            if dialog_unit_update.exec() == QDialog.Accepted:
                self.tableUnit.setRowCount(0)
                for row_number, row in enumerate(cur.execute("""select u.id,u.name,u.shortName,u1.name
                from unit as  u
                LEFT JOIN unit as u1
                on u.unitId= u1.id""").fetchall()):
                    self.tableUnit.insertRow(row_number)
                    for col_number, col in enumerate(row):
                        if col == None:
                            col = ''
                        self.tableUnit.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def closeEvent(self, event):
        """
        при закрытии окна показать главное окно . Событие формируется при закрытии окна.
        """
        wnd.show()


class Unit_new_win(QDialog, Ui_Dialog_unit_new):
    """
    Окно "Добавление данных по Подразделениям" .
    Вызывается из формы "Подразделения" по нажатию на кнопку "Добавить строку"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.CB_unit.setEditable(True)
        self.CB_unit.editTextChanged.connect(self.findText)

        # # нажата кнопка "Записать"
        self.btnUnit_Ok.clicked.connect(self.bt_ok_unit_new)
        # нажата кнопка "Отмена"
        self.btnUnit_Cancel.clicked.connect(self.bt_cancel_unit_new)

    def bt_ok_unit_new(self):
        """
        Функция вызывается по нажатию кнопки "Записать" на форме
        :return:
        """
        er1 = False
        er2 = False
        if self.Edit_Unit.text() == '':
            QMessageBox.information(self, 'Ошибка', 'Поле подразделение должно быть обязательно заполнено')
            er1 = True
        elif self.CB_unit.currentText() == '':
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                cur.execute('INSERT into unit(name,shortname) VALUES (?,?)',
                            (self.Edit_Unit.text(), self.Edit_Short_Unit.text()))
                cur.commit()
        else:
            # подразделение вышестоящее
            with sqlite3.connect('ProblemDB.db') as con:
                sql = """SELECT id FROM unit where name ='""" + self.CB_unit.currentText() + """'"""
                # QMessageBox.information(self, 'Отладка', str(sql))
                cur = con.cursor()
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Ошибка', 'Введено не верное название поразделения')
                else:
                    # print(id_un)
                    er2 = False
                    # print(id_un[0])
                    # QMessageBox.information(self, 'Отладка', str(id_un))
                    with sqlite3.connect('ProblemDB.db') as con:
                        cur = con.cursor()
                        cur.execute('INSERT into unit(name,shortname,unitId) VALUES (?,?,?)',
                                    (self.Edit_Unit.text(), self.Edit_Short_Unit.text(), str(id_un[0])))
                        cur.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_unit_new(self):
        """
        Функция вызывается по нажатию кнопки "Отмена"
        :return:
        """
        self.close()

    def findText(self, s):
        """
        функция поиска введенного текста в поле Подразделение
        :param s: строка текста для поиска соответствия
        :return:
        """
        index = self.CB_unit.findText(s)
        if index > -1:
            self.CB_unit.setCurrentIndex(index)


class Unit_update_win(QDialog, Ui_Dialog_unit_update):
    """
       Окно "Обновление данных по Подразделениям" .
       Вызывается из формы "Подразделения" по нажатию на кнопку "Обновить строку"
       """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        # нажата кнопка "Записать"
        self.btnUnit_up_Ok.clicked.connect(self.bt_ok_unit_up)
        # нажата кнопка "Отмена"
        self.btnUnit_up_Cancel.clicked.connect(self.bt_cancel_unit_up)

    def bt_ok_unit_up(self):
        """
        Функция вызывается по нажатию кнопки "Записать" на форме
        :return:
        """
        er1 = False
        er2 = False
        if self.Edit_Unit_up.text() == '':
            QMessageBox.information(self, 'Ошибка', 'Поле подразделение должно быть обязательно заполнено')
            er1 = True
        elif self.CB_unit_up.currentText() == '':
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                cur.execute('UPDATE unit set name=?,shortname=? where id=?',
                            (self.Edit_Unit_up.text(), self.Edit_Short_Unit_up.text()), self.Edit_Id.text())
                cur.commit()
        else:
            # подразделение вышестоящее
            with sqlite3.connect('ProblemDB.db') as con:
                sql = """SELECT id FROM unit where name ='""" + self.CB_unit_up.currentText() + """'"""
                cur = con.cursor()
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Ошибка', 'Введено не верное название поразделения')
                else:
                    er2 = False
                    with sqlite3.connect('ProblemDB.db') as con:
                        cur = con.cursor()
                        cur.execute('UPDATE unit set name= ?,shortname=?,unitId=? where id=?',
                                    (self.Edit_Unit_up.text(), self.Edit_Short_Unit_up.text(), str(id_un[0]),
                                     self.Edit_Id.text()))
                        cur.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_unit_up(self):
        """
        Функция вызывается по нажатию кнопки "Отмена"
        :return:
        """
        self.close()


class User_win(QDialog, Ui_Dialog_user):
    """
    Окно "Сотрудники"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        # Соединение с базой
        con = sqlite3.connect('ProblemDB.db')
        cur = con.cursor()
        # Заполнение таблицы
        for row_number, row in enumerate(cur.execute("""select u.id,u.FIO, u.birthday, u.gender, un.name
        from User as u
        LEFT JOIN  unit as un
        on  un.id= u.unitId""").fetchall()):
            self.tableUser.insertRow(row_number)
            for col_number, col in enumerate(row):
                if col == None:
                    col = ''
                self.tableUser.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.tableUser.setSortingEnabled(True)
        self.tableUser.resizeColumnsToContents()

        # Нажата кнопка "Добавить строку" на форме "Сотрудники"
        self.btUserAdd.clicked.connect(self.bt_add_user)
        # Нажата кнопка "Удалить строку" на форме "Сотрудники"
        self.btUserDel.clicked.connect(self.bt_del_user)
        # Нажата кнопка "Обновить строку" на форме "Сотрудники"
        self.btUserUpdate.clicked.connect(self.bt_upd_user)

        self.lineEdit.textChanged.connect(self.text_changed_find)

    def text_changed_find(self):
        items = self.tableUser.findItems(self.lineEdit.text(), QtCore.Qt.MatchContains)
        if items:  # если список не пустой
            # установить текущей первую из найденых ячеек
            self.tableUser.selectRow(items[0].row())

    def bt_add_user(self):
        """
        Функция выполняется при нажатии кнопки "Добавить строку" на форме "Сотрудники"
        :return: Открывает окно для ввода данных
        """
        dialog_user_new = User_new_win(self)
        with sqlite3.connect('ProblemDB.db') as con:
            cur = con.cursor()
            data = cur.execute('SELECT name FROM unit').fetchall()

            dialog_user_new.CB_unit.clear()
            for row in data:
                dialog_user_new.CB_unit.addItem(*row)
            # Устанвливаем "ПУСТУЮ" строку -ничего не выбрано из списка
            dialog_user_new.CB_unit.setCurrentIndex(-1)
        dialog_user_new.show()

        if dialog_user_new.exec() == QDialog.Accepted:
            self.tableUser.setRowCount(0)
            for row_number, row in enumerate(cur.execute("""select u.id,u.FIO, u.birthday, u.gender, un.name
                        from User as u
                        LEFT JOIN  unit as un
                        on  un.id= u.unitId""").fetchall()):
                self.tableUser.insertRow(row_number)
                for col_number, col in enumerate(row):
                    if col == None:
                        col = ''
                    self.tableUser.setItem(row_number, col_number, QTableWidgetItem(str(col)))

    def bt_del_user(self):
        """
        Функция выполняется при нажатии кнопки "Удалить строку" на форме "Сотрудники"
        :return:
        """
        a = []
        if self.tableUser.selectedItems():
            for currentQTableWidgetItem in self.tableUser.selectedItems():
                a.append(currentQTableWidgetItem.text())
            # Удаление строки
            sql = 'DELETE FROM  user WHERE id  =' + str(a[0])
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                self.cur.execute(sql)
                self.cur.commit()
                self.tableUser.removeRow(currentQTableWidgetItem.row())
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_user(self):
        """
        Функция выполняется при нажатии кнопки "Обновить строку" на форме "Сотрудники"
        :return: Открывает окно для обновления  данных
        :return:
        """
        dialog_user_update = User_update_win(self)
        dialog_user_update.Edit_Id.hide()
        a = []

        table = self.tableUser
        # Получаем строку с текущими данными
        if table.selectedItems():
            for currentQTableWidgetItem in table.selectedItems():
                a.append(currentQTableWidgetItem.text())
            # id
            dialog_user_update.Edit_Id.setText(str(a[0]))
            # заполняем  текущее значение ФИО
            dialog_user_update.Edit_Fio_up.setText(str(a[1]))
            # Дата рождения
            dt = QDate.fromString(str(a[2]), 'yyyy-MM-dd')
            # заполняем  текущее значение ФИО
            dialog_user_update.Edit_date_up.setDate(dt)
            # заполняем значение текущее Пол
            if a[3] == 'М':
                dialog_user_update.chB_male_up.setCheckState(2)
            else:
                dialog_user_update.chB_female_up.setCheckState(2)
            # Заполняем список Подразделений
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                data = cur.execute('SELECT name FROM unit').fetchall()
            dialog_user_update.CB_unit_up.clear()
            for row in data:
                dialog_user_update.CB_unit_up.addItem(*row)
                # Устанавливаем текущее значение
                dialog_user_update.CB_unit_up.setCurrentText(str(a[4]))
            # Показываем форму для изменения занчений
            dialog_user_update.show()
            if dialog_user_update.exec() == QDialog.Accepted:
                self.tableUser.setRowCount(0)
                for row_number, row in enumerate(cur.execute("""select u.id,u.FIO, u.birthday, u.gender, un.name
                            from User as u
                            LEFT JOIN  unit as un
                            on  un.id= u.unitId""").fetchall()):
                    self.tableUser.insertRow(row_number)
                    for col_number, col in enumerate(row):
                        if col == None:
                            col = ''
                        self.tableUser.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def closeEvent(self, event):
        """
        при закрытии окна показать главное окно . Событие формируется при закрытии окна.
        """
        wnd.show()


class User_new_win(QDialog, Ui_Dialog_user_new):
    """
    Окно "Добавление данных по Сотрудникам" .
    Вызывается из формы "Сотрудники" по нажатию на кнопку "Добавить строку"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        self.CB_unit.setEditable(True)
        self.CB_unit.editTextChanged.connect(self.findText)

        # нажата кнопка "Записать"
        self.btnUser_Ok.clicked.connect(self.bt_ok_user_new)
        # нажата кнопка "Отмена"
        self.btnUser_Cancel.clicked.connect(self.bt_cancel_user_new)

    def bt_ok_user_new(self):
        """
        Функция вызывается по нажатию кнопки "Записать" на форме
        :return:
        """
        er1 = False
        er2 = False
        if self.Edit_Fio.text() == '' or self.CB_unit.currentText() == '' or (
                not self.chB_female.isChecked() and not self.chB_male.isChecked()):
            QMessageBox.information(self, 'Ошибка', 'Не все поля заполнены')
            er1 = True
        else:
            # пол
            if self.chB_female.isChecked():
                er1 = False
                p = 'Ж'
            elif self.chB_male.isChecked():
                er1 = False
                p = 'М'

            # дата рождения
            d = self.Edit_date.date()
            td = d.toPyDate()

            # подразделение
            with sqlite3.connect('ProblemDB.db') as con:
                sql = """SELECT id FROM unit where name ='""" + self.CB_unit.currentText() + """'"""
                cur = con.cursor()
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Ошибка', 'Введено не верное название поразделения')
                else:
                    er2 = False
                    with sqlite3.connect('ProblemDB.db') as con:
                        cur = con.cursor()
                        cur.execute('INSERT into user(FIO,birthday,gender,unitId) VALUES (?,?,?,?)',
                                    (self.Edit_Fio.text(), str(td), p, str(id_un[0])))
                        cur.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_user_new(self):
        """
        Функция вызывается по нажатию кнопки "Отмена"
        :return:
        """
        self.close()

    def findText(self, s):
        """
        функция поиска введенного текста в поле Подразделение
        :param s: строка текста для поиска соответствия
        :return:
        """
        index = self.CB_unit.findText(s)
        if index > -1:
            self.CB_unit.setCurrentIndex(index)


class User_update_win(QDialog, Ui_Dialog_user_update):
    """
       Окно "Обновление данных по Сотрудникам" .
       Вызывается из формы "Сотрудники" по нажатию на кнопку "Обновить строку"
       """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        # нажата кнопка "Записать"
        self.btnUser_up_Ok.clicked.connect(self.bt_ok_user_up)
        # нажата кнопка "Отмена"
        self.btnUser_up_Cancel.clicked.connect(self.bt_cancel_user_up)

    def bt_ok_user_up(self):
        """
        Функция вызывается по нажатию кнопки "Записать" на форме
        :return:
        """
        er1 = False
        er2 = False
        if self.Edit_Fio_up.text() == '' or self.CB_unit_up.currentText() == '' or (
                not self.chB_female_up.isChecked() and not self.chB_male_up.isChecked()):
            QMessageBox.information(self, 'Ошибка', 'Не все поля заполнены')
            er1 = True
        else:
            # пол
            if self.chB_female_up.isChecked():
                er1 = False
                p = 'Ж'
            elif self.chB_male_up.isChecked():
                er1 = False
                p = 'М'

            # дата рождения
            d = self.Edit_date_up.date()
            td = d.toPyDate()

            # подразделение
            with sqlite3.connect('ProblemDB.db') as con:
                sql = """SELECT id FROM unit where name ='""" + self.CB_unit_up.currentText() + """'"""
                cur = con.cursor()
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Ошибка', 'Введено не верное название поразделения')
                else:
                    er2 = False
                    with sqlite3.connect('ProblemDB.db') as con:
                        cur = con.cursor()
                        cur.execute('Update user set FIO= ? , birthday= ?, gender =? ,unitId=? where id =?',
                                    (self.Edit_Fio_up.text(), str(td), p, str(id_un[0]), self.Edit_Id.text()))
                        cur.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_user_up(self):
        """
              Функция вызывается по нажатию кнопки "Отмена"
              :return:
              """
        self.close()


class Services_win(QDialog, Ui_Dialog_services):
    """
      Окно программы "Сервисные службы"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        # Соединение с базой
        con = sqlite3.connect('ProblemDB.db')
        cur = con.cursor()
        # Заполнение таблицы
        for row_number, row in enumerate(cur.execute("""select id,name from services""").fetchall()):
            self.tableSevices.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.tableSevices.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.tableSevices.setSortingEnabled(True)
        self.tableSevices.resizeColumnsToContents()

        # Нажата кнопка "Добавить строку" на форме "Сервисные службы"
        self.btServicesAdd.clicked.connect(self.bt_add_services)
        # Нажата кнопка "Удалить строку" на форме "Сервисные службы"
        self.btServicesDel.clicked.connect(self.bt_del_services)
        # Нажата кнопка "Обновить строку" на форме "Сервисные службы"
        self.btServicesUpdate.clicked.connect(self.bt_upd_services)

        self.lineEdit.textChanged.connect(self.text_changed_find)

    def text_changed_find(self):
        items = self.tableSevices.findItems(self.lineEdit.text(), QtCore.Qt.MatchContains)
        if items:  # если список не пустой
            # установить текущей первую из найденых ячеек
            self.tableSevices.selectRow(items[0].row())

    # def bt_find_services(self):
    #     txt=self.lineEdit.text()
    #     items = self.tableSevices.findItems(str(txt),QtCore.Qt.MatchContains)
    #     if items:  # если список не пустой
    #         # установить текущей первую из найденых ячеек
    #         self.tableSevices.selectRow(items[0].row())
    #     else:
    #         QMessageBox.information(self, 'Информация', 'Поиск не дал результатов')

    def bt_add_services(self):
        """
        Функция выполняется при нажатии кнопки "Добавить строку" на форме "Сервисные службы"
        :return: Открывает окно для ввода данных
        """
        serv, ok = QInputDialog.getText(self, 'Добавить', 'Название сервисной службы')
        table = self.tableSevices

        if ok:
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                cur.execute('INSERT into services(name) VALUES (?)', (serv,))
                cur.commit()
                table.setRowCount(0)
                for row_number, row in enumerate(cur.execute("""select id,name from services""").fetchall()):
                    table.insertRow(row_number)
                    for col_number, col in enumerate(row):
                        table.setItem(row_number, col_number, QTableWidgetItem(str(col)))

    def bt_del_services(self):
        """
        Функция выполняется при нажатии кнопки "Удалить строку" на форме "Сервисные службы"
        :return:
        """
        a = []
        if self.tableSevices.selectedItems():
            for currentQTableWidgetItem in self.tableSevices.selectedItems():
                a.append(currentQTableWidgetItem.text())

            # Удаление строки
            sql = 'DELETE FROM  services WHERE id  =' + str(a[0])
            with sqlite3.connect('ProblemDB.db') as con:
                cur = con.cursor()
                self.cur.execute(sql)
                self.cur.commit()
            self.tableSevices.removeRow(currentQTableWidgetItem.row())
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_services(self):
        """
        Функция выполняется при нажатии кнопки "Обновить строку" на форме "Сервисные службы"
        :return: Открывает окно для обновления данных (Services_up_win)
        """
        dial_upd = Services_up_win(self)
        a = []
        table = self.tableSevices

        if table.selectedItems():
            for currentQTableWidgetItem in table.selectedItems():
                a.append(currentQTableWidgetItem.text())
            dial_upd.lineEdit.setText(str(a[1]))
            if dial_upd.exec():
                sql = """UPDATE  services SET name ='""" + str(dial_upd.lineEdit.text()) + """' WHERE id  =""" + str(
                    a[0])
                with sqlite3.connect('ProblemDB.db') as con:
                    con.execute(sql)
                    con.commit()
                    self.tableSevices.setItem(currentQTableWidgetItem.row(), 1,
                                              QTableWidgetItem(dial_upd.lineEdit.text()))
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def closeEvent(self, event):
        """
        при закрытии окна показать главное окно . Событие формируется при закрытии окна.
        """
        wnd.show()


class Services_up_win(QDialog, Ui_Dialog):
    """
    Окно "Обновление данных по Сервисным службам" .
    Вызывается из формы "Сервисные службы" по нажатию на кнопку "Обновить строку"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

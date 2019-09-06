import sqlite3
import sys
from PyQt5 import QtCore, QtSql
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtSql import QSqlQueryModel, QSqlRelation, QSqlRelationalDelegate, QSqlQuery
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QTableWidgetItem, QMessageBox, \
    QAbstractItemView, QHeaderView
from PyQT_BD.My_PyQt_db.ui_main import Ui_MainWindow
from PyQT_BD.My_PyQt_db.ui_main_edit import Ui_EdMain

from PyQT_BD.My_PyQt_db.ui_services import Ui_Dialog_services
from PyQT_BD.My_PyQt_db.ui_services_update import Ui_Dialog
from PyQT_BD.My_PyQt_db.ui_unit import Ui_Dialog_unit
from PyQT_BD.My_PyQt_db.ui_unit_new import Ui_Dialog_unit_new
from PyQT_BD.My_PyQt_db.ui_unit_update import Ui_Dialog_unit_update
from PyQT_BD.My_PyQt_db.ui_user import Ui_Dialog_user
from PyQT_BD.My_PyQt_db.ui_user_new import Ui_Dialog_user_new
from PyQT_BD.My_PyQt_db.ui_user_update import Ui_Dialog_user_update


class Window(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        self.model = QSqlQueryModel()
        self.connectToSql()

        # Обработка действий по меню
        # нажата кнопка меню "Справочники -> Подразделения"
        self.unit_action.triggered.connect(self.unit_dialog)

        # нажата кнопка меню "Справочники -> Сотрудники"
        self.user_action.triggered.connect(self.user_dialog)

        # нажата кнопка меню "Справочники -> Сервисные службы"
        self.services_action.triggered.connect(self.services_dialog)

        # Работа с основной формой
        # Нажата кнопка "Добавить строку" на форме
        self.btProblemAdd.clicked.connect(self.bt_add)
        # Нажата кнопка "Обновить строку" на форме
        self.btProblemUpdate.clicked.connect(self.bt_upd)
        # Нажата кнопка "Удалить строку" на форме
        self.btProblemDel.clicked.connect(self.bt_del)
        # Найти заявку
        self.btProblemFind.clicked.connect(self.findText)
        # Сбросить фильтр
        self.btProblemReset.clicked.connect(self.reset)

    def connectToSql(self):
        """
        Открываем базу и создаем запрос и соединяем модель с таблицей
        """
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
        self.db.setDatabaseName("ProblemDB.db")
        if self.db.open():
            self.qry = QSqlQuery(self.db)
            self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO FROM def_message  d
            Left Join services s
            on d.idServices = s.id
            left join  User u
            on d.idUser = u.id""")
            self.qry.exec()

            self.model.setQuery(self.qry)
            self.tableView.setModel(self.model)
            self.tableView.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

            self.model.setHeaderData(0, Qt.Horizontal, '№ заявки')
            self.model.setHeaderData(1, Qt.Horizontal, 'Дата')
            self.model.setHeaderData(2, Qt.Horizontal, 'Служба')
            self.model.setHeaderData(3, Qt.Horizontal, 'Текст заявки')
            self.model.setHeaderData(4, Qt.Horizontal, 'ФИО заявителя')
        else:
            QMessageBox.critical(self, 'error', self.model.lastError().text())

    def bt_add(self):
        """
        Вызывается по нажатию кнопки "Добавить строку"
        """
        dialog_add = Ed_win(self)
        # Устанавливаем пустые значения в поля на форме
        dialog_add.edit_text.setText = ''
        dialog_add.cb_ser_name.setCurrentIndex(-1)
        dialog_add.cb_fio.setCurrentIndex(-1)
        # открываем окно добавления
        dialog_add.show()

        # Если нажата кнопка ОК на форме добавления
        if dialog_add.exec() == QDialog.Accepted:
            ser = dialog_add.cb_ser_name.currentText()
            user = dialog_add.cb_fio.currentText()

            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
            self.db.setDatabaseName("ProblemDB.db")

            if self.db.open():
                qry1 = QSqlQuery(self.db)
                qry1.prepare("""SELECT s.id FROM  services s
                where s.name =:ser""")
                qry1.bindValue(":ser", ser)
                qry1.exec()
                qry1.next()
                servId = qry1.value(0)

                qry1.prepare("""SELECT u.id FROM  User u
                                where u.FIO =:user""")
                qry1.bindValue(":user", user)
                qry1.exec()
                qry1.next()
                userId = qry1.value(0)

                qry1.prepare("""INSERT INTO def_message(idServices, text,idUser) 
                        VALUES(:idService, :text,:idUser)""")

                qry1.bindValue(":idService", servId)
                qry1.bindValue(":text", dialog_add.edit_text.text())
                qry1.bindValue(":idUser", userId)
                qry1.exec()

                self.qry = QSqlQuery(self.db)
                self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO 
                        FROM def_message  d
                        Left Join services s
                        on d.idServices = s.id
                        left join  User u
                        on d.idUser = u.id""")
                self.qry.exec()

                self.model.setQuery(self.qry)
                self.tableView.setModel(self.model)
            else:
                QMessageBox.critical(self, 'error', self.model.lastError().text())

    def bt_upd(self):
        """
        Вызывается по нажатию кнопки "Изменить строку"
        """
        dialog_add = Ed_win(self)

        # определяем индекс строки в таблице
        index = self.tableView.currentIndex().row()
        print(index)
        if index==-1:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')
        else:
            # определяем id строки в таблице в базе данных
            nom = str(self.model.data(self.model.index(index, 0), Qt.DisplayRole))

            # устанавливаем текст заявки в поле edit_text
            dialog_add.edit_text.setText(str(self.model.data(self.model.index(index, 3), Qt.DisplayRole)))

            # Данные по сервисной службе
            index_serv = dialog_add.cb_ser_name.findText(
                str(self.model.data(self.model.index(index, 2), Qt.DisplayRole)))

            if index_serv > -1:
                dialog_add.cb_ser_name.setCurrentIndex(index_serv)
            else:
                dialog_add.cb_ser_name.setCurrentIndex(-1)

            # Данные по сотруднику, который подал заявку
            index_fio = dialog_add.cb_fio.findText(str(self.model.data(self.model.index(index, 4), Qt.DisplayRole)))

            if index_fio > -1:
                dialog_add.cb_fio.setCurrentIndex(index_fio)
            else:
                dialog_add.cb_fio.setCurrentIndex(-1)

            # ОТкрываем окно с данными для редактирования
            dialog_add.show()

            # если нажата кнопка ОК в окне для редактирования строки
            if dialog_add.exec() == QDialog.Accepted:
                ser = dialog_add.cb_ser_name.currentText()
                user = dialog_add.cb_fio.currentText()

                self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
                self.db.setDatabaseName("ProblemDB.db")

                if self.db.open():
                    qry1 = QSqlQuery(self.db)
                    qry1.prepare("""SELECT s.id FROM  services s
                                   where s.name =:ser""")
                    qry1.bindValue(":ser", ser)
                    qry1.exec()
                    qry1.next()
                    servId = qry1.value(0)

                    qry1.prepare("""SELECT u.id FROM  User u
                                                   where u.FIO =:user""")
                    qry1.bindValue(":user", user)
                    qry1.exec()
                    qry1.next()
                    userId = qry1.value(0)

                    qry1.prepare("""UPDATE def_message SET idServices=:servId, text=:txt,idUser=:userId WHERE id=:id""")
                    qry1.bindValue(":servId", servId)
                    qry1.bindValue(":txt", dialog_add.edit_text.text())
                    qry1.bindValue(":userId", userId)
                    qry1.bindValue(":id", nom)
                    qry1.exec()

                    # снова делаем выборку данных после проведения обновления данных
                    self.qry = QSqlQuery(self.db)
                    self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO FROM def_message  d
                                                   Left Join services s
                                                   on d.idServices = s.id
                                                   left join  User u
                                                   on d.idUser = u.id""")
                    self.qry.exec()

                    self.model.setQuery(self.qry)
                    self.tableView.setModel(self.model)
                else:
                    QMessageBox.critical(self, 'error', self.model.lastError().text())




    def bt_del(self):
        """
        Вызывается по нажатию кнопки "Удалить строку"
        """
        quit_msg = "Подтвердите удаление записи"
        reply = QMessageBox.question(self, 'Confirm', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            index = self.tableView.currentIndex().row()
            nom = str(self.model.data(self.model.index(index, 0), Qt.DisplayRole))
            self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
            self.db.setDatabaseName("ProblemDB.db")

            if self.db.open():
                qry1 = QSqlQuery(self.db)
                qry1.prepare("""DELETE  FROM  def_message 
                                           where id =:id""")
                qry1.bindValue(":id", nom)
                qry1.exec()

                self.qry = QSqlQuery(self.db)
                self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO FROM def_message  d
                                                               Left Join services s
                                                               on d.idServices = s.id
                                                               left join  User u
                                                               on d.idUser = u.id""")
                self.qry.exec()
                self.model.setQuery(self.qry)
                self.tableView.setModel(self.model)
            else:
                QMessageBox.critical(self, 'error', self.model.lastError().text())

    def findText(self):
        """
        Вызывается по кнопке "Найти заявку"
        """
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
        self.db.setDatabaseName("ProblemDB.db")

        if self.db.open():
            self.qry = QSqlQuery(self.db)
            self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO FROM def_message  d
                   Left Join services s
                   on d.idServices = s.id
                   left join  User u
                   on d.idUser = u.id where d.text Like :txt """)
            self.qry.bindValue(":txt", '%' + self.EditFind.text() + '%')
            self.qry.exec()

            self.model.setQuery(self.qry)
            self.tableView.setModel(self.model)
        else:
            QMessageBox.critical(self, 'error', self.model.lastError().text())

    def reset(self):
        """
        Вызывается по кнопке "Сбросить фильтр"
        """
        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
        self.db.setDatabaseName("ProblemDB.db")
        if self.db.open():
            self.qry = QSqlQuery(self.db)
            self.qry.prepare("""SELECT d.id, dat, s.name, d.text, u.FIO FROM def_message  d
                          Left Join services s
                          on d.idServices = s.id
                          left join  User u
                          on d.idUser = u.id """)
            self.qry.exec()

            self.model.setQuery(self.qry)
            self.tableView.setModel(self.model)
        else:
            QMessageBox.critical(self, 'error', self.model.lastError().text())

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

        # поиск
        self.lineEdit.textChanged.connect(self.text_changed_find)

    def text_changed_find(self):
        """
        Поиск в таблице
        """
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
        quit_msg = "Подтвердите удаление записи"
        reply = QMessageBox.question(self, 'Confirm', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            a = []
            if self.tableUnit.selectedItems():
                for currentQTableWidgetItem in self.tableUnit.selectedItems():
                    a.append(currentQTableWidgetItem.text())
                # Удаление строки
                sql = 'DELETE FROM  unit WHERE id  =' + str(a[0])
                con = sqlite3.connect('ProblemDB.db')
                cur = con.cursor()
                try:
                    cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    QMessageBox.information(self, 'Ошибка', err)
                else:
                    con.commit()
                cur.close()
                con.close()
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
        Функция вызывается по нажатию кнопки "Записать" на форме Новое подразделение
        """
        er1 = False
        er2 = False
        if self.Edit_Unit.text() == '':
            QMessageBox.information(self, 'Ошибка', 'Поле подразделение должно быть обязательно заполнено')
            er1 = True
        elif self.CB_unit.currentText() == '':
            con = sqlite3.connect('ProblemDB.db')
            cur = con.cursor()
            try:
                cur.execute('INSERT into unit(name,shortname) VALUES (?,?)',
                            (self.Edit_Unit.text(), self.Edit_Short_Unit.text()))
            except sqlite3.DatabaseError as err:
                QMessageBox.information(self, 'Ошибка', err)
            else:
                con.commit()
            cur.close()
            con.close()
        else:
            # подразделение вышестоящее
            sql = """SELECT id FROM unit where name ='""" + self.CB_unit.currentText() + """'"""
            con = sqlite3.connect('ProblemDB.db')
            cur = con.cursor()
            try:
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Ошибка', 'Введено не верное название поразделения')
                else:
                    er2 = False
                    with sqlite3.connect('ProblemDB.db') as con:
                        cur = con.cursor()
                        con.execute('INSERT into unit(name,shortname,unitId) VALUES (?,?,?)',
                                    (self.Edit_Unit.text(), self.Edit_Short_Unit.text(), str(id_un[0])))
                        con.commit()
            except sqlite3.DatabaseError as err:
                QMessageBox.information(self, 'Ошибка', err)
            else:
                con.commit()
            cur.close()
            con.close()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_unit_new(self):
        """
        Функция вызывается по нажатию кнопки "Отмена"
        """
        self.close()

    def findText(self, s):
        """
        функция поиска введенного текста в поле Подразделение
        :param s: строка текста для поиска соответствия
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
                con.execute('UPDATE unit set name=?,shortname=? where id=?',
                            (self.Edit_Unit_up.text(), self.Edit_Short_Unit_up.text()), self.Edit_Id.text())
                con.commit()
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
                        con.execute('UPDATE unit set name= ?,shortname=?,unitId=? where id=?',
                                    (self.Edit_Unit_up.text(), self.Edit_Short_Unit_up.text(), str(id_un[0]),
                                     self.Edit_Id.text()))
                        con.commit()

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
        """
        Поиск строки
        :return:
        """
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
        quit_msg = "Подтвердите удаление записи"
        reply = QMessageBox.question(self, 'Confirm', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            a = []
            if self.tableUser.selectedItems():
                for currentQTableWidgetItem in self.tableUser.selectedItems():
                    a.append(currentQTableWidgetItem.text())
                # Удаление строки
                sql = 'DELETE FROM  user WHERE id  =' + str(a[0])
                con = sqlite3.connect('ProblemDB.db')
                cur = con.cursor()
                try:
                    cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    QMessageBox.information(self, 'Ошибка', err)
                else:
                    con.commit()
                cur.close()
                con.close()
                self.tableUser.removeRow(currentQTableWidgetItem.row())

            else:
                QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_user(self):
        """
        Функция выполняется при нажатии кнопки "Обновить строку" на форме "Сотрудники"
        :return: Открывает окно для обновления  данных
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
                index = dialog_user_update.CB_unit_up.findText(str(a[4]))
                if index > -1:
                    dialog_user_update.CB_unit_up.setCurrentIndex(index)

            # Показываем форму для изменения значений
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
        self.CB_unit.editTextChanged.connect(self.find_Text)

        # нажата кнопка "Записать"
        self.btnUser_Ok.clicked.connect(self.bt_ok_user_new)
        # нажата кнопка "Отмена"
        self.btnUser_Cancel.clicked.connect(self.bt_cancel_user_new)

    def bt_ok_user_new(self):
        """
        Функция вызывается по нажатию кнопки "Записать" на форме Добавить сотрудника
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
                        con.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_user_new(self):
        """
        Функция вызывается по нажатию кнопки "Отмена" на форме Добавить сотрудника
        :return:
        """
        self.close()

    def find_Text(self, s):
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
        Функция вызывается по нажатию кнопки "Записать" на форме Обновить данные по сотруднику
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
                        con.execute('Update user set FIO= ? , birthday= ?, gender =? ,unitId=? where id =?',
                                    (self.Edit_Fio_up.text(), str(td), p, str(id_un[0]), self.Edit_Id.text()))
                        con.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_user_up(self):
        """
            Функция вызывается по нажатию кнопки "Отмена" на форме Обновить данные по сотруднику
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
        """
        Поиск данных в таблице
        :return:
        """
        items = self.tableSevices.findItems(self.lineEdit.text(), QtCore.Qt.MatchContains)
        if items:  # если список не пустой
            # установить текущей первую из найденых ячеек
            self.tableSevices.selectRow(items[0].row())

    def bt_add_services(self):
        """
        Функция выполняется при нажатии кнопки "Добавить строку" на форме "Сервисные службы"
        :return: Открывает окно для ввода данных
        """
        serv, ok = QInputDialog.getText(self, 'Добавить', 'Название сервисной службы')
        table = self.tableSevices

        if ok:
            con = sqlite3.connect('ProblemDB.db')
            cur = con.cursor()
            cur.execute('INSERT into services(name) VALUES (?)', (serv,))
            con.commit()
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
        quit_msg = "Подтвердите удаление записи"
        reply = QMessageBox.question(self, 'Confirm', quit_msg, QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            a = []
            if self.tableSevices.selectedItems():
                for currentQTableWidgetItem in self.tableSevices.selectedItems():
                    a.append(currentQTableWidgetItem.text())

                # Удаление строки
                sql = 'DELETE FROM  services WHERE id  =' + str(a[0])
                con = sqlite3.connect('ProblemDB.db')
                cur = con.cursor()
                try:
                    cur.execute(sql)
                except sqlite3.DatabaseError as err:
                    QMessageBox.information(self, 'Ошибка', err)
                else:
                    con.commit()
                cur.close()
                con.close()
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
                    cur = con.cursor()
                    cur.execute(sql)
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


class Ed_win(QDialog, Ui_EdMain):
    """
    Окно для добавления и редактирования записи
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)
        self.servM = QSqlQueryModel()
        self.userM = QSqlQueryModel()

        self.db = QtSql.QSqlDatabase.addDatabase("QSQLITE")  # создаём подключение
        self.db.setDatabaseName("ProblemDB.db")

        if self.db.open():
            qry = QSqlQuery(self.db)
            qry.prepare('select name from services')
            qry.exec()
            # QMessageBox.information(self, 'Отладка', 'select name from services')
            self.servM.setQuery(qry)
            # QMessageBox.information(self, 'Отладка', '3')
            self.cb_ser_name.setModel(self.servM)

            qry.prepare('select FIO from User')
            qry.exec()
            self.userM.setQuery(qry)
            self.cb_fio.setModel(self.userM)
        else:
            QMessageBox.critical(self, 'error', self.model.lastError().text())

        self.btnOk.clicked.connect(self.bt_ok)
        self.btnCancel.clicked.connect(self.bt_cancel)

    def bt_ok(self):
        """
            Функция вызывается по нажатию кнопки "ОК"
        """
        self.accept()

    def bt_cancel(self):
        """
        Функция вызывается по нажатию кнопки "Отменить"
        """
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

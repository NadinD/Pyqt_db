import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QTableWidgetItem, QMessageBox
from PyQT_BD.My_PyQt_db.ui_main import Ui_MainWindow

from PyQT_BD.My_PyQt_db.ui_services import Ui_Dialog_services
from PyQT_BD.My_PyQt_db.ui_services_update import Ui_Dialog
from PyQT_BD.My_PyQt_db.ui_user import Ui_Dialog_user
from PyQT_BD.My_PyQt_db.ui_user_new import Ui_Dialog_user_new


class Window(QMainWindow, Ui_MainWindow):
    """
    Основное окно программы
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # нажата кнопка меню "Справочники -> Сотрудники"
        self.user_action.triggered.connect(self.user_dialg)

        # нажата кнопка меню "Справочники -> Сервисные службы"
        self.services_action.triggered.connect(self.services_dialg)

    def user_dialg(self):
        """
        Функция выполняется при нажатии кнопки меню "Справочники -> Сотрудники"
        :return: Открывает окно с таблицей информации по отрудникам (User_win)
        """
        dialog_user = User_win(self)
        dialog_user.show()
        # Скрываем основное окно программы
        wnd.hide()

    def services_dialg(self):
        """
         Функция выполняется при нажатии кнопки меню "Справочники -> Сервисные службы"
        :return: Открывает окно с таблицей информации по сервисным службам (Services_win)
        """
        dialog = Services_win(self)
        dialog.show()
        # Скрываем основное окно программы
        wnd.hide()


class User_win(QDialog, Ui_Dialog_user):
    """
    Окно программы "Сотрудники"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        # Соединение с базой
        con = sqlite3.connect('ProblemDB.db')
        # Заполнение таблицы
        for row_number, row in enumerate(con.execute("""select u.id,u.FIO, u.birthday, u.gender, un.name
        from User as u
        LEFT JOIN  unit as un
        on  un.id= u.unitId""").fetchall()):
            self.tableUser.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.tableUser.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.tableUser.setSortingEnabled(True)

        # Нажата кнопка "Добавить строку" на форме "Сотрудники"
        self.btUserAdd.clicked.connect(self.bt_add_user)
        # Нажата кнопка "Удалить строку" на форме "Сотрудники"
        self.btUserDel.clicked.connect(self.bt_del_user)
        # # Нажата кнопка "Обновить строку" на форме "Сотрудники"
        # self.btUserUpdate.clicked.connect(self.bt_upd_user)

    def bt_add_user(self):
        dialog_user_new = User_new_win(self)
        with sqlite3.connect('ProblemDB.db') as con:
            data = con.execute('SELECT name FROM unit').fetchall()

            dialog_user_new.CB_unit.clear()
            for row in data:
                dialog_user_new.CB_unit.addItem(*row)
            # Устанвливаем "ПУСТУЮ" строку -ничего не выбрано из списка
            dialog_user_new.CB_unit.setCurrentIndex(-1)
        dialog_user_new.show()

        if dialog_user_new.exec() == QDialog.Accepted:
            self.tableUser.setRowCount(0)
            for row_number, row in enumerate(con.execute("""select u.id,u.FIO, u.birthday, u.gender, un.name
                        from User as u
                        LEFT JOIN  unit as un
                        on  un.id= u.unitId""").fetchall()):
                self.tableUser.insertRow(row_number)
                for col_number, col in enumerate(row):
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
            #     print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            print(a)
            # Удаление строки
            sql = 'DELETE FROM  user WHERE id  =' + str(a[0])
            # QMessageBox.information(self, 'Remove item', sql)
            # with sqlite3.connect('ProblemDB.db') as con:
            self.con = sqlite3.connect('ProblemDB.db')
            # QMessageBox.information(self, 'соединение с базой', 'соединение с базой')

            self.con.execute(sql)
            # QMessageBox.information(self, 'соединение с базой', '2')
            self.con.commit()
            # QMessageBox.information(self, 'соединение с базой', '3')
            self.tableUser.removeRow(currentQTableWidgetItem.row())
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_user(self):
        pass

    def closeEvent(self, event):
        """
        при закрытии окна показать главное окно . Событие формируется при закрытии окна.
        """
        wnd.show()


class User_new_win(QDialog, Ui_Dialog_user_new):
    """
    Окно "Добавление данных по Сотрудникас" .
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
                QMessageBox.information(self, 'Отладка', str(sql))
                cur = con.cursor()
                cur.execute(sql)
                id_un = cur.fetchone()
                if id_un == None:
                    er2 = True
                    QMessageBox.information(self, 'Отладка', 'Введено не верное название поразделения')
                else:
                    print(id_un)
                    er2 = False
                    # print(id_un[0])
                    QMessageBox.information(self, 'Отладка', str(id_un))
                    with sqlite3.connect('ProblemDB.db') as con:
                        con.execute('INSERT into user(FIO,birthday,gender,unitId) VALUES (?,?,?,?)',
                                    (self.Edit_Fio.text(), str(td), p, str(id_un[0])))
                        con.commit()

        if (not er1 and not er2):
            self.accept()

    def bt_cancel_user_new(self):
        self.close()
        # pass

    def findText(self, s):
        """
        функция поиска введенного текста в поле Подразделение
        :param s: строка текста для поиска соответствия
        :return:
        """
        index = self.CB_unit.findText(s)
        if index > -1:
            self.CB_unit.setCurrentIndex(index)


class Services_win(QDialog, Ui_Dialog_services):
    """
      Окно программы "Сервисные службы"
    """

    def __init__(self, *args):
        super().__init__(*args)
        self.setupUi(self)

        # Соединение с базой
        con = sqlite3.connect('ProblemDB.db')
        # Заполнение таблицы
        for row_number, row in enumerate(con.execute("""select id,name from services""").fetchall()):
            self.tableSevices.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.tableSevices.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.tableSevices.setSortingEnabled(True)
        # Нажата кнопка "Добавить строку" на форме "Сервисные службы"
        self.btServicesAdd.clicked.connect(self.bt_add_services)
        # Нажата кнопка "Удалить строку" на форме "Сервисные службы"
        self.btServicesDel.clicked.connect(self.bt_del_services)
        # Нажата кнопка "Обновить строку" на форме "Сервисные службы"
        self.btServicesUpdate.clicked.connect(self.bt_upd_services)

    def bt_add_services(self):
        """
        Функция выполняется при нажатии кнопки "Добавить строку" на форме "Сервисные службы"
        :return: Открывает окно для ввода данных
        """
        serv, ok = QInputDialog.getText(self, 'Добавить', 'Название сервисной службы')
        table = self.tableSevices

        if ok:
            with sqlite3.connect('ProblemDB.db') as con:
                con.execute('INSERT into services(name) VALUES (?)', (serv,))
                con.commit()
                table.setRowCount(0)
                for row_number, row in enumerate(con.execute("""select id,name from services""").fetchall()):
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
            #     print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
            print(a)
            # Удаление строки
            sql = 'DELETE FROM  services WHERE id  =' + str(a[0])
            # QMessageBox.information(self, 'Remove item', sql)
            # with sqlite3.connect('ProblemDB.db') as con:
            self.con = sqlite3.connect('ProblemDB.db')
            # QMessageBox.information(self, 'соединение с базой', 'соединение с базой')

            self.con.execute(sql)
            # QMessageBox.information(self, 'соединение с базой', '2')
            self.con.commit()
            # QMessageBox.information(self, 'соединение с базой', '3')
            self.tableSevices.removeRow(currentQTableWidgetItem.row())
        else:
            QMessageBox.information(self, 'Ошибка', 'Строка не выбрана')

    def bt_upd_services(self):
        """
        Функция выполняется при нажатии кнопки "Обновить строку" на форме "Сервисные службы"
        :return: Открывает окно для обновления данных (Services_up_win)
        """
        # self.tableSevices.setItem(0, 0, QTableWidgetItem('5'))
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
                QMessageBox.information(self, 'update item', sql)
                # with sqlite3.connect('ProblemDB.db') as con:
                self.con = sqlite3.connect('ProblemDB.db')
                # QMessageBox.information(self, 'соединение с базой', 'соединение с базой')

                self.con.execute(sql)
                # QMessageBox.information(self, 'соединение с базой', '2')
                self.con.commit()
                self.tableSevices.setItem(currentQTableWidgetItem.row(), 1,
                                          QTableWidgetItem(dial_upd.lineEdit.text()))
                # QMessageBox.information(self, 'проверка', dial_upd.lineEdit.text())
                # QMessageBox.information(self, 'проверка', str(currentQTableWidgetItem.row()))
            # dial_upd.show()
            # self.dialog.hide()
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

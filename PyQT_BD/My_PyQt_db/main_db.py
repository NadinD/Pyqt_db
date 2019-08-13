import sqlite3
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog, QInputDialog, QTableWidgetItem, QMessageBox
from PyQT_BD.My_PyQt_db.ui_main import Ui_MainWindow

from PyQT_BD.My_PyQt_db.ui_services import Ui_Dialog_services
from PyQT_BD.My_PyQt_db.ui_services_update import Ui_Dialog


class Window(QMainWindow, Ui_MainWindow):
    """
    Основное окно программы
    """

    def __init__(self):
        super().__init__()
        self.setupUi(self)

        # нажата кнопка меню "Справочники -> Сервисные службы"
        self.services_action.triggered.connect(self.services_dialg)

    def services_dialg(self):
        """
         Функция выполняется при нажатии кнопки меню "Справочники -> Сервисные службы"
        :return: Открывает окно с таблицей информации по сервисным службам (Services_win)
        """
        dialog = Services_win(self)
        dialog.show()
        # Скрываем основное окно программы
        wnd.hide()


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

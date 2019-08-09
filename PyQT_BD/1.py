import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QWidget, QTableWidget, QVBoxLayout, QTableWidgetItem, QAbstractItemView, \
    QPushButton, QMessageBox, QCalendarWidget, QLineEdit, QFormLayout, QHBoxLayout, QDialog


class Window(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 300)

        self.layout = QVBoxLayout()
        self.table = QTableWidget()

        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            '№ заявки', 'Дата', 'Служба', 'Текст \n неисправности', 'ФИО сотрудника', 'Подразделение',
        ])
        # self.table.cellClicked(self.remove_item())
        # Разрешаем    выделение     только      одного     элемента
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        # Разрешаем выделение построчно
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        # # Скрываем колонку под номером 0
        # self.table.hideColumn(0)

        # self.table.doubleClicked.connect(self.remove_item)

        self.add = QPushButton('Добавить запись', self)
        self.add.clicked.connect(self.add_item)

        self.update = QPushButton('Обновить запись', self)
        self.update.clicked.connect(self.update_item)

        self.remove = QPushButton('Удалить запись', self)
        self.remove.clicked.connect(self.remove_item)

        con = sqlite3.connect('DefectDB.db')

        for row_number, row in enumerate(con.execute("""select d.id,d.dat,s.name, d.text, u.FIO,un.name
        from def_message as d
 left join user u
  on d.idUser=u.id
 left join   [services] as s
  on d.idServices =s.id
  left join [unit] un
  on u.unitId =un.id
        """
                                                     ).fetchall()):
            self.table.insertRow(row_number)
            for col_number, col in enumerate(row):
                self.table.setItem(row_number, col_number, QTableWidgetItem(str(col)))
            # for col_number, col in enumerate(row):
            #     table.setItem(row_number, col_number, QTableWidgetItem(str(col)))
        self.table.setSortingEnabled(True)

        con.close()

        self.layout.addWidget(self.table)
        self.layout.addWidget(self.add)
        self.layout.addWidget(self.update)
        self.layout.addWidget(self.remove)

        self.setLayout(self.layout)

    def update_item(self):
        pass
        # для обновления значений
        self.table.setItem(0, 2, QTableWidgetItem('5'))
        # row = self.table.currentRow
        # column = self.table.currentColumn
        # self.ID = self.table.item(row, column)

        # print("Row %d and Column %d was clicked" % (row, column))
        # item = self.table.itemAt(row, column)
        # self.ID = item.text()

    def add_item(self):
        # для обновления значений
        # self.table.setItem(0, 2, QTableWidgetItem('5'))
        # dialog = Dialog(self)
        # dialog.show()

        # pass
        dialog = Dialog(self)
        if dialog.exec():
            table = self.table
            row_number = table.rowCount()
            table.insertRow(row_number)
            table.setItem(row_number, 1, QTableWidgetItem(dialog.birth_day_date.selectedDate().toString()))
            table.setItem(row_number, 3, QTableWidgetItem(dialog.name.text()))
            # table.setItem(row_number, 1, QTableWidgetItem(dialog.email_address.text()))

            table.resizeColumnsToContents()

    # @pyqtSlot()
    def remove_item(self):
        # self.table.selectedItems()
        # информация из выбранной строки
        a = []

        for currentQTableWidgetItem in self.table.selectedItems():
            a.append(currentQTableWidgetItem.text())
            print(currentQTableWidgetItem.row(), currentQTableWidgetItem.column(), currentQTableWidgetItem.text())
        print(a)

        # Удаление строки

        sql = 'DELETE FROM  def_message WHERE id  =' + str(a[0])
        # QMessageBox.information(self, 'Remove item', sql)
        self.con = sqlite3.connect('DefectDB.db')
        # QMessageBox.information(self, 'соединение с базой', 'соединение с базой')

        self.con.execute(sql)
        self.con.commit()
        self.con.close()
        self.table.removeRow(currentQTableWidgetItem.row())

            # QMessageBox.information(self, 'Ошибка', 'нет соединения с базой')

        # table = self.table
        # rows = self.table.selectionModel().selectedRows()
        # print(self.table.currentRow())
        # print(self.table.selectedItems()[1])

        # if len(rows) > 0:
        #     msg = f'Are you sure you want to remove {"" if len(rows) == 1 else len(rows)} item' \
        #           f'{"" if len(rows) == 1 else "s"}?'
        #     reply = QMessageBox.question(
        #         self, f'Remove item{"" if len(rows) == 1 else "s"}', msg,
        #         QMessageBox.Yes, QMessageBox.No)
        #     if reply == QMessageBox.Yes:
        #         for index in sorted(rows, reverse=True):
        #             table.model().removeRow(index.row())
        # else:
        #     msg = 'Nothing to remove'
        #     QMessageBox.information(self, 'Remove item', msg)

class Dialog(QDialog):
    def __init__(self, *args):
        super().__init__(*args)

        self.name = None
        self.email_address = None
        self.birth_day_date = None

        self.setWindowTitle('Add new item')
        self.init_ui()

    def init_ui(self):
        form_layout = QFormLayout()

        self.name = QLineEdit(self)
        self.name.setMinimumWidth(300)
        form_layout.addRow('Текст неисправности:', self.name)

        self.email_address = QLineEdit(self)
        self.email_address.setMinimumWidth(300)
        form_layout.addRow('E-Mail:', self.email_address)

        self.birth_day_date = QCalendarWidget(self)
        form_layout.addRow('Дата:', self.birth_day_date)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)

        ok = QPushButton('Ok', self)
        ok.clicked.connect(self.accept)
        buttons_layout.addWidget(ok)

        cancel = QPushButton('Cancel', self)
        cancel.clicked.connect(self.close)
        buttons_layout.addWidget(cancel)

        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.addLayout(form_layout)
        main_layout.addLayout(buttons_layout)
        self.setLayout(main_layout)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = Window()
    wnd.show()
    sys.exit(app.exec())

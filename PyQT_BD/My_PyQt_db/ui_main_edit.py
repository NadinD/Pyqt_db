# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_edit.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_EdMain(object):
    def setupUi(self, EdMain):
        EdMain.setObjectName("EdMain")
        EdMain.resize(635, 415)
        self.verticalLayout = QtWidgets.QVBoxLayout(EdMain)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)
        self.label_2 = QtWidgets.QLabel(EdMain)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.cb_ser_name = QtWidgets.QComboBox(EdMain)
        self.cb_ser_name.setObjectName("cb_ser_name")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.cb_ser_name)
        self.label_3 = QtWidgets.QLabel(EdMain)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label_3)
        self.edit_text = QtWidgets.QLineEdit(EdMain)
        self.edit_text.setObjectName("edit_text")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.edit_text)
        self.label_4 = QtWidgets.QLabel(EdMain)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_4)
        self.cb_fio = QtWidgets.QComboBox(EdMain)
        self.cb_fio.setObjectName("cb_fio")
        self.formLayout.setWidget(5, QtWidgets.QFormLayout.FieldRole, self.cb_fio)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.btnOk = QtWidgets.QPushButton(EdMain)
        self.btnOk.setObjectName("btnOk")
        self.horizontalLayout_2.addWidget(self.btnOk)
        self.btnCancel = QtWidgets.QPushButton(EdMain)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.retranslateUi(EdMain)
        QtCore.QMetaObject.connectSlotsByName(EdMain)
        EdMain.setTabOrder(self.cb_ser_name, self.edit_text)

    def retranslateUi(self, EdMain):
        _translate = QtCore.QCoreApplication.translate
        EdMain.setWindowTitle(_translate("EdMain", "Dialog"))
        self.label_2.setText(_translate("EdMain", "Служба"))
        self.label_3.setText(_translate("EdMain", "Текст заявки"))
        self.label_4.setText(_translate("EdMain", "ФИО"))
        self.btnOk.setText(_translate("EdMain", "ОК"))
        self.btnCancel.setText(_translate("EdMain", "Отменить"))

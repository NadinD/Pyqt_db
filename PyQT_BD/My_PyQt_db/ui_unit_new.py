# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'unit_new.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(483, 361)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.formLayout.setContentsMargins(5, 10, 5, 2)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.Edit_Unit = QtWidgets.QLineEdit(Dialog)
        self.Edit_Unit.setObjectName("Edit_Unit")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Edit_Unit)
        self.label_2 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.label_2)
        self.Edit_Short_Unit = QtWidgets.QLineEdit(Dialog)
        self.Edit_Short_Unit.setObjectName("Edit_Short_Unit")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.Edit_Short_Unit)
        self.label_3 = QtWidgets.QLabel(Dialog)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.CB_Unit = QtWidgets.QComboBox(Dialog)
        self.CB_Unit.setObjectName("CB_Unit")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.CB_Unit)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btnUnit_Ok = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUnit_Ok.setFont(font)
        self.btnUnit_Ok.setObjectName("btnUnit_Ok")
        self.horizontalLayout_6.addWidget(self.btnUnit_Ok)
        self.btnUnit_Cancel = QtWidgets.QPushButton(Dialog)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUnit_Cancel.setFont(font)
        self.btnUnit_Cancel.setObjectName("btnUnit_Cancel")
        self.horizontalLayout_6.addWidget(self.btnUnit_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        spacerItem1 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "Подразделение"))
        self.label_2.setText(_translate("Dialog", "Сокращенное \n"
"название"))
        self.label_3.setText(_translate("Dialog", "Вышестоящие \n"
"подразделение"))
        self.btnUnit_Ok.setText(_translate("Dialog", "Записать"))
        self.btnUnit_Cancel.setText(_translate("Dialog", "Отмена"))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'user_update.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog_user_update(object):
    def setupUi(self, Dialog_user_update):
        Dialog_user_update.setObjectName("Dialog_user_update")
        Dialog_user_update.resize(533, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(Dialog_user_update)
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setContentsMargins(5, 10, 5, -1)
        self.formLayout.setSpacing(10)
        self.formLayout.setObjectName("formLayout")
        self.label = QtWidgets.QLabel(Dialog_user_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.label)
        self.Edit_Fio_up = QtWidgets.QLineEdit(Dialog_user_update)
        self.Edit_Fio_up.setObjectName("Edit_Fio_up")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.Edit_Fio_up)
        self.label_2 = QtWidgets.QLabel(Dialog_user_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.SpanningRole, self.label_2)
        self.Edit_date_up = QtWidgets.QDateEdit(Dialog_user_update)
        self.Edit_date_up.setObjectName("Edit_date_up")
        self.formLayout.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.Edit_date_up)
        self.label_3 = QtWidgets.QLabel(Dialog_user_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.formLayout.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chB_male_up = QtWidgets.QCheckBox(Dialog_user_update)
        self.chB_male_up.setObjectName("chB_male_up")
        self.buttonGroup = QtWidgets.QButtonGroup(Dialog_user_update)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.chB_male_up)
        self.horizontalLayout_2.addWidget(self.chB_male_up)
        self.chB_female_up = QtWidgets.QCheckBox(Dialog_user_update)
        self.chB_female_up.setObjectName("chB_female_up")
        self.buttonGroup.addButton(self.chB_female_up)
        self.horizontalLayout_2.addWidget(self.chB_female_up)
        self.formLayout.setLayout(4, QtWidgets.QFormLayout.FieldRole, self.horizontalLayout_2)
        self.label_4 = QtWidgets.QLabel(Dialog_user_update)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.formLayout.setWidget(6, QtWidgets.QFormLayout.SpanningRole, self.label_4)
        self.CB_unit_up = QtWidgets.QComboBox(Dialog_user_update)
        self.CB_unit_up.setObjectName("CB_unit_up")
        self.formLayout.setWidget(7, QtWidgets.QFormLayout.FieldRole, self.CB_unit_up)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(10)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem)
        self.btnUser_up_Ok = QtWidgets.QPushButton(Dialog_user_update)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUser_up_Ok.setFont(font)
        self.btnUser_up_Ok.setObjectName("btnUser_up_Ok")
        self.horizontalLayout_6.addWidget(self.btnUser_up_Ok)
        self.btnUser_up_Cancel = QtWidgets.QPushButton(Dialog_user_update)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.btnUser_up_Cancel.setFont(font)
        self.btnUser_up_Cancel.setObjectName("btnUser_up_Cancel")
        self.horizontalLayout_6.addWidget(self.btnUser_up_Cancel)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.Edit_Id = QtWidgets.QLineEdit(Dialog_user_update)
        self.Edit_Id.setEnabled(False)
        self.Edit_Id.setObjectName("Edit_Id")
        self.verticalLayout.addWidget(self.Edit_Id)
        spacerItem1 = QtWidgets.QSpacerItem(20, 42, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)

        self.retranslateUi(Dialog_user_update)
        QtCore.QMetaObject.connectSlotsByName(Dialog_user_update)

    def retranslateUi(self, Dialog_user_update):
        _translate = QtCore.QCoreApplication.translate
        Dialog_user_update.setWindowTitle(_translate("Dialog_user_update", "Обновить данные по сотруднику"))
        self.label.setText(_translate("Dialog_user_update", "ФИО"))
        self.label_2.setText(_translate("Dialog_user_update", "Дата рождения"))
        self.label_3.setText(_translate("Dialog_user_update", "Пол"))
        self.chB_male_up.setText(_translate("Dialog_user_update", "мужской"))
        self.chB_female_up.setText(_translate("Dialog_user_update", "женский"))
        self.label_4.setText(_translate("Dialog_user_update", "Подразделение"))
        self.btnUser_up_Ok.setText(_translate("Dialog_user_update", "Записать"))
        self.btnUser_up_Cancel.setText(_translate("Dialog_user_update", "Отмена"))

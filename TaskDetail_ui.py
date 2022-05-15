# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'TaskDetail.ui'
##
## Created by: Qt User Interface Compiler version 6.2.4
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QDialog, QGridLayout,
    QLabel, QLineEdit, QPlainTextEdit, QPushButton,
    QSizePolicy, QVBoxLayout, QWidget, QCalendarWidget, QHBoxLayout)

import datetime

class TaskDetailDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setObjectName("TaskDetailDialog")
        self.resize(350, 400)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.pushButtonSave = QPushButton("Save",self)
        self.pushButtonSave.setObjectName("pushButtonSave")

        self.gridLayout.addWidget(self.pushButtonSave, 5, 3, 1, 1)

        self.lineEditTask = QLineEdit(self)
        self.lineEditTask.setObjectName("lineEditTask")

        self.gridLayout.addWidget(self.lineEditTask, 0, 2, 1, 2)

        self.labelLog = QLabel("Log:",self)
        self.labelLog.setObjectName("labelLog")

        self.gridLayout.addWidget(self.labelLog, 4, 0, 1, 1)

        self.labelStart = QLabel("Start:",self)
        self.labelStart.setObjectName("labelStart")

        self.gridLayout.addWidget(self.labelStart, 2, 0, 1, 1)

        self.labelDue = QLabel("Due:",self)
        self.labelDue.setObjectName("labelDue")

        self.gridLayout.addWidget(self.labelDue, 3, 0, 1, 1)

        self.lineEditMember = QLineEdit(self)
        self.lineEditMember.setObjectName("lineEditMember")

        self.gridLayout.addWidget(self.lineEditMember, 1, 2, 1, 2)

        self.labelMember = QLabel("Member",self)
        self.labelMember.setObjectName("labelMember")

        self.gridLayout.addWidget(self.labelMember, 1, 0, 1, 1)

        self.labelTask = QLabel("Task",self)
        self.labelTask.setObjectName("labelTask")

        self.gridLayout.addWidget(self.labelTask, 0, 0, 1, 1)

        self.plainTextEditLog = QPlainTextEdit(self)
        self.plainTextEditLog.setObjectName("plainTextEditLog")

        self.gridLayout.addWidget(self.plainTextEditLog, 4, 2, 1, 2)

        self.lineEditStart = QDateTimeEdit(self)
        self.lineEditStart.setObjectName("lineEditStart")
        self.lineEditStart.setDateTime(datetime.datetime.now())
        self.lineEditStart.setCalendarPopup(True)
        self.lineEditStart.setDisplayFormat("dd/MM/yyyy HH:mm")

        self.gridLayout.addWidget(self.lineEditStart, 2, 2, 1, 2)

        self.lineEditDue = QDateTimeEdit(self)
        self.lineEditDue.setObjectName("lineEditDue")
        self.lineEditDue.setDateTime(datetime.datetime.now() + datetime.timedelta(days=7))
        self.lineEditDue.setCalendarPopup(True)
        self.lineEditStart.setDisplayFormat("dd/MM/yyyy HH:mm")

        self.gridLayout.addWidget(self.lineEditDue, 3, 2, 1, 2)


        self.verticalLayout.addLayout(self.gridLayout)

        self.pushButtonSave.clicked.connect(self.task_name)
        self.pushButtonSave.clicked.connect(self.task_member)
        self.pushButtonSave.clicked.connect(self.start_time)
        self.pushButtonSave.clicked.connect(self.due_time)
        self.pushButtonSave.clicked.connect(self.task_log)
        self.pushButtonSave.clicked.connect(self.close_event)

        self.flagSave = 0

        self.taskName = ""
        self.taskMember = ""
        self.startTime = ""
        self.dueTime = ""
        self.taskLog = ""

        QMetaObject.connectSlotsByName(self)
    # setupUi

    # --------------------------------------------------------------------------

    def task_name(self):
        self.taskName = self.lineEditTask.text()
        self.flagSave = 1
        return

    # --------------------------------------------------------------------------

    def task_member(self):
        self.taskMember = self.lineEditMember.text()
        self.flagSave = 1
        return

    # --------------------------------------------------------------------------

    def start_time(self):
        self.startTime = self.lineEditStart.dateTime()
        self.flagSave = 1
        return

    # --------------------------------------------------------------------------

    def due_time(self):
        self.dueTime = self.lineEditDue.dateTime()
        self.flagSave = 1
        return

    # --------------------------------------------------------------------------

    def task_log(self):
        self.taskLog = self.plainTextEditLog.toPlainText()
        self.flagSave = 1
        return

    # --------------------------------------------------------------------------

    def close_event(self):
        TaskDetailDialog.close(self)
        return

    # --------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    application = QApplication(sys.argv)

    # Create and show the dialog
    taskDetail = TaskDetailDialog()
    taskDetail.show()

    sys.exit(application.exec())

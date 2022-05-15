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
from PySide6.QtWidgets import QDoubleSpinBox

import datetime


class CreateBoard(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create a New Kanban Board")

        # Layout of the pop up
        self.setObjectName("CreateBoard")
        self.resize(250, 250)
        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.gridLayout = QGridLayout()
        self.gridLayout.setObjectName("gridLayout")

        # Save Button Place
        self.pushButtonSave = QPushButton("Save", self)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.gridLayout.addWidget(self.pushButtonSave, 5, 3, 1, 1)

        # Board Name Information
        self.lineEditBoardName = QLineEdit(self)
        self.lineEditBoardName.setObjectName("lineEditBoardName")
        self.gridLayout.addWidget(self.lineEditBoardName, 0, 2, 1, 2)
        self.labelBoardName = QLabel("Board Name", self)
        self.labelBoardName.setObjectName("labelBoardName")
        self.gridLayout.addWidget(self.labelBoardName, 0, 0, 1, 1)

        # Row Number Information
        self.labelRowNumber = QLabel("Row Number", self)
        self.gridLayout.addWidget(self.labelRowNumber, 1, 0, 1, 1)
        self.RowNumberEdit = QDoubleSpinBox(self)
        self.RowNumberEdit.setValue(1)
        self.RowNumberEdit.setMinimum(1)
        self.RowNumberEdit.setDecimals(0)
        self.gridLayout.addWidget(self.RowNumberEdit, 1, 2, 1, 2)

        # Column Number Information
        self.labelColumnNumber = QLabel("Column Number", self)
        self.gridLayout.addWidget(self.labelColumnNumber, 2, 0, 1, 1)
        self.ColumnNumberEdit = QDoubleSpinBox(self)
        self.ColumnNumberEdit.setValue(4)
        self.ColumnNumberEdit.setMinimum(4)
        self.ColumnNumberEdit.setDecimals(0)
        self.gridLayout.addWidget(self.ColumnNumberEdit, 2, 2, 1, 2)

        self.verticalLayout.addLayout(self.gridLayout)

        self.pushButtonSave.clicked.connect(self.board_name)
        self.pushButtonSave.clicked.connect(self.row_number)
        self.pushButtonSave.clicked.connect(self.column_number)

        self.flagSave = 0

        self.BoardName = ""
        self.RowNumber = ""
        self.ColumnNumber = ""

        QMetaObject.connectSlotsByName(self)

    # --------------------------------------------------------------------------

    def board_name(self):
        self.BoardName = self.lineEditBoardName.text()
        self.flagSave = 1
        return

    def row_number(self):
        self.RowNumber = self.RowNumberEdit.text()
        self.flagSave = 1
        return

    def column_number(self):
        self.ColumnNumber = self.ColumnNumberEdit.text()
        self.flagSave = 1
        return


if __name__ == "__main__":
    import sys

    application = QApplication(sys.argv)
    CreateNewBoard = CreateBoard()
    CreateNewBoard.show()
    sys.exit(application.exec())
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QIcon

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("Alex AI")
        MainWindow.setFixedSize(985, 617)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Create a QLabel for the GIF
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(200, 130, 601, 341))
        self.label.setText("")

        # Create a QMovie instance and set it to QLabel
        self.movie = QtGui.QMovie("gif.gif")  # Update with the correct path
        self.label.setMovie(self.movie)
        self.movie.start()

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(0, -10, 291, 561))
        self.label_2.setText("")
        self.label_2.setPixmap(QtGui.QPixmap("black.png"))
        self.label_2.setObjectName("label_2")

        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(0, 460, 641, 291))
        self.label_3.setText("")
        self.label_3.setPixmap(QtGui.QPixmap("black.png"))
        self.label_3.setObjectName("label_3")

        self.label_4 = QtWidgets.QLabel(self.centralwidget)
        self.label_4.setGeometry(QtCore.QRect(490, 460, 641, 291))
        self.label_4.setText("")
        self.label_4.setPixmap(QtGui.QPixmap("black.png"))
        self.label_4.setObjectName("label_4")

        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(700, 0, 291, 511))
        self.label_5.setText("")
        self.label_5.setPixmap(QtGui.QPixmap("black.png"))
        self.label_5.setObjectName("label_5")

        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(200, -130, 641, 291))
        self.label_6.setText("")
        self.label_6.setPixmap(QtGui.QPixmap("black.png"))
        self.label_6.setObjectName("label_6")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        icon = QIcon('icon.ico')
        MainWindow.setWindowIcon(icon)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("Alex AI", "Alex AI"))

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

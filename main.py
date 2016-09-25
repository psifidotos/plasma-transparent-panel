#! /usr/bin/env python2

import sys, os, shutil
from PyQt5 import QtGui, QtWidgets
from subprocess import call

def get_immediate_subdirectories(a_dir):
    return [name for name in os.listdir(a_dir)
            if os.path.isdir(os.path.join(a_dir, name))]


class MainWindow(QtWidgets.QWidget):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.initUI()


    def initUI(self):

        self.colActive = QtGui.QColor(30, 146, 255)
        self.colInactive = QtGui.QColor(150, 150, 150)

        panelsy = 100
        buttonsx = 75

        self.themeCmb = QtWidgets.QComboBox(self)

        self.deleteb = QtWidgets.QPushButton("Delete", self)
        self.deleteb.setEnabled(False)

        ## Labels
        chooseThemelbl = QtWidgets.QLabel("1. Theme",self)
        font = chooseThemelbl.font()
        font.setPointSize(16)
        chooseThemelbl.setFont(font)
        chooseThemelbl.move(10,10)

        setpanellbl = QtWidgets.QLabel("2. Panel",self)
        setpanellbl.setFont(font)
        setpanellbl.move(10,panelsy-40)

        # Panels visuals
        self.northSquare = QtWidgets.QFrame(self)
        self.northSquare.setGeometry(buttonsx+90, panelsy+30, 200, 30)
        self.northSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.westSquare = QtWidgets.QFrame(self)
        self.westSquare.setGeometry(self.northSquare.x()-30, self.northSquare.y()+self.northSquare.height()+10, 30, 120)
        self.westSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.eastSquare = QtWidgets.QFrame(self)
        self.eastSquare.setGeometry(self.northSquare.x()+self.northSquare.width(), self.westSquare.y(), self.westSquare.width(), self.westSquare.height())
        self.eastSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.southSquare = QtWidgets.QFrame(self)
        self.southSquare.setGeometry(self.northSquare.x(), self.westSquare.y()+self.westSquare.height()+10, self.northSquare.width(), self.northSquare.height())
        self.southSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())


        #Panels buttons visuals
        self.southb = QtWidgets.QPushButton('Bottom', self)
        self.southb.setCheckable(True)
        self.southb.move(buttonsx,panelsy-15)
        self.southb.clicked.connect(self.southClicked)

        self.northb = QtWidgets.QPushButton('Top', self)
        self.northb.setCheckable(True)
        self.northb.move(self.southb.x()+self.southb.width(),panelsy-15)
        self.northb.clicked.connect(self.northClicked)

        self.westb = QtWidgets.QPushButton('Left', self)
        self.westb.setCheckable(True)
        self.westb.move(self.northb.x()+self.northb.width(),panelsy-15)
        self.westb.clicked.connect(self.westClicked)

        self.eastb = QtWidgets.QPushButton('Right', self)
        self.eastb.setCheckable(True)
        self.eastb.move(self.westb.x()+self.westb.width(),panelsy-15)
        self.eastb.clicked.connect(self.eastClicked)

        #Shadows visuals
        shadowslbl = QtWidgets.QLabel("3. Shadows",self)
        shadowslbl.setFont(font)
        shadowslbl.move(10,self.southSquare.y()+self.southSquare.height()+5)

        shMargin = 15

        self.topleftShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-topleft.png")
        self.topleftShadow.setScaledContents(True)
        self.topleftShadow.setPixmap(self.pixmap)
        self.topleftShadow.setGeometry(self.southSquare.x()+2,self.southSquare.y()+self.southSquare.height()+60,shMargin,shMargin)

        self.topShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-top.png")
        self.topShadow.setScaledContents(True)
        self.topShadow.setPixmap(self.pixmap)
        self.topShadow.setGeometry(self.topleftShadow.x()+self.topleftShadow.width(),self.topleftShadow.y(),self.southSquare.width()-2*shMargin,shMargin)

        self.toprightShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-topright.png")
        self.toprightShadow.setScaledContents(True)
        self.toprightShadow.setPixmap(self.pixmap)
        self.toprightShadow.setGeometry(self.topShadow.x()+self.topShadow.width(),self.topShadow.y(),shMargin,shMargin)

        self.rightShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-right.png")
        self.rightShadow.setScaledContents(True)
        self.rightShadow.setPixmap(self.pixmap)
        self.rightShadow.setGeometry(self.toprightShadow.x(),self.toprightShadow.y()+self.toprightShadow.height(),shMargin,self.topShadow.width())

        self.bottomrightShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-bottomright.png")
        self.bottomrightShadow.setScaledContents(True)
        self.bottomrightShadow.setPixmap(self.pixmap)
        self.bottomrightShadow.setGeometry(self.rightShadow.x(),self.rightShadow.y()+self.rightShadow.height(),shMargin,shMargin)

        self.bottomShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-bottom.png")
        self.bottomShadow.setScaledContents(True)
        self.bottomShadow.setPixmap(self.pixmap)
        self.bottomShadow.setGeometry(self.topShadow.x(),self.bottomrightShadow.y(),self.topShadow.width(),shMargin)

        self.bottomleftShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-bottomleft.png")
        self.bottomleftShadow.setScaledContents(True)
        self.bottomleftShadow.setPixmap(self.pixmap)
        self.bottomleftShadow.setGeometry(self.topleftShadow.x(),self.bottomShadow.y(),shMargin,shMargin)

        self.leftShadow = QtWidgets.QLabel(self)
        self.pixmap = QtGui.QPixmap("images/shadow-left.png")
        self.leftShadow.setScaledContents(True)
        self.leftShadow.setPixmap(self.pixmap)
        self.leftShadow.setGeometry(self.topleftShadow.x(),self.rightShadow.y(),shMargin,self.rightShadow.height())

        #shadow buttons
        self.topleftb = QtWidgets.QPushButton('Top Left', self)
        self.topleftb.setCheckable(True)
        self.topleftb.move(buttonsx-5, self.topleftShadow.y()-30)
        self.topleftb.toggled.connect(self.topleftToggled)

        self.topb = QtWidgets.QPushButton('Top', self)
        self.topb.setCheckable(True)
        self.topb.move(self.topleftb.x()+self.topShadow.width()-self.topb.width()/6, self.topleftb.y())
        self.topb.toggled.connect(self.topToggled)

        self.toprightb = QtWidgets.QPushButton('Top Right', self)
        self.toprightb.setCheckable(True)
        self.toprightb.move(self.topleftb.x()+self.topleftb.width()+self.topShadow.width()+2*shMargin, self.topleftb.y())
        self.toprightb.toggled.connect(self.toprightToggled)

        self.rightb = QtWidgets.QPushButton('Right', self)
        self.rightb.setCheckable(True)
        self.rightb.move(self.toprightb.x(), self.toprightb.y()+self.toprightb.height()+self.rightShadow.height()/2)
        self.rightb.toggled.connect(self.rightToggled)

        self.bottomrightb = QtWidgets.QPushButton('Bottom Right', self)
        self.bottomrightb.setCheckable(True)
        self.bottomrightb.move(self.toprightb.x(), self.toprightb.y()+self.toprightb.height()+self.rightShadow.height()+2*shMargin)
        self.bottomrightb.toggled.connect(self.bottomrightToggled)

        self.bottomb = QtWidgets.QPushButton('Bottom', self)
        self.bottomb.setCheckable(True)
        self.bottomb.move(self.topb.x(), self.bottomrightb.y())
        self.bottomb.toggled.connect(self.bottomToggled)

        self.bottomleftb = QtWidgets.QPushButton('Bottom Left', self)
        self.bottomleftb.setCheckable(True)
        self.bottomleftb.move(self.topleftb.x()-0.5*shMargin, self.bottomrightb.y())
        self.bottomleftb.toggled.connect(self.bottomleftToggled)

        self.leftb = QtWidgets.QPushButton('Left', self)
        self.leftb.setCheckable(True)
        self.leftb.move(self.topleftb.x(), self.rightb.y())
        self.leftb.toggled.connect(self.leftToggled)


        self.southClicked(True)
        self.southb.clearFocus()

        self.setGeometry(300, 300, 550, 670)

        separator1 = QtWidgets.QFrame(self)
        separator1.setGeometry(self.northb.x()-20, self.northb.y()-20, 220, 1)
        separator1.setStyleSheet("QWidget { background-color: black }")

        separator2 = QtWidgets.QFrame(self)
        separator2.setGeometry(self.northb.x()-20, self.topb.y()-20, 220, 1)
        separator2.setStyleSheet("QWidget { background-color: black }")

        self.themeCmb.setGeometry(self.width()/2 - 150 ,chooseThemelbl.y()+15,300,30);

        #####generate button
        bottomspace = QtWidgets.QFrame(self)
        bottomspace.setGeometry(0, self.height()-40, self.width(), 40)
        bottomspace.setStyleSheet("QWidget { background-color: #4b4b4b }")

        self.generateb = QtWidgets.QPushButton('Generate New Theme', self)
        self.generateb.move(self.width()-90-self.generateb.width(), self.height()-6-self.generateb.height())

        self.deleteb.move(self.themeCmb.x()+self.themeCmb.width()+20,self.themeCmb.y())
        self.themeCmb.currentIndexChanged.connect(self.themeCurrentIndexChanged)
        self.generateb.clicked.connect(self.generateBtnClicked)
        self.deleteb.clicked.connect(self.deleteThemeBtnClicked)
        self.updateThemeCmb("")

        icon = QtGui.QIcon.fromTheme("preferences-desktop-color")
        self.setWindowIcon(icon)
        self.setWindowTitle('Transparent Panel')
        self.show()

    def northClicked(self, pressed):
        self.northSquare.setStyleSheet("QWidget { background-color: %s }" % self.colActive.name())
        self.westSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.eastSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.southSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.northb.setChecked(True)
        self.westb.setChecked(False)
        self.eastb.setChecked(False)
        self.southb.setChecked(False)

        self.topleftb.setChecked(False)
        self.topb.setChecked(False)
        self.toprightb.setChecked(False)
        self.rightb.setChecked(True)
        self.bottomrightb.setChecked(True)
        self.bottomb.setChecked(True)
        self.bottomleftb.setChecked(True)
        self.leftb.setChecked(True)

    def southClicked(self, pressed):
        self.northSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.westSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.eastSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.southSquare.setStyleSheet("QWidget { background-color: %s }" % self.colActive.name())

        self.southb.setChecked(True)
        self.westb.setChecked(False)
        self.eastb.setChecked(False)
        self.northb.setChecked(False)

        self.topleftb.setChecked(True)
        self.topb.setChecked(True)
        self.toprightb.setChecked(True)
        self.rightb.setChecked(True)
        self.bottomrightb.setChecked(False)
        self.bottomb.setChecked(False)
        self.bottomleftb.setChecked(False)
        self.leftb.setChecked(True)

    def eastClicked(self, pressed):
        self.northSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.westSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.eastSquare.setStyleSheet("QWidget { background-color: %s }" % self.colActive.name())
        self.southSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.southb.setChecked(False)
        self.westb.setChecked(False)
        self.eastb.setChecked(True)
        self.northb.setChecked(False)

        self.topleftb.setChecked(True)
        self.topb.setChecked(True)
        self.toprightb.setChecked(False)
        self.rightb.setChecked(False)
        self.bottomrightb.setChecked(False)
        self.bottomb.setChecked(True)
        self.bottomleftb.setChecked(True)
        self.leftb.setChecked(True)

    def westClicked(self, pressed):
        self.northSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.westSquare.setStyleSheet("QWidget { background-color: %s }" % self.colActive.name())
        self.eastSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())
        self.southSquare.setStyleSheet("QWidget { background-color: %s }" % self.colInactive.name())

        self.southb.setChecked(False)
        self.westb.setChecked(True)
        self.eastb.setChecked(False)
        self.northb.setChecked(False)

        self.topleftb.setChecked(False)
        self.topb.setChecked(True)
        self.toprightb.setChecked(True)
        self.rightb.setChecked(True)
        self.bottomrightb.setChecked(True)
        self.bottomb.setChecked(True)
        self.bottomleftb.setChecked(False)
        self.leftb.setChecked(False)


    def topToggled(self, checked):
        if not checked:
            self.topShadow.show()
        else:
            self.topShadow.hide()

    def topleftToggled(self, checked):
        if not checked:
            self.topleftShadow.show()
        else:
            self.topleftShadow.hide()

    def toprightToggled(self, checked):
        if not  checked:
            self.toprightShadow.show()
        else:
            self.toprightShadow.hide()

    def rightToggled(self, checked):
        if not checked:
            self.rightShadow.show()
        else:
            self.rightShadow.hide()

    def bottomrightToggled(self, checked):
        if not checked:
            self.bottomrightShadow.show()
        else:
            self.bottomrightShadow.hide()

    def bottomToggled(self, checked):
        if not checked:
            self.bottomShadow.show()
        else:
            self.bottomShadow.hide()

    def bottomleftToggled(self, checked):
        if not checked:
            self.bottomleftShadow.show()
        else:
            self.bottomleftShadow.hide()

    def leftToggled(self, checked):
        if not checked:
            self.leftShadow.show()
        else:
            self.leftShadow.hide()

    def themeCurrentIndexChanged(self, index):
        if self.themeCmb.itemText(index) in self.userthemes:
            self.deleteb.setEnabled(True)
        else:
            self.deleteb.setEnabled(False)


    def generateBtnClicked(self, pressed):

        self.panel=""

        if self.northb.isChecked():
            self.panel="North"
        elif self.southb.isChecked():
            self.panel="South"
        elif self.eastb.isChecked():
            self.panel="East"
        elif self.westb.isChecked():
            self.panel="West"

        self.shadows = []

        if self.topleftb.isChecked():
            self.shadows.append("-topleft")
        else:
            self.shadows.append("topleft")

        if self.topb.isChecked():
            self.shadows.append("-top")
        else:
            self.shadows.append("top")

        if self.toprightb.isChecked():
            self.shadows.append("-topright")
        else:
            self.shadows.append("topright")

        if self.rightb.isChecked():
            self.shadows.append("-right")
        else:
            self.shadows.append("right")

        if self.bottomrightb.isChecked():
            self.shadows.append("-bottomright")
        else:
            self.shadows.append("bottomright")

        if self.bottomb.isChecked():
            self.shadows.append("-bottom")
        else:
            self.shadows.append("bottom")

        if self.bottomleftb.isChecked():
            self.shadows.append("-bottomleft")
        else:
            self.shadows.append("bottomleft")

        if self.leftb.isChecked():
            self.shadows.append("-left")
        else:
            self.shadows.append("left")

        self.askThemeCreation()


    def askThemeCreation(self):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        newtheme=self.themeCmb.currentText()+' - '+self.panel+' Transparent'
        msg.setText("Would you like to create theme <b>"+newtheme+"</b> ?")
        msg.setWindowTitle("Create Theme Confirmation")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        retval = msg.exec_()

        if retval == QtGui.QMessageBox.Yes:
            command = 'python transparentpanel.py "'+self.themeCmb.currentText()+'" '+self.panel
            for shad in self.shadows:
                command = command + " " +shad
            os.system(str(command))
            self.updateThemeCmb(newtheme)
            msg2 = QtGui.QMessageBox()
            msg2.setIcon(QtGui.QMessageBox.Information)
            msg2.setText("Your new theme was created and you can activate it through Plasma System Settings")
            msg2.setWindowTitle("New Theme Created")
            msg2.setStandardButtons(QtGui.QMessageBox.Ok)
            retval2 = msg2.exec_()



    def updateThemeCmb(self, newTheme):
        self.themeCmb.clear()

        rootthemedir = "/usr/share/plasma/desktoptheme/"
        userthemedir = os.path.join(os.getenv("HOME"),".local/share/plasma/desktoptheme/")

        self.mainthemes = get_immediate_subdirectories(rootthemedir)
        self.userthemes = get_immediate_subdirectories(userthemedir)

        self.themeCmb.addItems(self.mainthemes)
        self.themeCmb.addItems(self.userthemes)

        if newTheme != "":
            indexPos=-1
            for i in range(0, self.themeCmb.count()-1):
                if self.themeCmb.itemText(i) == newTheme:
                    indexPos = i
            self.themeCmb.setCurrentIndex(indexPos)


    def deleteThemeBtnClicked(self, pressed):
        msg = QtGui.QMessageBox()
        msg.setIcon(QtGui.QMessageBox.Warning)

        msg.setText("Would you like to delete theme <b>"+self.themeCmb.currentText()+"</b> ?")
        msg.setWindowTitle("Delete Theme Confirmation")
        msg.setStandardButtons(QtGui.QMessageBox.Yes | QtGui.QMessageBox.No)

        retval = msg.exec_()

        if retval == QtGui.QMessageBox.Yes:
            themepath = os.path.join(os.getenv("HOME"),".local/share/plasma/desktoptheme/")
            themepath = os.path.join(themepath, str(self.themeCmb.currentText()) )
            if os.path.isdir(themepath):
                shutil.rmtree(themepath)
                self.updateThemeCmb("")


def main():
    app = QtWidgets.QApplication(sys.argv)
    ex = MainWindow()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()

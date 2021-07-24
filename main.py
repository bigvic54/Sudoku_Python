import copy
from random import randint
import sys
from PySide6 import QtCore, QtWidgets, QtGui


class Game:

    @staticmethod
    def printGrid(gridLocal):
        print("Grid is now: ")

        for i in range(0, 9):
            print(gridLocal[i])

    def __isSafeRow(self, row, num):
        for i in range(0, 9):
            if self.grid[row][i] == num:
                return False

        return True

    def __isSafeCol(self, col, num):
        for i in range(0, 9):
            if self.grid[i][col] == num:
                return False

        return True

    def __isSafeSquare(self, row, col, num):
        squareNum = self.coMat[row][col]
        x, y = self.squareCoord[squareNum]

        for i in range(0, 3):
            for j in range(0, 3):
                if self.grid[x + i][y + j] == num:
                    return False

        return True

    def __isSafe(self, row, col, num):
        if not self.__isSafeRow(row, num) or not self.__isSafeCol(col, num) or not self.__isSafeSquare(row, col, num):
            return False

        return True

    def __isGridFull(self):
        for i in range(0, 8):
            for j in range(0, 8):
                if self.grid[i][j] == 0:
                    return False

        return True

    def __generateSquare(self, row, col):
        x, y = row, col

        while x <= row + 2:
            if y > col + 2:
                if x == row + 2:
                    return

                else:
                    x += 1
                    y = col

            if self.grid[x][y] == 0:

                num = randint(1, 9)

                while not self.__isSafe(x, y, num):
                    num = randint(1, 9)

                self.grid[x][y] = num
                y += 1

    def __generateGridRec(self, row, col):

        if col >= 9 and row < 8:
            row += 1
            col = 0

        if row >= 9 and col >= 9:
            return True

        # We're located in the 0th square (1st on the diagonal).
        if row < 3:
            if col < 3:
                col = 3

        elif row < 6:
            # We're located in the 4th square (2nd on the diagonal).
            if col == (row // 3) * 3:
                col += 3

        else:
            if col == 6:
                row += 1
                col = 0
                if row >= 9:
                    return True

        for num in range(1, 10):
            if self.__isSafe(row, col, num):

                self.grid[row][col] = num
                if self.__generateGridRec(row, col + 1):
                    return True

                self.grid[row][col] = 0

        return False

    def __generateGrid(self):

        self.__generateSquare(0, 0)
        self.__generateSquare(3, 3)
        self.__generateSquare(6, 6)

        self.__generateGridRec(0, 3)

    def __removeFromGrid(self, diff):
        if diff == 0:
            num = 10

        elif diff == 1:
            num = 20

        elif diff == 2:
            num = 35

        else:
            num = 50

        for i in range(0, num):

            toDelete = randint(0, 80)
            row = toDelete // 9
            col = toDelete % 9

            while self.grid[row][col] == -1:
                toDelete = randint(0, 80)
                row = toDelete // 9
                col = toDelete % 9

            self.grid[row][col] = -1

        # self.printGrid(grid)

    def __init__(self, diff):

        self.diff = diff

        self.grid = []

        for k in range(0, 9):
            self.grid.append([0, 0, 0, 0, 0, 0, 0, 0, 0])

        self.coMat = []

        # coMat is the correlation matrix between the indices of the row and column and the square they're located in.
        # For example, the element on position (4, 1) is located in the square with coordinates (3, 0) (i. e. the 3rd square).

        for k in range(0, 9):
            self.coMat.append([0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        for i in range(0, 9):
            for j in range(0, 9):
                self.coMat[i][j] = (i // 3) * 3 + (j // 3)

        # squareCoord is the array used for obtaining the start coordinates of a square.
        self.squareCoord = [(0, 0), (0, 3), (0, 6), (3, 0), (3, 3), (3, 6), (6, 0), (6, 3), (6, 6)]

    def gameLogic(self):

        self.__generateGrid()

        originalGrid = copy.deepcopy(self.grid)
        # self.printGrid(originalGrid)

        self.__removeFromGrid(self.diff)

        # print("New GRID is: ")
        # self.printGrid(self.grid)

        # print("Original GRID is: ")
        # self.printGrid(originalGrid)

        return self.grid, originalGrid


class Delegate(QtWidgets.QStyledItemDelegate):

    def paint(self, painter, option, index):
        super().paint(painter, option, index)

        if index.row() == 0:    # First row
            painter.setPen(QtGui.QPen(QtGui.Qt.black, 3))
            painter.drawLine(option.rect.topLeft(), option.rect.topRight())

        elif (1 + index.row()) % 3 == 0:  # Every third row
            painter.setPen(QtGui.QPen(QtGui.Qt.black, 3))
            painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        if index.column() == 0: # First column
            painter.setPen(QtGui.QPen(QtGui.Qt.black, 3))
            painter.drawLine(option.rect.topLeft(), option.rect.bottomLeft())

        elif (1 + index.column()) % 3 == 0:  # Every third column
            painter.setPen(QtGui.QPen(QtGui.Qt.black, 3))
            painter.drawLine(option.rect.topRight(), option.rect.bottomRight())


class MyWidget(QtWidgets.QWidget):

    def populateTable(self):

        font = QtGui.QFont()
        font.setPointSize(22)
        font.setBold(True)

        self.tableWidget.setFont(font)

        for i in range(0, 9):
            for j in range(0, 9):
                if self.grid[i][j] != -1:
                    self.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(self.grid[i][j])))

    def __init__(self, diff):
        super().__init__()

        self.diff = diff
        self.game = Game(self.diff)
        self.grid, self.originalGrid = self.game.gameLogic()

        self.selectedCell = (-1, -1)

        self.tableWidget = QtWidgets.QTableWidget()

        self.tableWidget.setGeometry(QtCore.QRect(50, 20, 451, 451))
        self.tableWidget.setMinimumSize(QtCore.QSize(0, 0))
        self.tableWidget.setMaximumSize(QtCore.QSize(450, 450))
        self.tableWidget.setBaseSize(QtCore.QSize(0, 0))
        self.tableWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.tableWidget.setAutoScroll(True)
        self.tableWidget.setRowCount(9)
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setDefaultSectionSize(50)
        self.tableWidget.verticalHeader().setVisible(False)
        self.tableWidget.verticalHeader().setDefaultSectionSize(50)
        self.tableWidget.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectItems)
        self.tableWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        self.tableWidget.setGeometry(QtCore.QRect(20, 20, 451, 451))

        self.gridLayoutWidget = QtWidgets.QWidget()
        self.gridLayoutWidget.setObjectName(u"gridLayoutWidget")
        self.gridLayoutWidget.setGeometry(QtCore.QRect(560, 70, 164, 351))
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setObjectName(u"gridLayout")
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.pushButton2 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton2.setObjectName(u"pushButton2")
        self.pushButton2.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton2.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton2, 0, 1, 1, 1)

        self.pushButton1 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton1.setObjectName(u"pushButton1")
        self.pushButton1.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton1.setMaximumSize(QtCore.QSize(50, 50))

        palette = QtGui.QPalette()
        brush = QtGui.QBrush(QtGui.QColor(0, 120, 215, 255))
        brush.setStyle(QtGui.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Active, QtGui.QPalette.Highlight, brush)
        brush1 = QtGui.QBrush(QtGui.QColor(240, 240, 240, 255))
        brush1.setStyle(QtGui.Qt.SolidPattern)
        palette.setBrush(QtGui.QPalette.Inactive, QtGui.QPalette.Highlight, brush1)
        palette.setBrush(QtGui.QPalette.Disabled, QtGui.QPalette.Highlight, brush)

        self.pushButton1.setPalette(palette)

        self.gridLayout.addWidget(self.pushButton1, 0, 0, 1, 1)

        self.pushButton7 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton7.setObjectName(u"pushButton7")
        self.pushButton7.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton7.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton7, 2, 0, 1, 1)

        self.pushButton5 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton5.setObjectName(u"pushButton5")
        self.pushButton5.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton5.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton5, 1, 1, 1, 1)

        self.pushButton8 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton8.setObjectName(u"pushButton8")
        self.pushButton8.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton8.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton8, 2, 1, 1, 1)

        self.pushButton4 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton4.setObjectName(u"pushButton4")
        self.pushButton4.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton4.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton4, 1, 0, 1, 1)

        self.pushButton3 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton3.setObjectName(u"pushButton3")
        self.pushButton3.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton3.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton3, 0, 2, 1, 1)

        self.pushButton6 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton6.setObjectName(u"pushButton6")
        self.pushButton6.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton6.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton6, 1, 2, 1, 1)

        self.pushButton9 = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButton9.setObjectName(u"pushButton9")
        self.pushButton9.setMinimumSize(QtCore.QSize(50, 50))
        self.pushButton9.setMaximumSize(QtCore.QSize(50, 50))

        self.gridLayout.addWidget(self.pushButton9, 2, 2, 1, 1)

        self.pushButtonSubmit = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonSubmit.setObjectName(u"pushButtonSubmit")
        # self.pushButtonSubmit.setMinimumSize(QtCore.QSize(250, 50))
        # self.pushButtonSubmit.setMaximumSize(QtCore.QSize(250, 50))

        self.gridLayout.addWidget(self.pushButtonSubmit, 3, 0, 1, 3)

        self.pushButtonClear = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.pushButtonClear.setObjectName(u"pushButtonClear")

        self.gridLayout.addWidget(self.pushButtonClear, 4, 0, 1, 3)

        font1 = QtGui.QFont()
        font1.setPointSize(16)
        font1.setBold(True)

        self.pushButton1.setText("1")
        self.pushButton1.setFont(font1)

        self.pushButton2.setText("2")
        self.pushButton2.setFont(font1)

        self.pushButton3.setText("3")
        self.pushButton3.setFont(font1)

        self.pushButton4.setText("4")
        self.pushButton4.setFont(font1)

        self.pushButton5.setText("5")
        self.pushButton5.setFont(font1)

        self.pushButton6.setText("6")
        self.pushButton6.setFont(font1)

        self.pushButton7.setText("7")
        self.pushButton7.setFont(font1)

        self.pushButton8.setText("8")
        self.pushButton8.setFont(font1)

        self.pushButton9.setText("9")
        self.pushButton9.setFont(font1)

        self.pushButtonSubmit.setText("Submit Solution")
        self.pushButtonSubmit.setFont(font1)

        self.pushButtonClear.setText("Clear Cell")
        self.pushButtonClear.setFont(font1)

        self.horizLayout = QtWidgets.QHBoxLayout()
        self.horizLayout.addWidget(self.tableWidget)
        self.horizLayout.addWidget(self.gridLayoutWidget)

        self.populateTable()
        self.connectSignals()
        self.tableWidget.setItemDelegate(Delegate())

        self.setLayout(self.horizLayout)

    def connectSignals(self):

        self.tableWidget.cellClicked.connect(self.getSelectedCell)

        self.pushButton1.clicked.connect(lambda: self.selectNum(1))
        self.pushButton2.clicked.connect(lambda: self.selectNum(2))
        self.pushButton3.clicked.connect(lambda: self.selectNum(3))
        self.pushButton4.clicked.connect(lambda: self.selectNum(4))
        self.pushButton5.clicked.connect(lambda: self.selectNum(5))
        self.pushButton6.clicked.connect(lambda: self.selectNum(6))
        self.pushButton7.clicked.connect(lambda: self.selectNum(7))
        self.pushButton8.clicked.connect(lambda: self.selectNum(8))
        self.pushButton9.clicked.connect(lambda: self.selectNum(9))

        self.pushButtonSubmit.clicked.connect(self.submitSolution)
        self.pushButtonClear.clicked.connect(self.clearCell)

    def getSelectedCell(self):

        row = self.tableWidget.currentRow()
        col = self.tableWidget.currentColumn()

        if self.grid[row][col] == -1:
            self.selectedCell = (row, col)
            # print(self.selectedCell)

        else:
            self.selectedCell = (-1, -1)
            # print(self.selectedCell)

    def selectNum(self, num):

        if self.selectedCell != (-1, -1):
            item = QtWidgets.QTableWidgetItem(str(num))

            # Changing the colour to blue for numbers inserted by the user.
            item.setForeground(QtGui.QBrush(QtGui.QColor("blue")))

            self.tableWidget.setItem(self.selectedCell[0], self.selectedCell[1], item)

    def clearCell(self):

        if self.selectedCell != (-1, -1):
            item = QtWidgets.QTableWidgetItem("")
            self.tableWidget.setItem(self.selectedCell[0], self.selectedCell[1], item)

    @staticmethod
    def messageBox(msgType):
        # msgType = 0: The Puzzle Is Not Finished Yet!
        # msgType = 1: Try Again...
        # msgType = 2: Congratulations! You Win!

        msgBox = QtWidgets.QMessageBox()
        msgBox.setWindowTitle("Status")

        if msgType == 0:
            msgBox.setIcon(QtWidgets.QMessageBox.Warning)
            msgBox.setText("You haven't finished the puzzle yet!")

        elif msgType == 1:
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("Your solution is incorrect. Try again!")

        else:
            msgBox.setIcon(QtWidgets.QMessageBox.Information)
            msgBox.setText("Congratulations! You Win!")

        # msgBox.setFixedSize(500, 300)
        msgBox.exec()

    def submitSolution(self):

        # print("Original grid is: ")
        # self.game.printGrid(self.originalGrid)

        userGrid = []

        for i in range(0, 9):
            row = []
            for j in range(0, 9):

                try:
                    txt = self.tableWidget.item(i, j).text()

                    if txt == "":
                        raise AttributeError

                    num = int(txt)
                    row.append(num)

                except AttributeError:
                    self.messageBox(0)
                    return

            userGrid.append(row)

        # print("User grid is: ")
        # self.game.printGrid(userGrid)

        if userGrid == self.originalGrid:
            self.messageBox(2)

            sys.exit()

        else:
            self.messageBox(1)


class Menu(QtWidgets.QWidget):

    def __init__(self):

        super().__init__()

        self.diff = -1

        self.setFixedSize(300, 400)
        self.layout = QtWidgets.QVBoxLayout()

        font2 = QtGui.QFont()
        font2.setBold(True)
        font2.setPointSize(30)
        self.sudokuLab = QtWidgets.QLabel("SUDOKU")
        self.sudokuLab.setFont(font2)

        self.layout.addWidget(self.sudokuLab)

        font3 = QtGui.QFont()
        font3.setBold(True)
        font3.setPointSize(16)
        self.difficultyLab = QtWidgets.QLabel("Choose Difficulty:")
        self.difficultyLab.setFont(font3)

        self.layout.addWidget(self.difficultyLab)

        self.sudokuLab.setAlignment(QtCore.Qt.AlignCenter)
        self.difficultyLab.setAlignment(QtCore.Qt.AlignCenter)

        self.rb1 = QtWidgets.QRadioButton("Easy")
        self.rb2 = QtWidgets.QRadioButton("Medium")
        self.rb3 = QtWidgets.QRadioButton("Hard")
        self.rb4 = QtWidgets.QRadioButton("Extreme")

        self.rb1.setFont(font3)
        self.rb2.setFont(font3)
        self.rb3.setFont(font3)
        self.rb4.setFont(font3)

        self.layout.addWidget(self.rb1)
        self.layout.addWidget(self.rb2)
        self.layout.addWidget(self.rb3)
        self.layout.addWidget(self.rb4)

        self.pushButtonStart = QtWidgets.QPushButton("Start!")
        self.pushButtonStart.setFont(font3)

        self.layout.addWidget(self.pushButtonStart)

        self.layout.setAlignment(QtCore.Qt.AlignHCenter)
        self.setLayout(self.layout)

        self.connectSignals()

    def setDifficulty(self, difficulty):
        self.diff = difficulty

    def startGame(self):
        if self.diff == -1:

            msgBox = QtWidgets.QMessageBox()
            msgBox.setWindowTitle("Error!")
            msgBox.setIcon(QtWidgets.QMessageBox.Critical)
            msgBox.setText("You must select a difficulty before starting the game!")

            return -1

        else:
            self.hide()

            widget = MyWidget(self.diff)
            widget.resize(800, 600)
            widget.show()

    def connectSignals(self):

        self.rb1.clicked.connect(lambda: self.setDifficulty(0))
        self.rb2.clicked.connect(lambda: self.setDifficulty(1))
        self.rb3.clicked.connect(lambda: self.setDifficulty(2))
        self.rb4.clicked.connect(lambda: self.setDifficulty(3))

        self.pushButtonStart.clicked.connect(self.startGame)


if __name__ == "__main__":
    # QtGui.QFontDatabase.addApplicationFont("/res/hel93.ttf")
    app = QtWidgets.QApplication([])

    menu = Menu()
    menu.show()

    sys.exit(app.exec())

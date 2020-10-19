########## importing modules #########

import sys
import os
try:
    from PyQt5.QtWidgets import *
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
except:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *

########## global variable ##############

font = QFont('Arial',10)

font.setItalic(True)


############ This class capture screenshot ############

class ScreenShot(QWidget):


    def __init__(self):

        super(ScreenShot, self).__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet('''background-color:white; ''')

        self.setWindowOpacity(0.7)
        desktopRect = QDesktopWidget().screenGeometry()
        self.setGeometry(desktopRect)
        self.setCursor(Qt.CrossCursor)

        self.bmask = QBitmap(desktopRect.size())
        self.bmask.fill(Qt.black)

        self.mask = self.bmask.copy()
        self.isDrawing = False

        self.startPoint = QPoint()
        self.endPoint = QPoint()



    def paintEvent(self, event):

        if self.isDrawing:
            self.mask = self.bmask.copy()
            spainter = QPainter(self.mask)
            pen = QPen()
            pen.setStyle(Qt.NoPen)
            spainter.setPen(pen)
            brush = QBrush(Qt.white)
            spainter.setBrush(brush)
            spainter.drawRect(QRect(self.startPoint, self.endPoint))
            self.setMask(QBitmap(self.mask))



    def mousePressEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.startPoint = event.pos()
            self.endPoint = self.startPoint
            self.isDrawing = True



    def mouseMoveEvent(self, event):

        if self.isDrawing:
            self.endPoint = event.pos()
            self.update()


    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            self.endPoint = event.pos()


            main_window_id = QApplication.desktop().winId()
            long_win_id = long(main_window_id)

            screenshot = QPixmap.grabWindow(long_win_id)

            #screenshot = QApplication.primaryScreen().grabWindow(QApplication.desktop().winId())
            rect = QRect(self.startPoint, self.endPoint)
            outputRegion = screenshot.copy(rect)
            outputRegion.save('C:/tmp/shot.jpg', format='JPG', quality=100)
            self.image = QPixmap('C:/tmp/shot.jpg')
            self.close()

            self.window1 = MainWindow()


##########  this is mainwindow  ###########

class MainWindow(QWidget):

    def __init__(self):

        super(MainWindow, self).__init__()

        self.setWindowTitle("Nuke_Annotation")
        self.setWindowIcon(QIcon("Icon.png"))
        self.setGeometry(150,40,200,200)

        self.drawing = False
        self.brushsize = 3
        self.brushColor = Qt.white
        self.lastPoint = QPoint()

        self.UI()
        self.show()

###################   Creating Layouts ###############

    def layout(self):

    ################################# Main Layouts ######################
        self.mainLayout = QVBoxLayout()
        self.topLayout = QVBoxLayout()
        self.middleLayout  = QHBoxLayout()
        self.bottomLayout = QVBoxLayout()

        self.mainLayout.addLayout(self.topLayout)
        self.mainLayout.addLayout(self.middleLayout)
        self.mainLayout.addLayout(self.bottomLayout)
        self.setLayout(self.mainLayout)

#####################  Creating widgets #################

    def widgets(self):

        #################### TopLayout Widgets #########################

        self.imageLabel = QLabel()
        self.image = QPixmap('C:/tmp/shot.jpg')
        self.image = (QPixmap(self.image))
        self.image = (QPixmap(self.image).scaled(1580,1020,Qt.KeepAspectRatio))
        self.setFixedSize(self.image.width(),self.image.height())

        ####################### Middle Layout Widgets #############

        # To capture New screenshot
        self.btnscreenShot = QPushButton(' New ScreenShot  ', self)
        self.btnscreenShot.setFont(font)
        #self.btnscreenShot.setStyleSheet('background-color:orange')
        self.btnscreenShot.clicked.connect(self.newScreenshot)


        # To import images
        self.btnimportImage = QPushButton('Import Image ', self)
        self.btnimportImage.setFont(font)
        self.btnimportImage.setStyleSheet('background-color:Lightseagreen;color:gray')
        self.btnimportImage.clicked.connect(self.importImage)


        # To clear Paint
        self.btnClear = QPushButton('Clear', self)
        self.btnClear.setFont(font)
        #self.btnClear.setStyleSheet('background-color:Lightseagreen;color:gray')
        self.btnClear.clicked.connect(self.clearPaint)


        # brush sizes
        self.combobrushsize = QComboBox(self)
        size = ['BrushSize - 3', 'BrushSize - 5', 'BrushSize - 7', 'BrushSize - 9', 'BrushSize - 11', 'BrushSize - 13',
                'BrushSize - 15']
        self.combobrushsize.addItems(size)
        self.combobrushsize.setFont(font)
        #self.combobrushsize.setStyleSheet('background-color:skyblue')
        self.combobrushsize.currentTextChanged.connect(self.getsizeValue)


        # brush color
        self.combobrushColor = QComboBox(self)
        colors = ['BrushColor - white', 'BrushColor - red', 'BrushColor - blue', 'BrushColor - black',
                  'BrushColor - green', 'BrushColor - yellow']
        self.combobrushColor.addItems(colors)
        self.combobrushColor.setFont(font)
        #self.combobrushColor.setStyleSheet('background-color:skyblue')
        self.combobrushColor.currentTextChanged.connect(self.getcolorValue)
        self.combobrushColor.setFont(font)


        ############################ Save Image #########################

        self.btnsaveImage = QPushButton('Save Image', self)
        self.btnsaveImage.setFont(font)
        #self.btnsaveImage.setStyleSheet('background-color:orange')
        self.btnsaveImage.clicked.connect(self.save)

        ################# Adding Widgest to Layouts ######################

        self.imageLabel.setPixmap(self.image)
        self.topLayout.addWidget(self.imageLabel)

        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.btnimportImage)
        self.middleLayout.addWidget(self.btnscreenShot)
        self.middleLayout.addWidget(self.btnsaveImage)
        self.middleLayout.addStretch()
        self.middleLayout.addWidget(self.btnClear)
        self.middleLayout.addWidget(self.combobrushsize)
        self.middleLayout.addWidget(self.combobrushColor)
        self.middleLayout.addStretch()

        self.middleLayout.setContentsMargins(0, 10, 0, 0)


############## This method used to import the Images ###########

    def importImage(self):

        self.fileopen= QFileDialog.getOpenFileName(self,"Import Image")
        filename = self.fileopen[0]
        filename = os.path.basename(filename)

        if filename != "":
            self.image = QPixmap(filename)
            self.image = (QPixmap(self.image).scaled(1580,1020,Qt.KeepAspectRatio))
            self.resize(self.image.width(),self.image.height())
        else :
            pass


################  This method used to take screenshot ##################

    def newScreenshot(self):

        self.hide()
        QTimer.singleShot(500, self.ScreenShoter)


    def ScreenShoter(self):

        self.screenshot = ScreenShot()


################ this is used to change the brush sizes ################

    def getsizeValue(self):

        self.brushsize = self.combobrushsize.currentText()

        if self.brushsize == 'BrushSize - 3':
            self.brushsize = 3

        elif self.brushsize == 'BrushSize - 5':
            self.brushsize = 5

        elif self.brushsize == 'BrushSize - 7':
            self.brushsize = 7

        elif self.brushsize == 'BrushSize - 9':
            self.brushsize = 9

        elif self.brushsize == 'BrushSize - 11':
            self.brushsize = 11

        elif self.brushsize == 'BrushSize - 13':
            self.brushsize = 13

        elif self.brushsize == 'BrushSize - 15':
            self.brushsize = 15


################ this is used to change the brush color #####################

    def getcolorValue(self):

        self.brushColor = self.combobrushColor.currentText()

        if self.brushColor=='BrushColor - white':
            self.brushColor= Qt.white

        elif self.brushColor =='BrushColor - red':
            self.brushColor= Qt.red

        elif self.brushColor == 'BrushColor - blue':
            self.brushColor = Qt.blue

        elif self.brushColor == 'BrushColor - green':
            self.brushColor = Qt.green

        elif self.brushColor == 'BrushColor - yellow':
            self.brushColor = Qt.yellow

        elif self.brushColor == 'BrushColor - black':
            self.brushColor = Qt.black


    def mousePressEvent(self, event):

        # if left mouse button is pressed
        if event.button() == Qt.LeftButton:
            # make drawing flag true
            self.drawing = True
            # make last point to the point of cursor
            self.lastPoint_x = event.x()
            self.lastPoint_y = event.y()


    def mouseMoveEvent(self, event):

        # checking if left button is pressed and drawing flag is true
        if (event.buttons() & Qt.LeftButton) & self.drawing:
            # creating painter object
            linepainter = QPainter(self.image)

            # set the pen of the painter
            linepainter.setPen(QPen(self.brushColor, self.brushsize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
           # print(self.lastpoint())

            # this will draw only one step
            linepainter.drawLine(self.lastPoint_x-10,self.lastPoint_y+20, event.x()-10, event.y()+20)

            #linepainter.drawLine(self.lastPoint,event.pos())

            # change the last point
            self.lastPoint_x = event.x()
            self.lastPoint_y = event.y()
            
            # update
            self.update()
        



    def mouseReleaseEvent(self, event):

        if event.button() == Qt.LeftButton:
            # make drawing flag false
            self.drawing = False



    def paintEvent(self, event):

        self.imageLabel.setPixmap(self.image)
        self.topLayout.addWidget(self.imageLabel)


########### This medthod used to clear the paint ###############
    def clearPaint(self):

        # make the whole canvas white
        self.image = QPixmap('C:/tmp/shot.jpg')
        self.image = (QPixmap(self.image).scaled(1580, 1020, Qt.KeepAspectRatio))

        # update
        self.update()


############## This method used to saves the painted files ################
    def save(self):

        filePath, _ = QFileDialog.getSaveFileName(self, "Save Image", "","PNG(*.png);;JPEG(*.jpg *.jpeg);;All Files(*.*) ")

        if filePath == "":
            return
        self.image.save(filePath)


############## adding ui to main layout ###############
    def UI(self):

        self.layout()
        self.widgets()


############# Calling the main window #############

def start():

    start.SCREEN = ScreenShot()
    start.SCREEN.show()
    

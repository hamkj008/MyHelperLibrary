from icecream import ic
import os
import sys
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QSizePolicy, QMenuBar
from PySide6.QtCore import Qt, QPoint, QTimer
from PySide6.QtGui import QIcon, QCursor
from MyHelperLibrary.Helpers.HelperMethods import createLayoutFrame, createWidget


# =============================================================================================



class CustomWindow(QMainWindow):

    def __init__(self, windowName, windowIcon, addMenubar=False):
        super().__init__()

        self.windowName = windowName
        self.windowIcon = windowIcon

        self.setWindowFlags(Qt.FramelessWindowHint)
        self.menubarHeight = 25

        # Set the path for all files so that the directory is consistent no matter where the library is being run from
        if getattr(sys, "frozen", False):  # If running as an executable
            self.libraryDirectory = sys._MEIPASS  # PyInstaller temp directory
        else:
            self.libraryDirectory = os.path.dirname(os.path.abspath(__file__))  # Normal script path


        self.windowIconSize     = QPoint(25, 25)
        self.btnIconSize        = QPoint(25, 25)

        # Custom title bar
        self.createTitleBar(windowName, windowIcon)

        # Primary container 
        self.containerWidget = QWidget(objectName="containerWidget")
        containerLayout = QVBoxLayout(self.containerWidget)
        containerLayout.setContentsMargins(0, 0, 0, 0)  # Remove any margins
        containerLayout.setSpacing(0) 
        containerLayout.addWidget(self.titleBar)

        if addMenubar: 
            self.menubar = QMenuBar(self, objectName="menuBar")
            self.menubar.setFixedHeight(self.menubarHeight)
            self.menubar.setGeometry(0, self.titleBar.height(), self.width(), 25)
            self.menubar.setStyleSheet("""QMenuBar {
                                                border: none;  /* Remove any default borders */
                                                margin: 0px;   /* Remove any margins */
                                                padding: 0px;  /* Remove any padding */
                                            } """)
            containerLayout.addWidget(self.menubar)

        # Set the title bar as the menu widget
        self.setMenuWidget(self.containerWidget)

    
        # Variables for window dragging
        self.dragging           = False
        self.dragPosition       = QPoint()

        self.resizing           = False
        self.resizeDirection    = None
        self.resizeMargin       = 10  # Threshold for detecting edges

        # Timer to continuously check the mouse position and update cursor
        self.mouseTrackingTimer = QTimer(self)
        self.mouseTrackingTimer.timeout.connect(self.trackMousePosition)
        self.mouseTrackingTimer.start(300)  # Every 30 ms


    # =============================================================================================


    def createTitleBar(self, windowName, windowIcon):

        self.titleBar   = QWidget(self, objectName="titleBar")
        titleLayout     = QHBoxLayout(self.titleBar)
        titleLayout.setContentsMargins(10,0,0,0)
        self.titleBar.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.iconLabel = QLabel(objectName="windowIcon")
        self.iconLabel.setPixmap(QIcon(windowIcon).pixmap(self.windowIconSize.x() , self.windowIconSize.y()))

        self.titleLabel = createWidget("label", text=windowName, objectName="titleLabel", sizePolicy=("expanding", "fixed"))

        self.minBtn     = QPushButton(QIcon(os.path.join(self.libraryDirectory, "icons", "minimize.png")), "", objectName="titleBarButton")
        self.maxBtn     = QPushButton(QIcon(os.path.join(self.libraryDirectory, "icons", "maximize.png")), "", objectName="titleBarButton")
        self.closeBtn   = QPushButton(QIcon(os.path.join(self.libraryDirectory, "icons", "close_window.png")), "", objectName="titleBarButton")

        self.minBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())
        self.maxBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())
        self.closeBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())

        buttonFrame = createLayoutFrame(objectName="buttonFrame", sizePolicy=("fixed", "fixed"), spacing=5)
        buttonFrame.setContentsMargins(0,0,0,0)
        buttonFrame.layout().addWidget(self.minBtn)
        buttonFrame.layout().addWidget(self.maxBtn)
        buttonFrame.layout().addWidget(self.closeBtn)

        titleLayout.addWidget(self.iconLabel)
        titleLayout.addWidget(self.titleLabel)
        titleLayout.addWidget(buttonFrame)

        # Connect buttons to functions
        self.minBtn.clicked.connect(self.minimizeWindow)
        self.maxBtn.clicked.connect(self.toggleMaximize)
        self.closeBtn.clicked.connect(self.close_window)


    # =============================================================================================


    def main(self):
        self.show()

        
    # =============================================================================================


    def setWindowIconSize(self, newIconSize):

        self.windowIconSize = newIconSize
        self.iconLabel.setPixmap(QIcon(self.windowIcon).pixmap(self.windowIconSize.x() , self.windowIconSize.y()))


    # =============================================================================================


    def setButtonIconSize(self, newButtonSize):
        ic("changeIconSize")

        self.btnIconSize = newButtonSize

        self.minBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())
        self.maxBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())
        self.closeBtn.setFixedSize(self.btnIconSize.x(), self.btnIconSize.y())
 

    # =============================================================================================


    def minimizeWindow(self):
        self.showMinimized()


    # =============================================================================================

    """ Make sure the title bar expands to fit the width of any screen resizing event """
    def resizeEvent(self, event):

        if hasattr(self, "titleBar"):
            self.titleBar.setFixedWidth(self.width())

        return super().resizeEvent(event)


    # =============================================================================================


    def toggleMaximize(self):

        if self.isMaximized():
            self.showNormal()
            self.maxBtn.setIcon(QIcon(os.path.join(self.libraryDirectory, "icons", "maximize.png")))

        else:
            self.showMaximized()
            self.maxBtn.setIcon(QIcon(os.path.join(self.libraryDirectory, "icons", "restore_down.png")))


    # =============================================================================================


    def close_window(self):
        self.close()


    # =============================================================================================


    def trackMousePosition(self):
        pos = QCursor.pos()

        for key, value in self.checkMouseOnWindowBorder(pos).items():
            if value:
                self.setCursor(self.changeCursor(key))
                break

        else:
            self.setCursor(Qt.ArrowCursor)


    # =============================================================================================


    def mousePressEvent(self, event):

        pos = QCursor.pos()

        if event.button() == Qt.LeftButton:
            # Detect if mouse is near the edges for resizing
            for key, value in self.checkMouseOnWindowBorder(pos).items():
                if value:
                    # Lock in the cursor and window values before resizing
                    self.resizing           = True
                    self.resizeDirection    = key
                    self.initialPosition    = event.globalPos()
                    self.initialWidth       = self.width()
                    self.initialHeight      = self.height()
                    break
            
            else:
                self.dragging = True
                self.dragPosition = event.globalPos() - self.frameGeometry().topLeft()

    # =============================================================================================


    def mouseMoveEvent(self, event):

        if self.resizing:
            # Resize the window based on the direction
            self.resizeWindow()

        elif self.dragging:
            # Drag the window
            self.move(event.globalPos() - self.dragPosition)


    # =============================================================================================


    def mouseReleaseEvent(self, event):

        self.dragging = False
        self.resizing = False
        self.setCursor(Qt.ArrowCursor)

    
    # =============================================================================================


    """Check if the mouse is near any edge or corner of the window."""
    
    def checkMouseOnWindowBorder(self, pos):

        leftEdge    = pos.x() <= self.pos().x() + self.resizeMargin and pos.x() >= self.pos().x() - self.resizeMargin
        rightEdge   = pos.x() <= self.pos().x() + self.rect().width() + self.resizeMargin and pos.x() >= self.pos().x() + self.rect().width() - self.resizeMargin
        topEdge     = pos.y() >= self.pos().y() - self.resizeMargin and pos.y() <= self.pos().y() + self.resizeMargin
        bottomEdge  = pos.y() <= self.pos().y() + self.rect().height() + self.resizeMargin and pos.y() >= self.pos().y() + self.rect().height() - self.resizeMargin


        topLeft, bottomLeft, topRight, bottomRight = "", "", "", ""

        if leftEdge and topEdge:
            topLeft, leftEdge, topEdge = True, False, False

        elif leftEdge and bottomEdge:
            bottomLeft, leftEdge, bottomEdge = True, False, False

        elif rightEdge and topEdge:
            topRight, rightEdge, topEdge = True, False, False

        elif rightEdge and bottomEdge:
            bottomRight, rightEdge, bottomEdge = True, False, False

        direction = {"left": leftEdge, "topLeft": topLeft, "bottomLeft": bottomLeft , 
                     "right": rightEdge, "topRight": topRight, "bottomRight": bottomRight, 
                     "top": topEdge, "bottom": bottomEdge }
 
        return direction


    # =============================================================================================


    """Returns the appropriate cursor for the resize direction."""
    def changeCursor(self, direction):

        if direction == 'left' or direction == 'right':
            return Qt.SizeHorCursor

        elif direction == 'top' or direction == 'bottom':
            return Qt.SizeVerCursor

        elif direction == 'topLeft' or direction == 'bottomRight':
            return Qt.SizeFDiagCursor

        elif direction == 'topRight' or direction == 'bottomLeft':
            return Qt.SizeBDiagCursor

        return Qt.ArrowCursor


    # =============================================================================================


    """Resize the window based on mouse movement."""
    def resizeWindow(self):

        pos = QCursor.pos()

        difference = pos - self.initialPosition

        
        if self.resizeDirection == 'left':
            self.setGeometry(pos.x(), self.y(), self.initialWidth - difference.x(), self.height())

        elif self.resizeDirection == 'right':
            self.setGeometry(self.x(), self.y(), self.initialWidth + difference.x(), self.height())

        elif self.resizeDirection == 'top':
            self.setGeometry(self.x(), pos.y(), self.width(), self.initialHeight - difference.y())

        elif self.resizeDirection == 'bottom':
            self.setGeometry(self.x(), self.initialPosition.y() - self.initialHeight, self.width(), self.initialHeight + difference.y())

        elif self.resizeDirection == 'topLeft':
            ic(self.initialWidth - difference.x())
            self.setGeometry(pos.x(), pos.y(), self.initialWidth - difference.x(), self.initialHeight - difference.y())

        elif self.resizeDirection == 'topRight':
            self.setGeometry(self.x(), pos.y(), self.initialWidth + difference.x(), self.initialHeight - difference.y())

        elif self.resizeDirection == 'bottomLeft':
            self.setGeometry(pos.x(), self.initialPosition.y() - self.initialHeight, self.initialWidth - difference.x(), self.initialHeight + difference.y())

        elif self.resizeDirection == 'bottomRight':
            self.setGeometry(self.x(), self.initialPosition.y() - self.initialHeight, self.initialWidth + difference.x(), self.initialHeight + difference.y())


    # =============================================================================================

    def handleChildResizeLimit(self, direction):
        ic("handleChildResizeLimit")

        # Stop the current resize operation
        self.resizing = False
    
        # Reset cursor
        self.setCursor(Qt.ArrowCursor)
    
        # If resizing vertically and hit a limit
        if direction == "vertical" and self.resizeDirection in ["top", "bottom", "topLeft", "topRight", "bottomLeft", "bottomRight"]:
            self.setGeometry(self.x(), self.y(), self.width(), self.height() + 10) # adds a little bounce back so it doesn't get stuck in the minimum
    
        # If resizing horizontally and hit a limit
        elif direction == "horizontal" and self.resizeDirection in ["left", "right", "topLeft", "topRight", "bottomLeft", "bottomRight"]:
            self.setGeometry(self.x(), self.y(), self.width() + 10, self.height()) # adds a little bounce back so it doesn't get stuck in the minimum

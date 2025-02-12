from enum import Enum, auto

from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt, QEvent, QTimer
from PySide6.QtGui import QCursor

# =============================================================================================


class Direction(Enum):

    HORIZONTAL      = auto()
    VERTICAL        = auto()
    
# =============================================================================================


""" A grid that contains resizable frames. 
    Can be either horizontal frames, where the resize divider goes left/right, 
    or vertical frames, where the divider goes top/ bottom """

class ResizeableGrid(QWidget):
    def __init__(self, dividers, direction = Direction.HORIZONTAL, minWidth = 0, minHeight = 0):
        super().__init__()
        
        # Create a grid layout
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        self.grid.setVerticalSpacing(0)
        self.setLayout(self.grid)

        self.direction          = direction
        self.dividers           = dividers              # a list of tuples containing the frame pairs that have the divider
        self.isOverDivider      = False
        self.resizing           = False
        self.resizingFrames     = (None, None)          # the actual frames involved in the split

        self.minWidth           = minWidth              # the smallest a column should go
        self.minHeight          = minHeight             # the smallest a row should go
        self.startX             = 0
        self.startWidth         = 0
        self.startHeight        = 0
        self.startHeight        = 0
        self.currentWidth       = 0
        self.currentHeight      = 0

        # Timer to continuously check the mouse position and update cursor
        self.mouseTrackingTimer = QTimer(self)
        self.mouseTrackingTimer.timeout.connect(self.trackMousePosition)
        self.mouseTrackingTimer.start(300)  # Every 30 ms

        self.installEventFilter(self)


    # ========================================================================================   


    def trackMousePosition(self):
        pos             = QCursor.pos()
        foundDivider    = False

        for frame1, frame2 in self.dividers:

            # convert local coordinates to global coordinates
            frame1Rect = frame1.mapToGlobal(frame1.rect().topLeft())        
            frame2Rect = frame2.mapToGlobal(frame2.rect().topLeft())

            if self.direction == Direction.HORIZONTAL:

                # frameRect.x() gives the leftedge, so to get the right edge add the width
                # the cursor is greater than right edge of frame 1 and less than the left edge of frame 2 
                if frame1Rect.x() + frame1.geometry().width() <= pos.x() <= frame2Rect.x():          

                    self.setCursor(Qt.SplitHCursor)
                    self.isOverDivider  = True
                    self.resizingFrames = (frame1, frame2)          # load the frames involved in the split
                    foundDivider        = True
                    break


            elif self.direction == Direction.VERTICAL:
                if frame1Rect.y() + frame1.geometry().height() <= pos.y() <= frame2Rect.y():

                    self.setCursor(Qt.SplitVCursor)
                    self.isOverDivider  = True
                    self.resizingFrames = (frame1, frame2)          # load the frames involved in the split
                    foundDivider        = True
                    break


        if not foundDivider:
            self.setCursor(Qt.ArrowCursor) 
            self.isOverDivider = False


    # ========================================================================================   


    def eventFilter(self, obj, event):

        if event.type() == QEvent.MouseButtonPress:
            
            self.MousePressHandler(event)
            return True 

        return super().eventFilter(obj, event)
    
            
    # ========================================================================================   


    def MousePressHandler(self, event):

        if self.isOverDivider:

            self.resizing = True

            if self.direction == Direction.HORIZONTAL:
                self.startX         = event.globalX()
                self.startWidth     = self.resizingFrames[0].width()


            elif self.direction == Direction.VERTICAL:
                self.startY         = event.globalY()
                self.startHeight    = self.resizingFrames[0].height()
                self.currentHeight = self.startHeight
            
    # ========================================================================================   


    def mouseMoveEvent(self, event):

        if self.resizing:
            if self.direction == Direction.HORIZONTAL:
                
                delta                   = event.globalX() - self.startX

                newWidth                = self.startWidth + delta    # Get distance mouse has moved from start position        
            
                firstColNumber          = self.getColumnNumber(self.resizingFrames[0])
                secondColNumber         = self.getColumnNumber(self.resizingFrames[1])
                 
                # Retrieve the widgets in the column
                activeColWidgets        = self.getColumnWidgets(firstColNumber)
                adjacentColWidgets      = self.getColumnWidgets(secondColNumber)

                adjacentCurrentWidth    = adjacentColWidgets[0].width()     # all widgets have the same width so can get the first
                adjacentMinimumWidth    = self.getRowMinimumWidth(adjacentColWidgets)

                if self.minWidth == 0:
                    # if no min has been set then the min is set by the internal minimum width of the widgets.
                    # this applies to the active frame as well as the adjacent
                    self.minWidth = adjacentMinimumWidth    

                # Conditions for resizing. 
                # 1. the active frame can shrink if the mouse movement is negative than the current width
                # 2. the widgets in the adjacent frame have not reached their internal minimum width
                # 3. the adjacent frame has not reached the user defined minimum
                canResize = ((newWidth < self.currentWidth and newWidth > self.minWidth) or
                             adjacentCurrentWidth > adjacentMinimumWidth or
                             (self.minWidth > adjacentMinimumWidth and adjacentCurrentWidth > self.minWidth)) 

                if canResize:
                    for widget in activeColWidgets:
                        self.currentWidth = max(self.minWidth, newWidth)    # Enforce minimum width and update tracking
                        widget.setFixedWidth(self.currentWidth)             # Apply new width            

            # --------------------------------------------------------------------------------------------------------

            elif self.direction == Direction.VERTICAL:

                delta                   = event.globalY() - self.startY

                newHeight               = self.startHeight + delta    # Get distance mouse has moved from start position     
            
                firstRowNumber          = self.getRowNumber(self.resizingFrames[0])
                secondRowNumber         = self.getRowNumber(self.resizingFrames[1])
                 
                # Retrieve the widgets in the row
                activeRowWidgets        = self.getRowWidgets(firstRowNumber)
                adjacentRowWidgets      = self.getRowWidgets(secondRowNumber)

                adjacentCurrentHeight   = adjacentRowWidgets[0].height()     # all widgets have the same height so can get the first
                adjacentMinimumHeight   = self.getRowMinimumHeight(adjacentRowWidgets)

                if self.minHeight == 0:
                    self.minHeight = adjacentMinimumHeight

                # Conditions for resizing. 
                # 1. the active frame can shrink if the mouse movement is negative than the current height
                # 2. the widgets in the adjacent frame have not reached their internal minimum height
                # 3. the adjacent frame has not reached the user defined minimum
                canResize = ((newHeight < self.currentHeight and newHeight > self.minHeight) or
                             adjacentCurrentHeight > adjacentMinimumHeight or
                             (self.minHeight > adjacentMinimumHeight and adjacentCurrentHeight > self.minHeight))    

                if canResize:
                    for widget in activeRowWidgets:
                        self.currentHeight = max(self.minHeight, newHeight)     # Enforce minimum height and update tracking
                        widget.setFixedHeight(self.currentHeight)               # Apply new height


    # ========================================================================================   
    
        """Get the actual minimum height a widget can shrink to"""
    def getRealMinimumWidth(self, widget):
        return max(
            widget.minimumWidth(),              # Explicit minimum
            widget.minimumSizeHint().width(),   # Size hint minimum
            widget.layout().minimumSize().width() if widget.layout() else 0  # Layout minimum
        )

    # ========================================================================================   
    
    """Get the largest minimum height from any widget in the row"""
    def getRowMinimumWidth(self, rowWidgets):
        return max(self.getRealMinimumWidth(widget) for widget in rowWidgets)
    

    # ========================================================================================   

    """Get the actual minimum height a widget can shrink to"""
    def getRealMinimumHeight(self, widget):
        return max(
            widget.minimumHeight(),              # Explicit minimum
            widget.minimumSizeHint().height(),   # Size hint minimum
            widget.layout().minimumSize().height() if widget.layout() else 0  # Layout minimum
        )

    # ========================================================================================   
    
    """Get the largest minimum height from any widget in the row"""
    def getRowMinimumHeight(self, rowWidgets):
        return max(self.getRealMinimumHeight(widget) for widget in rowWidgets)
    

    # ========================================================================================   
    

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.resizing       = False
            self.resizingFrames = (None, None)


    # ========================================================================================   
    

    # Find the column number of the frame that is being moved to move all frames in the column at once
    def getColumnNumber(self, checkWidget):
            for colNum in range(self.grid.columnCount()):
                for row in range(self.grid.rowCount()):
                    item = self.grid.itemAtPosition(row, colNum)
                    if item:
                        widget = item.widget()
                        if widget:
                            if widget == checkWidget:
                                return colNum


    # ========================================================================================   
     

    # Find the row number of the frame that is being moved to move all frames in the row at once
    def getRowNumber(self, checkWidget):
            for rowNum in range(self.grid.rowCount()):
                for col in range(self.grid.columnCount()):
                    item = self.grid.itemAtPosition(rowNum, col)
                    if item:
                        widget = item.widget()
                        if widget:
                            if widget == checkWidget:
                                return rowNum

    # ========================================================================================   
     

    def getColumnWidgets(self, colNum):
        
        widgets = []
        for row in range(self.grid.rowCount()):
            item = self.grid.itemAtPosition(row, colNum)
            if item:
                widget = item.widget()
                if widget:
                    widgets.append(widget)
        return widgets
    

    # ========================================================================================   
           
    def getRowWidgets(self, rowNum):
        
        widgets = []
        for col in range(self.grid.columnCount()):
            item = self.grid.itemAtPosition(rowNum, col)
            if item:
                widget = item.widget()
                if widget:
                    widgets.append(widget)
        return widgets
    

    # ========================================================================================  

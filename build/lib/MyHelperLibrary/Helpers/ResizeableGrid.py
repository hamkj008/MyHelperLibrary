from enum import Enum, auto
from icecream import ic

from PySide6.QtWidgets import QWidget, QGridLayout
from PySide6.QtCore import Qt, QEvent, QTimer, Signal
from PySide6.QtGui import QCursor


# =============================================================================================


class Direction(Enum):

    HORIZONTAL      = auto()
    VERTICAL        = auto()
    
# =============================================================================================


""" A grid that contains resizable frames. 
    Can be either horizontal frames, where the resize divider goes left/right, 
    or vertical frames, where the divider goes top/ bottom.
    Also includes equal distribution resizing when modifying window size in order to keep sizing consistent and not break layouts.
    If the parent that owns the custom window is provided, a signal can be sent to prevent resizing past minimums"""

class ResizeableGrid(QWidget):

    # Define a signal to communicate resize constraints
    stopResizeSignal = Signal(str)  # Signal will carry the direction ("vertical" or "horizontal")

    def __init__(self, dividers, direction = Direction.HORIZONTAL, minWidth = 75, minHeight = 75, customWindowParent=None):
        super().__init__()
        
        # Create a grid layout
        self.grid = QGridLayout(self)
        self.grid.setContentsMargins(0,0,0,0)
        # self.grid.setHorizontalSpacing(0)
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


        # Timer to continuously check the mouse position and update cursor
        self.mouseTrackingTimer = QTimer(self)
        self.mouseTrackingTimer.timeout.connect(self.trackMousePosition)
        self.mouseTrackingTimer.start(300)  # Every 30 ms

        # Connect stop resizing signal to CustomWindow
        if customWindowParent:
            self.stopResizeSignal.connect(customWindowParent.handleChildResizeLimit)


        for i in range(self.grid.columnCount()):
            widgets = self.getColumnWidgets(i)           
            if widgets:
                for widget in widgets:
                    widget.setFixedWidth(self.minWidth)

        self.installEventFilter(self)


    # ========================================================================================    


    def trackMousePosition(self):
        pos             = QCursor.pos()
        foundDivider    = False

        if self.resizing:
            return

        # Loop through every tuple in the divider list
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
        ic("mouse press")

        if self.isOverDivider:

            self.resizing = True

            if self.direction == Direction.HORIZONTAL:
                self.startX             = event.globalX()
                self.startWidth         = self.resizingFrames[0].width()

                firstColNumber          = self.getColumnNumber(self.resizingFrames[0])
                secondColNumber         = self.getColumnNumber(self.resizingFrames[1])
                 
                # Retrieve the widgets in the column
                self.activeColWidgets   = self.getColumnWidgets(firstColNumber)
                self.adjacentColWidgets = self.getColumnWidgets(secondColNumber)

                self.combinedWidth      = self.resizingFrames[0].width() + self.resizingFrames[1].width()


            elif self.direction == Direction.VERTICAL:
                self.startY             = event.globalY()
                self.startHeight        = self.resizingFrames[0].height()

                firstRowNumber          = self.getRowNumber(self.resizingFrames[0])
                secondRowNumber         = self.getRowNumber(self.resizingFrames[1])
                 
                # Retrieve the widgets in the row
                self.activeRowWidgets   = self.getRowWidgets(firstRowNumber)
                self.adjacentRowWidgets = self.getRowWidgets(secondRowNumber)

                self.combinedHeight     = self.resizingFrames[0].height() + self.resizingFrames[1].height()
            

    # ========================================================================================   


    def mouseMoveEvent(self, event):
        ic("mouse move")
        if self.resizing:

            if self.direction == Direction.HORIZONTAL:
                
                delta = event.globalX() - self.startX

                newWidth         = max(self.minWidth, self.startWidth + delta)    # Get distance mouse has moved from start position                  
                newAdjacentWidth = max(self.minWidth, self.combinedWidth - newWidth)

                if newWidth > self.minWidth and (newAdjacentWidth > self.minWidth or newWidth < self.startWidth):

                    for widget in self.activeColWidgets:
                        widget.setFixedWidth(newWidth)

                    for widget in self.adjacentColWidgets:
                        widget.setFixedWidth(newAdjacentWidth)


            # --------------------------------------------------------------------------------------------------------

            elif self.direction == Direction.VERTICAL:

                delta                   = event.globalY() - self.startY

                newHeight               = max(self.minHeight, self.startHeight + delta) 
                newAdjacentHeight       = max(self.minHeight, self.combinedHeight - newHeight) 

                if newHeight > self.minHeight and (newAdjacentHeight > self.minHeight or newHeight < self.startHeight):

                    for widget in self.activeRowWidgets:
                        widget.setFixedHeight(newHeight)

                    for widget in self.adjacentRowWidgets:
                        widget.setFixedHeight(newAdjacentHeight)


    # ========================================================================================   


    def mouseReleaseEvent(self, event):
        ic("mouse release")
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

    def resizeEvent(self, event):

        super().resizeEvent(event)
    
        if self.direction   == Direction.HORIZONTAL:
            self.adjustColumnsOnWindowResize()

        elif self.direction == Direction.VERTICAL:
            self.adjustRowsOnWindowResize()


    # ========================================================================================  


    def adjustColumnsOnWindowResize(self):

        totalWidth      = self.width()
        spacing         = self.grid.layout().horizontalSpacing()
        totalSpacing    = spacing * (self.grid.columnCount() - 1)
        columnSpace     = totalWidth - totalSpacing
        minTotalWidth   = (self.grid.columnCount() * self.minWidth) + totalSpacing
    
        # If being resized too small, emit signal to stop
        if totalWidth <= minTotalWidth:
            self.stopResizeSignal.emit("horizontal")
            return
    
        # Get current column widths and calculate current total
        currentWidths   = []
        currentTotal    = 0
    
        for i in range(self.grid.columnCount()):
            widgets = self.getColumnWidgets(i)
            if widgets:
                width = widgets[0].width()
                currentWidths.append((i, width))
                currentTotal += width
    
        # Calculate and apply new widths based on proportions
        for i, currentWidth in currentWidths:

            # What percentage of the total does this column currently occupy?
            proportion = currentWidth / currentTotal
        
            # Apply that same percentage to the new total width
            newWidth = max(self.minWidth, columnSpace * proportion)
        
            # Apply to all widgets in this column
            widgets = self.getColumnWidgets(i)
            for widget in widgets:
                widget.setFixedWidth(newWidth)


    # ========================================================================================  


    def adjustRowsOnWindowResize(self):

        totalHeight     = self.height()
        spacing         = self.grid.layout().verticalSpacing()
        totalSpacing    = spacing * (self.grid.rowCount() - 1) if self.grid.verticalSpacing() is not None else 0
        rowSpace        = totalHeight - totalSpacing
        minTotalHeight  = (self.grid.rowCount() * self.minHeight) + totalSpacing
    
        # If being resized too small, emit signal to stop
        if totalHeight <= minTotalHeight:
            self.stopResizeSignal.emit("vertical")
            return
    
        # Get current row heights and calculate current total
        currentHeights  = []
        currentTotal    = 0
    
        for i in range(self.grid.rowCount()):
            widgets = self.getRowWidgets(i)
            if widgets:
                height = widgets[0].height()
                currentHeights.append((i, height))
                currentTotal += height
    
        # Calculate and apply new widths based on proportions
        for i, currentHeight in currentHeights:

            # What percentage of the total does this column currently occupy?
            proportion = currentHeight / currentTotal
        
            # Apply that same percentage to the new total width
            newHeight = max(self.minHeight, rowSpace * proportion)
        
            # Apply to all widgets in this column
            widgets = self.getRowWidgets(i)
            for widget in widgets:
                widget.setFixedHeight(newHeight)
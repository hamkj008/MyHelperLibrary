from icecream import ic
from PySide6.QtWidgets import QMainWindow, QLabel, QWidget, QSizePolicy

from UiViews.UiLogControllerWindow import Ui_LogControllerWindow
from LogView import LogView



class LogController(QMainWindow):
    
    def __init__(self):
        super().__init__()

        self.window = Ui_LogControllerWindow()
        self.window.setupUi(self)
        self.setWindowTitle("Log")
        

        self.displayLogView()
        self.setGeometry(4100, 50, 1200, 700)
        
        self.logData = []
        
        self.red    = 0
        self.blue   = 0
        self.green  = 0
        
        self.row    = 0
        self.column = 0
        

    # ========================================================================================
        

    def main(self):        
        self.show()


    # ========================================================================================
    
    
    def displayLogView(self):
        ic("displayLogView")
        
        self.logView = LogView(self)
        self.window.stackedWidget.addWidget(self.logView)
        self.window.stackedWidget.setCurrentWidget(self.logView)
     
        
    # ========================================================================================
    
    
    def log(self, description, data):
        self.logRow = []
        
        self.logRow.append(f"Label: {description}")
        
        if isinstance(data, list):
            self.logRow.append(f"Total data length: {str(len(data))}")
            
            for d in data:
                self.checkTypes(d)
                    
                if isinstance(d, list):
                    self.logRow.append(f"Array found")
                    self.logRow.append(f"Array length: {str(len(d))}")
                    
                    for member in d:
                        self.checkTypes(member)
        else:
            self.checkTypes(data)
           
        self.logData.append(self.logRow)
        self.display(self.logRow)



    # ========================================================================================
    

    def checkTypes(self, dataPoint):
        
        self.logRow.append(f"Type: {type(dataPoint)}")
                        
        if isinstance(dataPoint, QWidget):
            self.logRow.append(f"Object Name: {dataPoint.objectName()}")

        elif isinstance(dataPoint, int):
            self.logRow.append(str(dataPoint))
                            
        elif isinstance(dataPoint, str):
            self.logRow.append(dataPoint)



    # ========================================================================================


    def display(self, logRow):
        self.column = 0
        
        for l in logRow:
            ic(l)
            label = QLabel(str(l))
            label.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
            self.logView.window.TextGridFrame.layout().addWidget(label, self.row, self.column)
            label.setStyleSheet(f"color: rgb({self.red + 1}, 255, {self.green + 1})")
            self.column +=1
            
        self.row += 1

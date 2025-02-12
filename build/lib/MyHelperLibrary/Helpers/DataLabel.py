from icecream import ic

from PySide6.QtWidgets import QLabel


class DataLabel(QLabel):
    def __init__(self, text, data, objectName=None):
        super().__init__(text)    
        
        self.data = data
        if objectName:
            self.setObjectName(objectName)

from icecream import ic

from PySide6.QtWidgets import QLabel
from MyHelperLibrary.Helpers.HelperMethods import getSizePolicyMap



class DataLabel(QLabel):
    def __init__(self, text, data, objectName=None, sizePolicy: tuple[str, str]=None):
        super().__init__(text=text, objectName=objectName)    
        
        self.data = data

        if sizePolicy:
            self.setSizePolicy(getSizePolicyMap(sizePolicy))
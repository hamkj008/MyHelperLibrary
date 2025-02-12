from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QSizePolicy, QVBoxLayout, QFrame, QDialog, QMessageBox, QDialogButtonBox
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap
import os
from icecream import ic

# ========================================================================================


def loadImage(fileName, width, height):
        
    imageFolder = 'Images' 
    imagePath = os.path.join(imageFolder, fileName)

    # Create QPixmap with resized image
    pixmap = QPixmap(imagePath)
    if pixmap:
        pixmap = pixmap.scaled(width, height, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        
    return pixmap


# ========================================================================================


def createDictionary(rows, cursorDescription):
        
    # -- Create dictionary --
    columnNames = [description[0] for description in cursorDescription]

    resultsDictList = []

    # Zip the column names and results together into a dictionary list
    for row in rows:
        if row is None:
            continue
        
        rowDict = {}
        for columnName, value in zip(columnNames, row):
            rowDict[columnName] = value
        resultsDictList.append(rowDict)

    return resultsDictList
     

# ========================================================================================


# Create a dictionary for a single record
def createSingleRecordDictionary(category, cursorDescription):
    
    columnNames = [description[0] for description in cursorDescription]
       
    rowDict = {}

    if category is not None:
        for columnName, value in zip(columnNames, category):
            rowDict[columnName] = value

        return rowDict


# ========================================================================================


def createWidget(widgetType, text=None, objectName=None, toolTip=None, sizePolicy: tuple[str, str]=None, align=None):
    
    item = None
    if widgetType == "label":
        item = QLabel(text, objectName=objectName)
        
    elif widgetType == "button":
        item = QPushButton(text, objectName=objectName)
        
    elif widgetType == "date":
        item = QDateEdit()
        item.setCalendarPopup(True)
        item.setDisplayFormat("dd-MMM-yyyy")
        currentDate = QDate.currentDate()
        item.setDate(currentDate)
        
    elif widgetType == "lineEdit":
        item = QLineEdit()
     
    if toolTip:
        item.setToolTip(toolTip)

    if sizePolicy:
        item.setSizePolicy(getSizePolicyMap(sizePolicy))
        
    if align:
        if align == "left":
            item.setAlignment(Qt.AlignLeft)
        
        elif align == "right":
            item.setAlignment(Qt.AlignRight)
        
        elif align == "center":
            item.setAlignment(Qt.AlignCenter)
        
    return item


# ========================================================================================
    
    
def clearLayout(layout):
    
    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()      
                

# ========================================================================================

# Customizable dialog box
def createDialog(title, message, width, height):
    
    dialog = QDialog(objectName="dialog")
    dialog.setWindowTitle(title)
    dialog.setMinimumSize(width, height)
    
    # ------ Set Style ------
    dialog.setStyleSheet(getDialogStyle())
    # -------------------------------

    # Create a layout and add widgets
    layout = QVBoxLayout()

    # Add a label
    messageLabel = createWidget("label", text=message, align="center")
    layout.addWidget(messageLabel)

    # Add an OK button
    okBtn = createWidget("button", text="Ok", sizePolicy=("fixed", "fixed"))
    okBtn.clicked.connect(dialog.accept)  # Close the dialog when the button is clicked
    
    frame = QFrame()
    frameLayout = QVBoxLayout()
    frameLayout.addWidget(okBtn)
    frameLayout.setAlignment(Qt.AlignCenter)
    frame.setLayout(frameLayout)
    
    
    layout.addWidget(frame)
    
    # Set the layout for the dialog
    dialog.setLayout(layout)

    # Show the dialog
    dialog.exec()      
    

# ========================================================================================


def createChoiceDialog(windowTitle, message):
    
    messageBox = QMessageBox()
    messageBox.setMinimumSize(200, 200)
    messageBox.setWindowTitle(windowTitle)
    messageBox.setText(message)
    messageBox.setIcon(QMessageBox.Warning)
    messageBox.setStandardButtons(QMessageBox.Ok | QMessageBox.Cancel)
    messageBox.setDefaultButton(QMessageBox.Cancel)
    ret = messageBox.exec()
        
    return ret == QMessageBox.Ok


# ========================================================================================


def createCustomChoiceDialog(title, message, width, height):
    
    dialog = QDialog(objectName="choiceDialog")
    dialog.setWindowTitle(title)
    dialog.setMinimumSize(width, height)
    
    # ---- SetUI ---
    dialog.setStyleSheet(getDialogStyle())
    # --------------

    # Create a layout and add widgets
    layout = QVBoxLayout()

    # Add a label
    messageLabel = createWidget("label", text=message, align="center")
    layout.addWidget(messageLabel)

    # Create a QDialogButtonBox with OK and Cancel buttons
    buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
    buttonBox.setDefaultButton(buttonBox.button(QDialogButtonBox.Cancel))  
    
    # Add the button box to the layout
    layout.addWidget(buttonBox)
 
    # Connect signals to slots
    buttonBox.accepted.connect(dialog.accept)
    buttonBox.rejected.connect(dialog.reject)
    
    # Set the layout for the dialog
    dialog.setLayout(layout)
        
    return dialog.exec() == QDialog.Accepted


# ========================================================================================

# Creates a frame containing an error frame, that error messages can be added to
def createErrorLayout(widget):
    
    vboxFrame = QFrame()
    
    vbox = QVBoxLayout()  
    vbox.setSpacing(1)
    vbox.setContentsMargins(0,0,0,0)
    vboxFrame.setLayout(vbox)
    
    errorFrame = QFrame()
    
    hboxLayout = QHBoxLayout()
    hboxLayout.setContentsMargins(0,0,0,0)
    errorFrame.setLayout(hboxLayout)

    vbox.addWidget(errorFrame)
    vbox.addWidget(widget)

    return errorFrame, vboxFrame

    
# ========================================================================================


# Creates a frame that also has a layout attached
def createLayoutFrame(direction=None, sizePolicy: tuple[str, str]=None, margins: tuple[int, int, int, int]=None):
    
    frame = QFrame()
    
    if direction or direction == "vertical" or direction == "v":
        layout = QVBoxLayout()
        
    else:
        layout = QHBoxLayout()
        
    if sizePolicy:
        frame.setSizePolicy(getSizePolicyMap(sizePolicy))
       
    if margins:
        layout.setContentsMargins(margins[0], margins[1], margins[2], margins[3])

    frame.setLayout(layout)
    
    return frame


# ========================================================================================


# Creates a dictionary composed of a key dictionary and a value dictionary. 
# The keys are mapped to values and the values are mapped to keys, enabling search both ways

def createTwoWayDictionary(dictionary):
    
    k = {}
    v = {}
    
    custDict = {"keyDict"   :   k,
                "valueDict" :   v}
    
    for key, value in dictionary.items():
        if keyCheck(value):
            k[key] = value
            v[value] = key
        else:
            ic("cant key dictionary")
        
    return custDict
    

# ========================================================================================


def keyCheck(value):   
    try:
        hash(value)
        return True
    except TypeError:
        return False 
    

# ========================================================================================


def getSizePolicyMap(sizePolicy):
    policyMap = {"fixed" : QSizePolicy.Fixed, "expanding" : QSizePolicy.Expanding}
        
    # Using get() on a dictionary, if sizePolicy[0] is not a key in the dictionary, it defaults to QSizePolicy.Preferred
    customSizePolicy = QSizePolicy(policyMap.get(sizePolicy[0], QSizePolicy.Preferred), policyMap.get(sizePolicy[1], QSizePolicy.Preferred))
            
    return customSizePolicy


# ========================================================================================


def getDialogStyle():
    return f"""QLabel {{
                    font-size: 15pt;
                    background-color #fcfcfc;
                    color: white;
                    padding: 10px;
                }}
                
                #dialog {{
                    background-color: black;
                }}
                """


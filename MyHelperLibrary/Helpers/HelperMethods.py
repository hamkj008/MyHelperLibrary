from icecream import ic
import os
import json

from PySide6.QtWidgets import QHBoxLayout, QLabel, QLineEdit, QDateEdit, QPushButton, QSizePolicy, QVBoxLayout, QFrame, QDialog, QMessageBox, QGridLayout
from PySide6.QtCore import Qt, QDate
from PySide6.QtGui import QPixmap


# ========================================================================================


""" Creates a pixmap from a given filename, connecting the filepath to an Images folder in the directory. 
Sets to the given width and height"""

def loadImage(fileName, width, height):
        
    imageFolder = 'Images' 
    imagePath = os.path.join(imageFolder, fileName)

    # Create QPixmap with resized image
    pixmap = QPixmap(imagePath)
    if pixmap:
        pixmap = pixmap.scaled(width, height, aspectMode=Qt.AspectRatioMode.KeepAspectRatio)
        
    return pixmap


# ========================================================================================


# Create a dictionary for all the records returned from a model query
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
        item = QDateEdit(objectName=objectName)
        item.setCalendarPopup(True)
        item.setDisplayFormat("dd-MMM-yyyy")
        currentDate = QDate.currentDate()
        item.setDate(currentDate)
        
    elif widgetType == "lineEdit":
        item = QLineEdit(objectName=objectName)
     
    if toolTip:
        item.setToolTip(toolTip)

    if sizePolicy:
        item.setSizePolicy(getSizePolicyMap(sizePolicy))
        
    if align:
        item.setAlignment(getAlignMap(align))

        
    return item


# ========================================================================================
    
    
def clearLayout(layout):
    ic("clearLayout")

    while layout.count():
        item = layout.takeAt(0)
        if item.widget():
            item.widget().deleteLater()      
                

# ========================================================================================


def clearStackedLayout(viewList, stackedWidget):
    ic("clearStackedLayout")
   
    for key in viewList.keys():
        viewList[key] = None

    while stackedWidget.count():
        widget = stackedWidget.widget(0)
        stackedWidget.removeWidget(widget)
        widget.deleteLater()      
                

# ========================================================================================
  

""" Removes a specific widgetfrom a layout """
def removeWidgetFromLayout(layout, removeWidget):
    
    # Iterate through the items in the layout
    item_count = layout.count()
    
    for i in range(item_count):
        item = layout.itemAt(i)
        
        if item.widget() == removeWidget:
            # Remove the widget from the layout
            layout.removeWidget(removeWidget)
            
            # Optionally, delete the widget
            removeWidget.deleteLater()
            
            # Break the loop as we found the widget
            break
        

# ========================================================================================
  

""" Removes any instances of a class from a layout """
def removeClassFromLayout(layout, removeClass: type):
    
    # Iterate through the items in the layout
    item_count = layout.count()
    
    for i in range(item_count):
        item = layout.itemAt(i)
        widget = item.widget()
        
        if item.widget() is not None and isinstance(widget, removeClass):
            
            # Remove the widget from the layout
            layout.removeWidget(widget)           
            widget.deleteLater()

            continue   
        

# ========================================================================================
  

# Customizable dialog box
def createCustomDialog(title, message, width, height, style):
    
    dialog = QDialog(objectName="dialog")
    dialog.setWindowTitle(title)
    dialog.setMinimumSize(width, height)
    
    # ------ Set Style ------
    dialog.setStyleSheet(style)
    # -------------------------------

    # Create a layout and add widgets
    vbox = QVBoxLayout()
    
    frame = createLayoutFrame("v", align="center")
    # Add a label
    messageLabel = createWidget("label", text=message, align="center")
    frame.layout().addWidget(messageLabel)

    # Add an OK button
    okBtn = createWidget("button", text="Ok", sizePolicy=("fixed", "fixed"))
    okBtn.clicked.connect(dialog.accept)  # Close the dialog when the button is clicked 
    btnFrame = createLayoutFrame(align="center")    
    btnFrame.layout().addWidget(okBtn)
    
    frame.layout().addWidget(btnFrame)
    vbox.addWidget(frame)
    
    # Set the layout for the dialog
    dialog.setLayout(vbox)

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


def createCustomChoiceDialog(title, message, width, height, style):

    dialog = QDialog(objectName="dialog")
    dialog.setWindowTitle(title)
    dialog.setMinimumSize(width, height)
    
    # ---- SetUI ---
    dialog.setStyleSheet(style)
    # --------------

    # Create a layout and add widgets
    frame = createLayoutFrame("v", align="center", margins=(0,0,0,0))
    frame.layout().setSpacing(50)
    # Add a label
    messageLabel = createWidget("label", text=message, align="center")
    frame.layout().addWidget(messageLabel)

    # Create a QDialogButtonBox with OK and Cancel buttons
    buttonFrame = createLayoutFrame(align="center",  margins=(0,0,0,0))
    okBtn = createWidget("button", text="Ok")
    cancelBtn = createWidget("button", text="Cancel")
    buttonFrame.layout().addWidget(okBtn)
    buttonFrame.layout().addWidget(cancelBtn)
    frame.layout().addWidget(buttonFrame)

    # Connect signals to slots
    okBtn.clicked.connect(dialog.accept)
    cancelBtn.clicked.connect(dialog.reject)
    
    # Set the layout for the dialog
    dialog.setLayout(frame.layout())
        
    return dialog.exec() == QDialog.Accepted


# ========================================================================================


# Creates a frame containing an error frame, that error messages can be added to
def createErrorLayout(widget):
    
    frame = createLayoutFrame("v", margins=(0,0,0,0)) 
    frame.layout().setSpacing(1)
    
    errorFrame = createLayoutFrame(objectName="errorFrame", margins=(0,0,0,0))

    frame.layout().addWidget(errorFrame)
    frame.layout().addWidget(widget)

    return errorFrame, frame

    
# ========================================================================================


# Creates a frame that also has a layout attached
def createLayoutFrame(layoutType=None, objectName=None, spacing: int=None, sizePolicy: tuple[str, str]=None, align=None, margins: tuple[int, int, int, int]=None):
    
    frame = QFrame(objectName=objectName)
    
    if layoutType == "vertical" or layoutType == "v":
        layout = QVBoxLayout()
     
    elif layoutType == "g" or layoutType == "grid":
        layout = QGridLayout()

    else:
        layout = QHBoxLayout()
        
    if spacing or spacing == 0:
        layout.setSpacing(spacing)

    if sizePolicy:
        frame.setSizePolicy(getSizePolicyMap(sizePolicy))
       
    if align:
        layout.setAlignment(getAlignMap(align))
        
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


def getAlignMap(alignment):
    
    align = {"left" : Qt.AlignLeft, "right" : Qt.AlignRight, "center" : Qt.AlignCenter}
    return align[alignment]


# ========================================================================================


def readJSONData(filePath):
    data = []
    if os.path.exists(filePath):
        with open(filePath, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return data  # Start with an empty list if the file is empty or invalid
    else:
        return data  # Create a new list if the file does not exist
    

# ========================================================================================


def writeJSONData(filePath, data):
    
    # Write the json file
    with open(filePath, 'w') as file:
        json.dump(data, file, indent=4)
        

# ========================================================================================


"""Retrieve an action from a menu by its text."""

def getAction(menu, actionName):
    for action in menu.actions():
        if action.text() == actionName:
            return action
    return None
    

# ========================================================================================
    
"""Create a menu with actions. Creates and returns the menu to be added (Create the list of actions first)
@parentMenu:    the parent of the menu to be added. Normally would be menubar if not a submenu
@menuName:      the name of the menu to add.
@actionList:    A list of dictionaries contaning actions using the createActionDictionary method. 
    Should contain name, shortcut(if applicable), trigger(if applicable)"""
    
def createMenu(parentMenu, menuName, actionList):

    menu = parentMenu.addMenu(f"&{menuName}")

    for item in actionList:
        if item == "separator":
            menu.addSeparator()
                
        else:
            action = menu.addAction(f"{item['actionName']}")
            action.setShortcut(f"{item.get('shortcut', '')}")
            action.triggered.connect(item.get("trigger"))
        
    return menu
    

# ========================================================================================
    

"""Create actions for a menu, such as a right click menu. 
Difference between this and createMenu is createMenu includes the menu as well
@menuName: the name of the menu to add.
@actionList: A list of dictionaries containg actions using the createActionDictionarymethod. 
    Should contain name, shortcut(if applicable), trigger(if applicable) """
    
def addActionToMenu(menu, actionList):

    for item in actionList:
        if item == "separator":
            menu.addSeparator()
                
        else:
            action = menu.addAction(f"{item['actionName']}")
            action.setShortcut(f"{item.get('shortcut', '')}")
            action.triggered.connect(item.get("trigger"))
        
    return menu


# ========================================================================================


"""Creates an action that can be used with createMenu for menus. Combines the action name, the shortcut keys, and the trigger"""

def createActionDictionary(actionName, shortcut=None, trigger=None):
        
    actionDict = {}
    actionDict["actionName"] = actionName
        
    if shortcut:
        actionDict["shortcut"] = shortcut
    if trigger:
        actionDict["trigger"] = trigger
            
    return actionDict


# ========================================================================================

"""Safely replace the triggered signal connection for a QAction."""
    
def replaceActionTriggeredConnection(action, slot):
        
    # Disconnect all existing connections
    try:
        action.triggered.disconnect()
    except RuntimeError:
        pass
        
    # Connect the new slot
    if slot:    
        action.triggered.connect(slot)
        

# ========================================================================================


"""Goes through a layout and checks what children are attached to it"""

def checkLayoutChildren(layout):

    for i in range(layout.count()):
        item = layout.itemAt(i)
        if item is None:
            ic(f"Item {i} is None")
            continue
        
        # Check if the item is a widget
        widget = item.widget()
        if widget:
            ic(widget.objectName)
            ic(type(widget))
            

# ========================================================================================
  

def showError(frame):
                
    # Set up error label
    errorLabel = QLabel("invalid format")
    errorLabel.setStyleSheet("color: red; font-size: 8pt;") 

    if not frame.isVisible():
        frame.setVisible(True)
        frame.layout().addWidget(errorLabel)


# ========================================================================================
    

def clearError(frameDict): 

    for frame in frameDict.values():
        if frame.isVisible():
            clearLayout(frame.layout())
            frame.setVisible(False)


# ========================================================================================
    

""" Cleans an input that accepts numbers (float, int). Strips whitespace, makes sure it is positive and converts to type"""
    
def cleanConvertedInput(numberType, textInput, errorFrame):
        
    if not textInput.strip(): return 0
        
    try:
        if numberType == "float":
            floatInput = float(textInput)  
            return abs(floatInput)
            
        elif numberType == "int":
            intInput = int(textInput)  
            return abs(intInput)
                
    except ValueError:
        showError(errorFrame)
        return 0
        

# ========================================================================================       

    
def getAverage(value, quantity):
        
    if value == 0 or quantity == 0:
        return 0
        
    return value / quantity   


# ========================================================================================       


def checkIconPath(icon_path):
    if os.path.exists(icon_path):
        print(f"Icon found at: {icon_path}")
    else:
        print(f"Icon NOT found at: {icon_path}")


# ========================================================================================       

from login import hoofdMenu
import os
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QDialog, QTextEdit

def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('Printen diverse formulieren')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
 
def ongDir(m_email):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Directory niet toegestaan!')
    msg.setWindowTitle('Geen bevoegdheid')
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.exec_()
    hoofdMenu(m_email)
    
def printFile(filename):
    from sys import platform
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
    
def fileList(m_email, path):
    class bestandLijst(QDialog):
       def __init__(self, parent = None):
          super(bestandLijst, self).__init__(parent)
          self.getfile()
          self.contents = QTextEdit()
          
       def getfile(self):
          fname = QFileDialog.getOpenFileName(self, 'Herprinten bestanden', path)
          if fname[0].startswith(path[1:],10):
              printFile(fname[0])
          else:
              ongDir(m_email)
    		
       def getfiles(self):
          QFileDialog.DontUseNativeDialog
          dlg = QFileDialog()
          dlg.setFileMode(QFileDialog.AnyFile)
          dlg.setFilter("Text files (*.txt)")
 
          filenames = path

          if dlg.exec_():
             filenames = dlg.selectedFiles()
             f = open(filenames[0], 'r')
             with f:
                data = f.read()
                self.contents.setText(data)
 
    bestandLijst()
    hoofdMenu(m_email)
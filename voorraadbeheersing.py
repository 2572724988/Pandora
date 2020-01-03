import datetime
from math import sqrt
from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon, QColor, QImage
from PyQt5.QtWidgets import QLabel, QPushButton, QLineEdit, QGridLayout, QDialog,\
                  QWidget,QTableView, QStyledItemDelegate, QMessageBox
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                     MetaData, create_engine, select, update)

def refresh(m_email, self):
    self.close()
    jaarVerbruik(m_email)

def artVerwerkt(rpartikel, mbestgr, minvrd):
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setWindowTitle('Voorraadbeheersing')
    msg.setIcon(QMessageBox.Information)
    msg.setText('Artikel: '+str(rpartikel[0])+'\nOmschrijving: '+rpartikel[1]+'\nMinimumvoorraad gewijzigd in '+str(minvrd)+'\nBestelgrootte gewijzigd in '+str(mbestgr))
    msg.exec_()

def aanpArt(rpartikel, mbestgr, minvrd):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('art_min_voorraad', Float),
        Column('art_bestelgrootte', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    updart = update(artikelen).where(artikelen.c.artikelID == rpartikel[0])\
      .values(art_min_voorraad = minvrd, art_bestelgrootte = mbestgr)
    con.execute(updart)
    artVerwerkt(rpartikel, mbestgr, minvrd)
 
def jaarVerbruik(m_email):
    metadata = MetaData()
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_voorraad', Float),
        Column('art_eenheid', String),
        Column('art_min_voorraad', Float),
        Column('bestelsaldo', Float),
        Column('bestelstatus', Boolean),
        Column('reserveringsaldo', Float),
        Column('categorie', Integer),
        Column('thumb_artikel', String),
        Column('art_bestelgrootte', Float),
        Column('jaarverbruik_1', Float),
        Column('jaarverbruik_2', Float))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([artikelen]).where(artikelen.c.categorie < 5).order_by(artikelen.c.artikelID)
    rpartikelen = conn.execute(sel)
          
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1800, 900)
            self.setWindowTitle('Jaarverbruik afgelopen jaar')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            self.setFont(QFont('Arial', 10))
            grid = QGridLayout()
            grid.setSpacing(20)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.setItemDelegateForColumn(10, showImage(self))
            table_view.setColumnWidth(10, 100)
            table_view.verticalHeader().setDefaultSectionSize(75)
            table_view.clicked.connect(aanpMinvoorraad)
            grid.addWidget(table_view, 0, 0, 1, 16)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl, 1, 0, 1, 2)
       
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 15, 1, 1, Qt.AlignRight)
            
            freshBtn = QPushButton('Verversen')
            freshBtn.clicked.connect(lambda: refresh(m_email, self))

            freshBtn.setFont(QFont("Arial",10))
            freshBtn.setFixedWidth(100) 
            freshBtn.setStyleSheet("color: black;  background-color: gainsboro")
   
            grid.addWidget(freshBtn, 1, 14, 1, 1, Qt.AlignRight)
        
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)

            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100) 
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            grid.addWidget(sluitBtn, 1, 13, 1, 1, Qt.AlignRight)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 1, 0, 1, 16, Qt.AlignCenter)
            
            self.setLayout(grid)
            self.setGeometry(50, 50, 1800, 900)
            self.setLayout(grid)


    class MyTableModel(QAbstractTableModel):
        def __init__(self, parent, mylist, header, *args):
            QAbstractTableModel.__init__(self, parent, *args)
            self.mylist = mylist
            self.header = header
        def rowCount(self, parent):
            return len(self.mylist)
        def columnCount(self, parent):
            return len(self.mylist[0])
        def data(self, index, role):
            if not index.isValid():
                return None
            #elif index.column() == 9 and role == Qt.DecorationRole: # alternatief picture echter
            #    return QPixmap(index.data())                        # met tekst rechts van path
            elif role != Qt.DisplayRole:
                return None
            return self.mylist[index.row()][index.column()]
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
       
    class showImage(QStyledItemDelegate):  
           def __init__(self, parent):
               QStyledItemDelegate.__init__(self, parent)
           def paint(self, painter, option, index):        
                painter.fillRect(option.rect,QColor(255,255,255))
                image = QImage(index.data())
                pixmap = QPixmap(image)
                pixmap.scaled(256,256) 
                return(painter.drawPixmap(option.rect, pixmap))
                                       
    header = ['Artikelnr', 'Omschrijving', 'Prijs', 'Voorraad', 'Eenheid','MinVrd',\
              'BestelSaldo', 'Bestelstatus', 'ReserveringSaldo', 'Categorie', 'Afbeelding',\
              'Te bestellen','Jaarverbruik-1', 'Jaarverbruik-2']    
        
    data_list=[]
    for row in rpartikelen:
        data_list += [(row)] 
        
    def aanpMinvoorraad(idx):
        martikelnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            sel = select([artikelen]).where(artikelen.c.artikelID == martikelnr)
            rpartikel = con.execute(sel).first() 
            
            metadata = MetaData()
            params = Table('params', metadata,
               Column('paramID', Integer, primary_key=True),
               Column('tarief', Float))
         
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selpar = select([params]).where(params.c.paramID == 101)
            rppar = con.execute(selpar).first()
            selpar1 = select([params]).where(params.c.paramID == 6)
            rppar1 = con.execute(selpar1).first()
            mjaar = int(str(datetime.datetime.now())[0:4])
            if mjaar%2 == 1:
                mbestgr = round(sqrt(2*rpartikel[12]*rppar[1]/rpartikel[2]*(rpartikel[2]*rppar1[1])),0)
                mjrverbr = rpartikel[12]
            else:
                mbestgr = round(sqrt(2*rpartikel[13]*rppar[1]/rpartikel[2]*(rpartikel[2]*rppar1[1])),0)
                mjrverbr = rpartikel[13]
            if rpartikel[9] == 1:
                minvrd = round(mjrverbr*1/17, 0) # 3 weken levertijd
            elif rpartikel[9] == 2:
                minvrd = round(mjrverbr*2/17, 0) # 6 weken levertijd
            elif rpartikel[9] == 3:  
                minvrd = round(mjrverbr*4/17, 0) # 12 weken levertijd
            elif rpartikel[9] == 4: 
                 minvrd = round(mjrverbr*8/17, 0) # 24 weken levertijd
            class Widget(QDialog):
                def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                
                    self.setWindowTitle("Aanpassen minimumvoorraad / bestelgrootte")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                
                    self.setFont(QFont('Arial', 10))
                               
                    self.Artikelnummer = QLabel()
                    q1Edit = QLineEdit(str(rpartikel[0]))
                    q1Edit.setFixedWidth(100)
                    q1Edit.setDisabled(True)
                    q1Edit.setFont(QFont("Arial",10))
                
                    self.Artikelomschrijving = QLabel()
                    q2Edit = QLineEdit(str(rpartikel[1]))
                    q2Edit.setFixedWidth(400)
                    q2Edit.setFont(QFont("Arial",10))
                    q2Edit.setDisabled(True)
                    
                    self.Artikelprijs = QLabel()
                    q3Edit = QLineEdit(str(rpartikel[2]))
                    q3Edit.setFixedWidth(100)
                    q3Edit.setFont(QFont("Arial",10))
                    q3Edit.setDisabled(True)
                                    
                    self.Artikelvoorraad = QLabel()
                    q4Edit = QLineEdit(str(rpartikel[3]))
                    q4Edit.setFixedWidth(100)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setDisabled(True)
                    
                    self.Artikeleenheid = QLabel()
                    q5Edit = QLineEdit(rpartikel[4])
                    q5Edit.setFixedWidth(100)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)
                    
                    self.Minimumvoorraad = QLabel()
                    q6Edit = QLineEdit(str(rpartikel[5]))
                    q6Edit.setFixedWidth(100)
                    q6Edit.setFont(QFont("Arial",10))
                    q6Edit.setDisabled(True)
                     
                    self.Bestelsaldo = QLabel()
                    q16Edit = QLineEdit(str(rpartikel[6]))
                    q16Edit.setFixedWidth(100)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
    
                    self.Bestelstatus = QLabel()
                    q7Edit = QLineEdit(str(rpartikel[7]))
                    q7Edit.setFixedWidth(100)
                    q7Edit.setFont(QFont("Arial",10))
                    q7Edit.setDisabled(True)
                    
                    self.Reserveringsaldo = QLabel()
                    q12Edit = QLineEdit(str(rpartikel[8]))
                    q12Edit.setFixedWidth(100)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.setDisabled(True)
                                   
                    self.Categorie = QLabel()
                    q8Edit = QLineEdit(str(rpartikel[9]))
                    q8Edit.setFixedWidth(100)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
 
                    self.Bestelgrootte = QLabel()
                    q9Edit = QLineEdit(str(rpartikel[11]))
                    q9Edit.setFixedWidth(100)
                    q9Edit.setFont(QFont("Arial",10))
                    q9Edit.setDisabled(True)
                    
                    self.Jaarverbruik_1 = QLabel()
                    q14Edit = QLineEdit(str(rpartikel[12]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setDisabled(True) 
                    
                    self.Jaarverbruik_2 = QLabel()
                    q13Edit = QLineEdit(str(rpartikel[13]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.setDisabled(True)   
                    
                    self.Minvrd_berekening = QLabel()
                    q10Edit = QLineEdit(str(int(minvrd)))
                    q10Edit.setFixedWidth(100)
                    q10Edit.setFont(QFont("Arial",10))
                    q10Edit.setReadOnly(True)
                    
                    self.Bestelhoev_berekening = QLabel()
                    q11Edit = QLineEdit(str(int(mbestgr)))
                    q11Edit.setFixedWidth(100)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.setReadOnly(True)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl , 0, 0, 1, 2)
                
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 2, 1, 3, Qt.AlignRight) 
                  
                    grid.addWidget(QLabel('Artikelnummer'), 1, 0, 2, 1)
                    grid.addWidget(q1Edit, 1, 1, 2, 1)
                
                    grid.addWidget(QLabel('Artikelomschrijving'), 3, 0)
                    grid.addWidget(q2Edit, 3, 1, 1 ,3)
                    
                    grid.addWidget(QLabel('Eenheid'), 5, 0)
                    grid.addWidget(q5Edit, 5, 1)
                    
                    grid.addWidget(QLabel('Artikelprijs'), 5, 2)
                    grid.addWidget(q3Edit, 5 , 3) 
                    
                    grid.addWidget(QLabel('Voorraad'), 6, 0)
                    grid.addWidget(q4Edit, 6, 1)
                                  
                    grid.addWidget(QLabel('Minimum voorraad'), 6, 2)
                    grid.addWidget(q6Edit, 6, 3)
                    
                    grid.addWidget(QLabel('Bestelsaldo'), 7, 0)
                    grid.addWidget(q16Edit, 7, 1)
                    
                    grid.addWidget(QLabel('Reserveringsaldo '), 8, 0)
                    grid.addWidget(q12Edit, 8, 1)
                                       
                    grid.addWidget(QLabel('BestelStatus'),7 ,2)
                    grid.addWidget(q7Edit, 7, 3)
                    
                    grid.addWidget(QLabel('Categorie'),8 ,2)
                    grid.addWidget(q8Edit, 8,3)
                    
                    grid.addWidget(QLabel('Bestelgrootte'),9 ,0)
                    grid.addWidget(q9Edit, 9,1)
                    
                    grid.addWidget(QLabel('Jaarverbruik-1'),10, 0)
                    grid.addWidget(q14Edit, 10, 1)

                    grid.addWidget(QLabel('Jaarverbruik-2'),10, 2)
                    grid.addWidget(q13Edit, 10, 3)                    
                    
                    grid.addWidget(QLabel('Minimum voorraad\nberekening '),11 ,0)
                    grid.addWidget(q10Edit, 11,1) 
                    
                    grid.addWidget(QLabel('Te bestellen\nberekening'),11, 2)
                    grid.addWidget(q11Edit, 11, 3)
                    
                    pixmap = QPixmap(rpartikel[10])
                    lbl2 = QLabel(self)
                    lbl2.setPixmap(pixmap)
                    grid.addWidget(lbl2 , 1, 2, 2, 2, Qt.AlignRight)
                
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
                    
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 12, 2, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    aanpBtn = QPushButton('Aanpassen')
                    aanpBtn.clicked.connect(lambda: aanpArt(rpartikel, mbestgr, minvrd))
                   
                    grid.addWidget(aanpBtn, 12, 3, 1, 1, Qt.AlignRight)
                    aanpBtn.setFont(QFont("Arial",10))
                    aanpBtn.setFixedWidth(100) 
                    aanpBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
                    self.setLayout(grid)
                    self.setGeometry(500, 100, 350, 300)
                
            window = Widget()
            window.exec_()
                                            
    win = MyWindow(data_list, header)
    win.exec_()
    hoofdMenu(m_email)
from login import hoofdMenu
from PyQt5.QtCore import Qt, QAbstractTableModel
from PyQt5.QtGui import QFont, QPixmap, QIcon
from PyQt5.QtWidgets import  QLabel, QPushButton, QWidget, QGridLayout,\
     QComboBox, QDialog, QLineEdit, QMessageBox, QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, ForeignKey,  Integer, String, MetaData,\
                       create_engine, Float)
from sqlalchemy.sql import select, and_ 

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Dienstenorderrs opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen record gevonden\nmaak een andere selektie s.v.p.!')
    msg.setWindowTitle('Dienstenorders opvragen')               
    msg.exec_() 

def inkooporderKeuze(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Opvragen Inkooporder Diensten")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Keuze = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(330)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: gainsboro")
            k0Edit.addItem('                Sorteersleutel voor zoeken')
            k0Edit.addItem('1. Alle dienstenorders op werknr gesorteerd')
            k0Edit.addItem('2. Filter op bedrijfsnaam')
            k0Edit.addItem('3. Filter op naam extern werk')
            k0Edit.addItem('4. Filter op extern werknummer')
            k0Edit.addItem('5. Filter op inkoopordernummer.')
            k0Edit.addItem('6. Levertijd yyyy(-mm(-dd))')
            k0Edit.activated[str].connect(self.k0Changed)
                            
            self.Zoekterm = QLabel()
            zktermEdit = QLineEdit()
            zktermEdit.setFixedWidth(220)
            zktermEdit.setFont(QFont("Arial",10))
            zktermEdit.textChanged.connect(self.zktermChanged)
     
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
                                  
            grid.addWidget(k0Edit, 1, 0, 1, 2, Qt. AlignRight)
            lbl1 = QLabel('Zoekterm')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zktermEdit, 2, 1, 1, 1 , Qt.AlignRight)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 2, Qt.AlignRight)
    
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
         
            grid.addWidget(applyBtn, 3, 1, 1, 2, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(110)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))   
            grid.addWidget(cancelBtn, 3, 1)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(110)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
       
        def k0Changed(self, text):
            self.Keuze.setText(text)
            
        def zktermChanged(self, text):
            self.Zoekterm.setText(text)
 
        def returnk0(self):
            return self.Keuze.text()
        
        def returnzkterm(self):
            return self.Zoekterm.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(), dialog.returnzkterm()]       

    window = Widget()
    data = window.getData()
    if not data[0] or data[0][0] == ' ':
        keuze = 0
    elif data[0]:
        keuze = int(data[0][0])
    else:
        keuze = 0
    if data[1]:
        zoekterm = data[1]
    else:
        zoekterm = ''
    opvrDienstorders(keuze,zoekterm, m_email)
    
def opvrDienstorders(keuze,zoekterm, m_email):
    import validZt
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer(), primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.leverancierID')),
        Column('besteldatum', String),
        Column('goedgekeurd', String),
        Column('betaald', String),
        Column('afgemeld', String))
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String))
    orders_inkoop_diensten = Table('orders_inkoop_diensten', metadata,
        Column('orddienstlevID', Integer(), primary_key=True),
        Column('orderinkoopID', None, ForeignKey('orders_inkoop.orderinkoopID')),
        Column('werknummerID', None, ForeignKey('werken.werknummerID')),
        Column('werkomschr', String),
        Column('omschrijving', String),
        Column('aanneemsom', Float),
        Column('plan_start', String),
        Column('werk_start', String),
        Column('plan_gereed', String),
        Column('werk_gereed', String),
        Column('acceptatie_gereed', Float),
        Column('acceptatie_datum', String),
        Column('meerminderwerk', Float),
        Column('regel', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('werkomschrijving', String))
      
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
 
    if keuze == 1:
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken]).\
         where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
           leverancierID, orders_inkoop_diensten.c.werknummerID == werken.c.\
           werknummerID, orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.\
           orderinkoopID)).order_by(orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 2:
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
        .where(and_(orders_inkoop_diensten.c.orderinkoopID==orders_inkoop.c.orderinkoopID,\
          orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
          orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
          leveranciers.c.bedrijfsnaam.ilike('%'+zoekterm+'%'))).order_by\
           (orders_inkoop.c.leverancierID, orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 3:
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          werken.c.werkomschrijving.ilike('%'+zoekterm+'%'))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 4 and validZt.zt(zoekterm, 8):
       sel = select([orders_inkoop_diensten,orders_inkoop, leveranciers, werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
          werken.c.werknummerID == int(zoekterm))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 5 and validZt.zt(zoekterm, 4):
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
            orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_diensten.c.orderinkoopID == int(zoekterm))).order_by\
         (orders_inkoop_diensten.c.werknummerID, orders_inkoop_diensten.c.\
          orderinkoopID, orders_inkoop_diensten.c.regel)
    elif keuze == 6 and validZt.zt(zoekterm, 10):
        sel = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
         .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.leverancierID,\
         orders_inkoop_diensten.c.werknummerID == werken.c.werknummerID,\
         orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.orderinkoopID,
         orders_inkoop_diensten.c.plan_gereed.like(zoekterm+'%'))).order_by\
         (orders_inkoop_diensten.c.plan_gereed, orders_inkoop_diensten.c.werknummerID,\
           orders_inkoop_diensten.c.orderinkoopID, orders_inkoop_diensten.c.regel)
    else:
        ongInvoer()
        inkooporderKeuze(m_email)
        
    if con.execute(sel).fetchone():
        rpinkorders = con.execute(sel)
    else:
        geenRecord()
        inkooporderKeuze(m_email)
                                     
    class Window(QDialog):
       def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1600, 900)
            self.setWindowTitle('Inkooporders diensten opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.resizeColumnsToContents()
            table_view.setColumnHidden(2,True)
            table_view.setColumnHidden(14,True)
            table_view.setColumnHidden(15,True)
            table_view.setSelectionBehavior(QTableView.SelectRows)
            table_view.clicked.connect(showOrder)
            layout = QVBoxLayout(self)
            layout.addWidget(table_view)
            self.setLayout(layout)
    
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
            elif role != Qt.DisplayRole:
                return None
            return self.mylist[index.row()][index.column()]
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
       
    header = ['Orderinkoopdienstnr','Orderinkoopnr', 'Werknummer','Dienstsoort', 'Dienstomschrijving', 'Aanneemsom',\
          'Planning start', 'Werkelijk start','Panning gereed', 'Werkelijk gereed', 'Acceptatie gereed', 'Acceptatie datum', 'Meerminderwerk',\
          'Regelnr', 'Orderinkoopnr','Leverancier', 'Besteldatum', 'Goedgekeurd', 'Betaald',\
          'Afgemeld','Leveranciernummer', 'Leveranciernaam' ,'Rechtsvorm','Werknummer','Werkomschrijving']    
        
    data_list=[]
    for row in rpinkorders:
        data_list += [(row)] 
        
    def showOrder(idx):
        mordinkdnst = idx.data()
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        con = engine.connect()
        if idx.column() == 0:
            selorddnst = select([orders_inkoop_diensten, orders_inkoop, leveranciers,werken])\
                .where(and_(orders_inkoop.c.leverancierID == leveranciers.c.\
                leverancierID, orders_inkoop_diensten.c.werknummerID == werken.c.\
                werknummerID, orders_inkoop_diensten.c.orderinkoopID == orders_inkoop.c.\
                orderinkoopID, orders_inkoop_diensten.c.orddienstlevID == mordinkdnst))
            rporddnst = con.execute(selorddnst).first() 
            class Widget(QDialog):
                 def __init__(self, parent=None):
                    super(Widget, self).__init__(parent)
                    self.setWindowTitle("Inkooporders diensten opvragen")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                          
                    self.setFont(QFont('Arial', 10))
                        
                    self.Orderinkoopdienst = QLabel()
                    q2Edit = QLineEdit(str(rporddnst[14]))
                    q2Edit.setFixedWidth(90)
                    q2Edit.setDisabled(True)
                    q2Edit.setFont(QFont("Arial",10))
        
                    self.Leveranciernummer = QLabel()
                    q4Edit = QLineEdit(str(rporddnst[15]))
                    q4Edit.setFixedWidth(90)
                    q4Edit.setFont(QFont("Arial",10))
                    q4Edit.setDisabled(True)
         
                    self.Besteldatum = QLabel()
                    q5Edit = QLineEdit(str(rporddnst[16]))
                    q5Edit.setFixedWidth(90)
                    q5Edit.setFont(QFont("Arial",10))
                    q5Edit.setDisabled(True)                              
                    
                    self.Goedgekeurd = QLabel()
                    q8Edit = QLineEdit(str(rporddnst[17]))
                    q8Edit.setFixedWidth(90)
                    q8Edit.setFont(QFont("Arial",10))
                    q8Edit.setDisabled(True)
                                                         
                    self.Betaald = QLabel()
                    q18Edit = QLineEdit(str(rporddnst[18]))
                    q18Edit.setFixedWidth(90)
                    q18Edit.setFont(QFont("Arial",10))
                    q18Edit.setDisabled(True)
                      
                    self.Afgemeld = QLabel()
                    q12Edit = QLineEdit(str(rporddnst[19]))
                    q12Edit.setFixedWidth(90)
                    q12Edit.setFont(QFont("Arial",10))
                    q12Edit.setDisabled(True)
                     
                    self.Leveranciernummer = QLabel()
                    q13Edit = QLineEdit(str(rporddnst[20]))
                    q13Edit.setFixedWidth(100)
                    q13Edit.setFont(QFont("Arial",10))
                    q13Edit.setDisabled(True)
             
                    self.Bedrijfsnaam = QLabel()
                    q19Edit = QLineEdit(str(rporddnst[21]))
                    q19Edit.setFixedWidth(380)
                    q19Edit.setFont(QFont("Arial",10))
                    q19Edit.setDisabled(True)
             
                    self.Rechtsvorm = QLabel()
                    q14Edit = QLineEdit(str(rporddnst[22]))
                    q14Edit.setFixedWidth(100)
                    q14Edit.setFont(QFont("Arial",10))
                    q14Edit.setDisabled(True)
                                    
                    self.Werknummer = QLabel()
                    q15Edit = QLineEdit(str(rporddnst[23]))
                    q15Edit.setDisabled(True)
                    q15Edit.setFixedWidth(100)
                    q15Edit.setFont(QFont("Arial",10))
                    q15Edit.setDisabled(True)
          
                    self.Werkomschrijving = QLabel()
                    q16Edit = QLineEdit(str(rporddnst[24]))
                    q16Edit.setFixedWidth(390)
                    q16Edit.setFont(QFont("Arial",10))
                    q16Edit.setDisabled(True)
         
                    self.Dienstomschrijving = QLabel()
                    q17Edit = QLineEdit(str(rporddnst[4]))
                    q17Edit.setFixedWidth(390)
                    q17Edit.setFont(QFont("Arial",10))
                    q17Edit.setDisabled(True)
                    
                    self.Dienstsoort = QLabel()
                    q11Edit = QLineEdit(str(rporddnst[3]))
                    q11Edit.setFixedWidth(150)
                    q11Edit.setFont(QFont("Arial",10))
                    q11Edit.setDisabled(True)
                    
                    self.Aanneemsom = QLabel()
                    q20Edit = QLineEdit(str(rporddnst[5]))
                    q20Edit.setFixedWidth(100)
                    q20Edit.setFont(QFont("Arial",10))
                    q20Edit.setDisabled(True)
                    
                    self.Planstart = QLabel()
                    q21Edit = QLineEdit(str(rporddnst[6]))
                    q21Edit.setFixedWidth(100)
                    q21Edit.setFont(QFont("Arial",10))
                    q21Edit.setDisabled(True)
    
                    self.Werkelijkstart = QLabel()
                    q22Edit = QLineEdit(str(rporddnst[7]))
                    q22Edit.setFixedWidth(100)
                    q22Edit.setFont(QFont("Arial",10))
                    q22Edit.setDisabled(True)
    
                    self.Plangereed = QLabel()
                    q23Edit = QLineEdit(str(rporddnst[8]))
                    q23Edit.setFixedWidth(100)
                    q23Edit.setFont(QFont("Arial",10))
                    q23Edit.setDisabled(True)
                    
                    self.Werkelijkgereed = QLabel()
                    q24Edit = QLineEdit(str(rporddnst[9]))
                    q24Edit.setFixedWidth(100)
                    q24Edit.setFont(QFont("Arial",10))
                    q24Edit.setDisabled(True)
                    
                    self.AcceptatieaantaL = QLabel()
                    q25Edit = QLineEdit(str(rporddnst[10]))
                    q25Edit.setFixedWidth(100)
                    q25Edit.setFont(QFont("Arial",10))
                    q25Edit.setDisabled(True)
                    
                    self.Acceptatiedatum = QLabel()
                    q26Edit = QLineEdit(str(rporddnst[11]))
                    q26Edit.setFixedWidth(100)
                    q26Edit.setFont(QFont("Arial",10))
                    q26Edit.setDisabled(True)
                    
                    self.Meerminderwerk = QLabel()
                    q27Edit = QLineEdit(str(rporddnst[12]))
                    q27Edit.setFixedWidth(100)
                    q27Edit.setFont(QFont("Arial",10))
                    q27Edit.setDisabled(True) 
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    lbl = QLabel()
                    pixmap = QPixmap('./images/logos/verbinding.jpg')
                    lbl.setPixmap(pixmap)
                    grid.addWidget(lbl ,0 , 0)
                    
                    logo = QLabel()
                    pixmap = QPixmap('./images/logos/logo.jpg')
                    logo.setPixmap(pixmap)
                    grid.addWidget(logo , 0, 5, 1, 1, Qt.AlignRight)
            
                    self.setFont(QFont('Arial', 10))
                    
                    lbl1 = QLabel('Ordergegevens')
                    lbl1.setStyleSheet("font: 12pt Comic Sans MS")
                    grid.addWidget(lbl1, 1, 0)
                    grid.addWidget(QLabel('Orderinkoopnummer'), 2, 0)
                    grid.addWidget(q2Edit, 2, 1) 
                                                        
                    grid.addWidget(QLabel('Leveranciernummer'), 2, 2)
                    grid.addWidget(q4Edit, 2, 3)
                    
                    grid.addWidget(QLabel('Besteldatum'), 2, 4)
                    grid.addWidget(q5Edit, 2 , 5) 
                     
                    grid.addWidget(QLabel('Goedgekeurd'), 3, 0)
                    grid.addWidget(q8Edit, 3, 1)
                                                              
                    grid.addWidget(QLabel('Betaald'), 3, 2)
                    grid.addWidget(q18Edit, 3, 3)
                                              
                    grid.addWidget(QLabel('Afgemeld'), 3, 4)
                    grid.addWidget(q12Edit, 3, 5)
     
                    lbl2 = QLabel('Orderregelgegevens'+' - regelnummer: '+str(rporddnst[13]))
                    lbl2.setStyleSheet("font: 12pt Comic Sans MS")               
                    grid.addWidget(lbl2, 5, 0, 1, 4)
                    grid.addWidget(QLabel('Leveranciernummer'), 6, 0)
                    grid.addWidget(q13Edit, 6, 1) 
                    
                    grid.addWidget(QLabel('Bedrijfsnaam'), 7, 0)
                    grid.addWidget(q19Edit, 7, 1, 1, 4) 
                                   
                    grid.addWidget(q14Edit, 7, 4) 
               
                    grid.addWidget(QLabel('Werknummer'), 8, 0)
                    grid.addWidget(q15Edit, 8, 1) 
                                                           
                    grid.addWidget(QLabel('Werkomschrijving'), 9, 0)
                    grid.addWidget(q16Edit, 9, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Dienstomschrijving'), 10, 0)
                    grid.addWidget(q17Edit, 10, 1, 1, 3)
                    
                    grid.addWidget(QLabel('Dienstsoort'), 11, 0)
                    grid.addWidget(q11Edit, 11, 1)
                    
                    grid.addWidget(QLabel('Aanneemsom'), 11, 2)
                    grid.addWidget(q20Edit, 11, 3)
                                    
                    grid.addWidget(QLabel('Planning Start'), 11, 4)
                    grid.addWidget(q21Edit, 11, 5)
                    
                    grid.addWidget(QLabel('Werkelijk start'), 12, 0)
                    grid.addWidget(q22Edit, 12, 1)
                    
                    grid.addWidget(QLabel('Planning gereed'), 12, 2)
                    grid.addWidget(q23Edit, 12, 3)
                    
                    grid.addWidget(QLabel('Werkelijk gereed'), 12, 4)
                    grid.addWidget(q24Edit, 12, 5)
                    
                    grid.addWidget(QLabel('Acceptatie gereed'), 13,  0)
                    grid.addWidget(q25Edit, 13, 1)
                    
                    grid.addWidget(QLabel('Acceptatie datum'), 13, 2)
                    grid.addWidget(q26Edit, 13, 3)
                   
                    grid.addWidget(QLabel('Meerminderwerk'), 13, 4)
                    grid.addWidget(q27Edit, 13, 5)
                                                                            
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 15, 0, 1, 6, Qt.AlignCenter)
                    self.setLayout(grid)
                    self.setGeometry(500, 200, 350, 300)
                                               
                    cancelBtn = QPushButton('Sluiten')
                    cancelBtn.clicked.connect(self.close)
                
                    grid.addWidget(cancelBtn, 14, 5, 1, 1, Qt.AlignRight)
                    cancelBtn.setFont(QFont("Arial",10))
                    cancelBtn.setFixedWidth(100)
                    cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            window = Widget()
            window.exec_()
                                   
    win = Window(data_list, header)
    win.exec_()
    inkooporderKeuze(m_email)
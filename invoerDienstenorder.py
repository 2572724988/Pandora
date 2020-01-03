from login import hoofdMenu
import datetime
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
                QDialog, QMessageBox ,QComboBox 
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, ForeignKey, \
                        MetaData, create_engine, func)
from sqlalchemy.sql import select, insert, update, and_

def foutLeverancier():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))        
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Leverancier/Werknummer\nniet gevonden!')
        msg.setWindowTitle('INKOOPORDER')
        msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
                 
def _11check(mlevnr):
    number = str(mlevnr)
    total = 0       
    fullnumber = number                       
    for i in range(8):
        total += int(fullnumber[i])*(9-i)
        checkdigit = total % 11
    if checkdigit == 10:
        checkdigit = 0
    if checkdigit == int(fullnumber[8]):
        return True
    else:
        return False
 
def maak11proef(basisnr):
   basisnr = str(basisnr)
   basisnr = str((int(basisnr[0:8]))+int(1))
   total = 0                       
   for i in range(int(8)):
       total += int(basisnr[i])*(int(9)-i)
   checkdigit = total % 11
   if checkdigit == 10:
            checkdigit = 0
   basisuitnr = basisnr+str(checkdigit)
   return basisuitnr

def zoekLeverancier(m_email):
    metadata = MetaData()
    leveranciers = Table('leveranciers', metadata,
        Column('leverancierID', Integer(), primary_key=True),
        Column('bedrijfsnaam', String),
        Column('rechtsvorm', String),
        Column('postcode', String),
        Column('huisnummer', String),
        Column('toevoeging', String))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True))
            
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()

    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Orders diensten invoeren.")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                            
            self.Leveranciernummer = QLabel()
            levEdit = QLineEdit()
            levEdit.setFixedWidth(100)
            levEdit.setFont(QFont("Arial",10))
            levEdit.textChanged.connect(self.levChanged)
            reg_ex = QRegExp('^[3]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            levEdit.setValidator(input_validator)
                            
            self.Werknummer = QLabel()
            werknEdit = QLineEdit()
            werknEdit.setFixedWidth(100)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
            reg_ex = QRegExp('^[8]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, levEdit)
            werknEdit.setValidator(input_validator)
            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 2, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Leverancier\nWerknummer\n  Diensten'), 0, 1)
    
            grid.addWidget(QLabel('Leverancier'), 1, 0)
            grid.addWidget(levEdit, 1, 1)
            
            grid.addWidget(QLabel('Werknummer'), 2, 0)
            grid.addWidget(werknEdit, 2, 1)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 3, 0, 1 ,3, Qt.AlignCenter)
       
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 2, 2)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(120)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
        
            grid.addWidget(cancelBtn, 1, 2)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(120)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(300, 300, 150, 150)
    
        def levChanged(self, text):
            self.Leveranciernummer.setText(text)
            
        def werknChanged(self, text):
            self.Werknummer.setText(text)
    
        def returnLeveranciernummer(self):
            return self.Leveranciernummer.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnLeveranciernummer(), dialog.returnWerknummer()]
       
    window = Widget()
    data = window.getData()
    if data[0] and data[1] and len(data[0]) == 9 and len(data[1]) == 9\
           and _11check(data[0]) and  _11check(data[1]):
        mlevnr = int(data[0])
        mwerknr = int(data[1])
    else:
        check = 0
        foutLeverancier()
        return(check)
    sel = select([leveranciers, werken]).where(and_(leveranciers.c.leverancierID\
                == mlevnr, werken.c.werknummerID == mwerknr))
    rplev = conn.execute(sel).first()
    if not rplev:
        check = 0
        return(check)
    return(rplev)
           
def bepaalInkoopOrdernr():
    metadata = MetaData()
    orders_inkoop = Table('orders_inkoop', metadata,
        Column('orderinkoopID', Integer, primary_key=True),
        Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    
    morderinkoopnr=(conn.execute(select([func.max(orders_inkoop.c.orderinkoopID, type_=Integer)\
                                   .label('morderinkoopnr')])).scalar())
    morderinkoopnr=int(maak11proef(morderinkoopnr))
    conn.close
    return(morderinkoopnr)
   
def Inkooporder(m_email):
    rplev = zoekLeverancier(m_email)
    if rplev:
        mlevnr = int(rplev[0])
        mwerknr = int(rplev[6])
    else:
        check = 0
        return(check)
    mbedrnaam = rplev[1]
    mrechtsvorm = rplev[2]
    mpostcode = rplev[3]
    mhuisnr = int(rplev[4])
    if rplev[5]:
        mtoev = rplev[5]
    else:
        mtoev=''
    import postcode
    mstrplts = postcode.checkpostcode(mpostcode, mhuisnr)
    mstraat = mstrplts[0]
    mplaats = mstrplts[1]
    minkordnr = bepaalInkoopOrdernr()
    return(minkordnr, mlevnr, mbedrnaam, mrechtsvorm, mstraat, mhuisnr,\
               mtoev, mpostcode, mplaats, mwerknr)
    
def inkoopRegels(minkgeg, mregel):
    if not minkgeg:
        check = 0
        return(check)
    minkordnr = minkgeg[0]
    mlevnr = minkgeg[1]
    mwerknr = minkgeg[9]
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Bestelregels diensten inbrengen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
                       
            self.Inkoopordernummer = QLabel()
            inkorderEdit = QLineEdit(str(minkordnr))
            inkorderEdit.setDisabled(True)
            inkorderEdit.setFixedWidth(100)
            inkorderEdit.setFont(QFont("Arial",10))
            inkorderEdit.textChanged.connect(self.inkorderChanged) 
        
            self.Werknummer = QLabel()
            werknEdit = QLineEdit(str(mwerknr))
            werknEdit.setFixedWidth(100)
            werknEdit.setDisabled(True)
            werknEdit.setFont(QFont("Arial",10))
            werknEdit.textChanged.connect(self.werknChanged)
            
            self.Soort = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(150)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: gainsboro")
            k0Edit.addItem(' Maak Uw Keuze')
            k0Edit.addItem('1. Materieel')
            k0Edit.addItem('2. Leiding')
            k0Edit.addItem('3. Huisvesting')
            k0Edit.addItem('4. Overig')
            k0Edit.addItem('5. Inhuur')
            k0Edit.addItem('6. Vervoer')
            k0Edit.addItem('7. Beton')
            k0Edit.addItem('8. Kabelwerk')
            k0Edit.addItem('9. Grondverzet')
            k0Edit.activated[str].connect(self.k0Changed)
            
            self.OrderregelPrijs = QLabel()
            q1Edit = QLineEdit()
            q1Edit.setFixedWidth(130)
            q1Edit.setFont(QFont("Arial",10))
            q1Edit.textChanged.connect(self.q1Changed) 
            reg_ex = QRegExp("^[0-9.]{0,12}$")
            input_validator = QRegExpValidator(reg_ex, q1Edit)
            q1Edit.setValidator(input_validator)
            
            self.Omschrijving = QLabel()
            q2Edit = QLineEdit()
            q2Edit.setFixedWidth(400)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.textChanged.connect(self.q2Changed) 
            reg_ex = QRegExp("^.{0,50}$")
            input_validator = QRegExpValidator(reg_ex,q2Edit)
            q2Edit.setValidator(input_validator)    
        
            self.GeplandeStart = QLabel()
            q3Edit = QLineEdit()
            q3Edit.setCursorPosition(0)
            q3Edit.setFixedWidth(130)
            q3Edit.setFont(QFont("Arial",10))
            q3Edit.textChanged.connect(self.q3Changed) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q3Edit)
            q3Edit.setValidator(input_validator)  
            
            self.GeplandGereed = QLabel()
            q4Edit = QLineEdit()
            q4Edit.setCursorPosition(0)
            q4Edit.setFixedWidth(130)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.textChanged.connect(self.q4Changed) 
            reg_ex = QRegExp('^[2]{1}[0]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, q4Edit)
            q4Edit.setValidator(input_validator)  
                        
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,1, 0)
            
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Bestelling voor\nLeverancier: '+str(minkgeg[1])\
            +',\n'+minkgeg[2]+' '+minkgeg[3]+',\n'+minkgeg[4]+' '+str(minkgeg[5])\
            +minkgeg[6]+',\n'+minkgeg[7]+' '+minkgeg[8]+'.\nOrderregel '+str(mregel)), 1, 1, 1, 3)
                                             
            lbl1 = QLabel('Ordernummer')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 5, 0)
            grid.addWidget(inkorderEdit, 5, 1)
            
            grid.addWidget(QLabel('Werknummer'), 6, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(werknEdit, 6, 1)  
                                                         
            lbl3 = QLabel('Discipline')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 7, 0)
            grid.addWidget(k0Edit, 7, 1)
                       
            lbl4 = QLabel('Aanneemsom')  
            lbl4.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl4, 8, 0)
            grid.addWidget(q1Edit,8, 1)
            
            lbl5 = QLabel('Omschrijving')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 9, 0)
            grid.addWidget(q2Edit, 9, 1, 1 , 3)
            
            lbl6 = QLabel('Geplande Start jjjj-mm-dd')  
            lbl6.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl6, 10, 0)
            grid.addWidget(q3Edit, 10, 1)
            
            lbl7 = QLabel('Gepland Gereed jjjj-mm-dd')  
            lbl7.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl7, 11, 0)
            grid.addWidget(q4Edit, 11, 1)
                   
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 13, 0, 1, 4, Qt.AlignCenter)
         
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 3, 1 , 1, Qt.AlignRight)
                       
            self.setLayout(grid)
            self.setGeometry(100, 100, 150, 150)
    
            applyBtn = QPushButton('Invoeren')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 12, 3, 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            sluitBtn = QPushButton('Sluiten')
            sluitBtn.clicked.connect(self.close)
    
            grid.addWidget(sluitBtn, 12, 2, 1, 2)
            sluitBtn.setFont(QFont("Arial",10))
            sluitBtn.setFixedWidth(100)
            sluitBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                                                                            
        def inkorderChanged(self, text):
            self.Inkoopordernummer.setText(text)
            
        def werknChanged(self, text):
            self.Werknummer.setText(text)
            
        def k0Changed(self,text):
            self.Soort.setText(text)
            
        def q1Changed(self,text):
            self.OrderregelPrijs.setText(text)
            
        def q2Changed(self,text):
            self.Omschrijving.setText(text)
        
        def q3Changed(self,text):
            self.GeplandeStart.setText(text)
            
        def q4Changed(self,text):
            self.GeplandGereed.setText(text)
          
        def returninkorder(self):
            return self.Inkoopordernummer.text()
        
        def returnWerknummer(self):
            return self.Werknummer.text()    
        
        def returnk0(self):
            return self.Soort.text()
        
        def returnq1(self):
            return self.Omschrijving.text()
        
        def returnq2(self):
            return self.OrderregelPrijs.text()
        
        def returnq3(self):
            return self.GeplandeStart.text()
        
        def returnq4(self):
            return self.GeplandGereed.text()
       
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnk0(),dialog.returnq1(), dialog.returnq2(),\
                    dialog.returnq3(), dialog.returnq4()]  
   
    window = Widget()
    data = window.getData()
    check = 1
    if mregel == 1 and data[0]:
        datum = str(datetime.datetime.now())
        mbestdatum = (datum[0:4]+'-'+datum[8:10]+'-'+datum[5:7])
        metadata = MetaData()
        orders_inkoop = Table('orders_inkoop', metadata,
            Column('orderinkoopID', Integer(), primary_key=True),
            Column('leverancierID', None, ForeignKey('leveranciers.c.leverancierID')),
            Column('besteldatum', String),
            Column('status', Integer))
        engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
        conn = engine.connect()
        mbestdatum = (datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))[0:10]
        ins = insert(orders_inkoop).values(orderinkoopID = minkordnr, leverancierID =\
                    mlevnr, besteldatum = mbestdatum, status = 1)
        conn.execute(ins)
        conn.close
    if data[0]:
        check = 1
        soort = data[0]
    else:
        check = 0
        return(check)
    if data[2]:
        mprijs = float(data[2])
    else:
        check = 0
        return(check)       
    if data[1]:
        momschr = data[1]
    else:
       check = 0
       return(check)
    if data[3]:
        geplstart = data[3]
    else:
       check = 0
       return(check)
    if data[4]:
        geplgereed = data[4]
    else:
       check = 0
       return(check)
      
    metadata = MetaData()
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
        Column('regel', Integer))
    werken = Table('werken', metadata,
        Column('werknummerID', Integer, primary_key=True),
        Column('begr_materieel', Float),
        Column('begr_leiding' , Float),
        Column('begr_huisv', Float ),
        Column('begr_overig', Float),
        Column('begr_inhuur', Float),
        Column('begr_vervoer', Float),
        Column('begr_beton_bvl', Float),
        Column('begr_kabelwerk', Float),
        Column('begr_grondverzet', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    if soort[0] == '1':  
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_materieel = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '2': 
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_leiding = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '3':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
         .values(begr_huisv = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '4':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
         .values(begr_overig = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '5':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_inhuur = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '6':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_vervoer = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '7':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_beton_bvl = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '8':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_kabelwerk = mprijs)  
        conn.execute(updwerk)
    elif soort[0] == '9':
        mdienstnr=(conn.execute(select([func.max(orders_inkoop_diensten.c.orddienstlevID,\
            type_=Integer).label('mdienstnr')])).scalar())
        mdienstnr += 1
        insrgl = insert(orders_inkoop_diensten).values(orddienstlevID = mdienstnr,\
             orderinkoopID = minkordnr, werknummerID = mwerknr,\
             werkomschr = soort, omschrijving = momschr, aanneemsom = mprijs,\
             plan_start = geplstart, plan_gereed = geplgereed, regel = mregel)
        conn.execute(insrgl)
        updwerk = update(werken).where(werken.c.werknummerID == mwerknr)\
        .values(begr_grondverzet = mprijs)  
        conn.execute(updwerk)
    
    conn.close
    return(check)
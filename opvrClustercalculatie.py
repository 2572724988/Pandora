from login import hoofdMenu
import os, datetime
from PyQt5.QtCore import Qt, QAbstractTableModel, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QIcon, QRegExpValidator
from PyQt5.QtWidgets import  QDialog, QLabel, QGridLayout,\
                             QPushButton, QMessageBox, QLineEdit, QWidget,\
                             QTableView, QVBoxLayout
from sqlalchemy import (Table, Column, Integer, String, Float,\
                        MetaData, create_engine, ForeignKey)
from sqlalchemy.sql import select, update, insert, and_, func

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def calcBestaatniet():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Calculatie is niet aanwezig!')
    msg.setWindowTitle('INVOEREN')
    msg.exec_()
    
def printing():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    msg.setIcon(QMessageBox.Information)
    msg.setText('Ogenblik afdrukken wordt gestart!')
    msg.setWindowTitle('AFDRUKKEN')
    msg.exec_()
     
def zoekCalculatie(m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Calculeren / Opvragen / Printen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
  
            self.Calculatie = QLabel()
            zkcalcEdit = QLineEdit()
            zkcalcEdit.setFixedWidth(100)
            zkcalcEdit.setFont(QFont("Arial",10))
            zkcalcEdit.textChanged.connect(self.zkcalcChanged)
            reg_ex = QRegExp('^[1-9]{1}[0-9]{0,8}$')
            input_validator = QRegExpValidator(reg_ex, zkcalcEdit)
            zkcalcEdit.setValidator(input_validator)  
            
            grid = QGridLayout()
            grid.setSpacing(20)
                          
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            lbl1 = QLabel('Calculatienummer')  
            lbl1.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl1, 1, 0)
            grid.addWidget(zkcalcEdit, 1, 1)
            
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2, Qt.AlignCenter)
             
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
   
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn, 3, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
    
            grid.addWidget(cancelBtn, 3, 0, 1, 1,Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
             
        def zkcalcChanged(self, text):
            self.Calculatie.setText(text)
             
        def returnCalculatie(self):
            return self.Calculatie.text()
        
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnCalculatie()]       

    window = Widget()
    data = window.getData()
    if not data[0]:
       return(0)
    elif data[0]:
        mcalnr = data[0]
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calculatie', Integer),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selcl = select([calculaties]).where(calculaties.c.calculatie == int(mcalnr))
    rpcl = con.execute(selcl).first()
    if not rpcl:
        calcBestaatniet()
        zoekCalculatie(m_email)
    elif rpcl and (not rpcl[2]):
        opbouwRp(rpcl[0], rpcl[1], rpcl[2], m_email)
    elif rpcl and rpcl[2]:
        opvragenCalc(rpcl[0], rpcl[1], rpcl[2], m_email)
    
def opvragenCalc(mcalnr, mwerkomschr,mverw, m_email):
    class MainWindow(QDialog):
        def __init__(self):
            QDialog.__init__(self)
            
            grid = QGridLayout()
            grid.setSpacing(20)
            
            self.lbl = QLabel()
            self.pixmap = QPixmap('./images/logos/verbinding.jpg')
            self.lbl.setPixmap(self.pixmap)
            grid.addWidget(self.lbl , 0, 1)
    
            self.logo = QLabel()
            self.pixmap = QPixmap('./images/logos/logo.jpg')
            self.logo.setPixmap(self.pixmap)
            grid.addWidget(self.logo , 0, 2, 1, 1, Qt.AlignRight)
              
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Calculatie: '+str(mcalnr)), 1, 1, 1, 3)
            grid.addWidget(QLabel(mwerkomschr[0:35]), 2 , 1, 1, 3)
                                   
            self.setWindowTitle("Calculatie opvragen / printen") 
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
                                                      
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved\n   dj.jansen@casema.nl'), 6, 0, 2, 3, Qt.AlignCenter)
                             
            self.printBtn = QPushButton('Calculatie\nPrinten')
            self.printBtn.clicked.connect(lambda: printCalculatie(mcalnr))
            grid.addWidget(self.printBtn, 4, 2)
            self.printBtn.setFont(QFont("Arial",10))
            self.printBtn.setFixedWidth(100)
            self.printBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.artprintBtn = QPushButton('Artikellijst\nPrinten')
            self.artprintBtn.clicked.connect(lambda: printArtikellijst(mcalnr))
            grid.addWidget(self.artprintBtn, 4, 1, 1, 1, Qt.AlignRight)
            self.artprintBtn.setFont(QFont("Arial",10))
            self.artprintBtn.setFixedWidth(100)
            self.artprintBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.toonBtn = QPushButton('Calculatie\nOpvragen')
            self.toonBtn.clicked.connect(lambda: toonCalculatie(mcalnr))
            grid.addWidget(self.toonBtn, 5, 2)
            self.toonBtn.setFont(QFont("Arial",10))
            self.toonBtn.setFixedWidth(100)
            self.toonBtn.setStyleSheet("color: black;  background-color: gainsboro")
              
            self.artlijstBtn = QPushButton('Artikellijst\nOpvragen')
            self.artlijstBtn.clicked.connect(lambda: toonArtikellijst(mcalnr))
            grid.addWidget(self.artlijstBtn,5, 1, 1, 1, Qt.AlignRight)
            self.artlijstBtn.setFont(QFont("Arial",10))
            self.artlijstBtn.setFixedWidth(100)
            self.artlijstBtn.setStyleSheet("color: black;  background-color: gainsboro")
           
            self.terugBtn = QPushButton('T\ne\nr\nu\ng')
            self.terugBtn.clicked.connect(self.close)
            grid.addWidget(self.terugBtn, 4, 1, 5, 1, Qt.AlignTop)
            self.terugBtn.setFont(QFont("Arial", 10))
            self.terugBtn.setFixedWidth(40)
            self.terugBtn.setFixedHeight(115)
            self.terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                                             
            self.setLayout(grid)
            self.setGeometry(500, 100, 150, 150)
     
    mainWin = MainWindow()
    mainWin.exec_()
    zoekCalculatie(m_email)
    
def opbouwRp(mcalnr, mwerkomschr, mverw, m_email):
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float),
        Column('calculatie', Integer),
        Column('materialen', Float))
    cluster_artikelen = Table('cluster_artikelen', metadata,
        Column('cluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelprijs', Float))
    
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selmat=select([calculaties, cluster_artikelen, artikelen]).where(and_(\
            calculaties.c.calculatie == mcalnr,\
            calculaties.c.clusterID == cluster_artikelen.c.clusterID,\
            cluster_artikelen.c.artikelID == artikelen.c.artikelID))
    rpmat = con.execute(selmat)
    for rij in rpmat:
        updcalmat = update(calculaties).where(and_(calculaties.c.calculatie ==\
           mcalnr, calculaties.c.clusterID == rij[1],\
           cluster_artikelen.c.artikelID == rij[9])).values(\
           materialen = calculaties.c.materialen+rij[2]*rij[8]*rij[10]*(1+rppar[6][1]))
        con.execute(updcalmat)
   
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('koppelnummer', Integer),
        Column('calculatie', Integer),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('uren_constr', Float),
        Column('uren_mont', Float),
        Column('uren_retourlas', Float),
        Column('uren_telecom', Float),
        Column('uren_bfi', Float),
        Column('uren_voeding', Float),
        Column('uren_bvl', Float),
        Column('uren_spoorleg', Float),
        Column('uren_spoorlas', Float),
        Column('uren_inhuur', Float),
        Column('sleuvengraver', Float),
        Column('persapparaat', Float),
        Column('atlaskraan', Float),
        Column('kraan_groot', Float),
        Column('mainliner', Float),
        Column('hormachine', Float),
        Column('wagon', Float),
        Column('locomotor', Float),
        Column('locomotief', Float),
        Column('montagewagen', Float),
        Column('stormobiel', Float),
        Column('robeltrein', Float),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
    clusters = Table('clusters', metadata,
        Column('clusterID', Integer(), primary_key=True),
        Column('omschrijving', String),
        Column('prijs', Float),
        Column('eenheid', String),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('uren_constr', Float),
        Column('uren_mont', Float),
        Column('uren_retourlas', Float),
        Column('uren_telecom', Float),
        Column('uren_bfi', Float),
        Column('uren_voeding', Float),
        Column('uren_bvl', Float),
        Column('uren_spoorleg', Float),
        Column('uren_spoorlas', Float),
        Column('uren_inhuur', Float),
        Column('sleuvengraver', Float),
        Column('persapparaat', Float),
        Column('atlaskraan', Float),
        Column('kraan_groot', Float),
        Column('mainliner', Float),
        Column('hormachine', Float),
        Column('wagon', Float),
        Column('locomotor', Float),
        Column('locomotief', Float),
        Column('montagewagen', Float),
        Column('stormobiel', Float),
        Column('robeltrein', Float))
    cluster_artikelen = Table('cluster_artikelen', metadata,
        Column('cluster_artID',Integer, primary_key=True),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('hoeveelheid', Float))
    artikelen = Table('artikelen', metadata,
        Column('artikelID', Integer(), primary_key=True),
        Column('artikelomschrijving', String),
        Column('artikelprijs', Float),
        Column('art_eenheid', String))
    materiaallijsten = Table('materiaallijsten', metadata,
        Column('matlijstID', Integer, primary_key=True),
        Column('calculatie', Integer),
        Column('hoeveelheid', Float),
        Column('artikelID', None, ForeignKey('artikelen.artikelID')),
        Column('artikelprijs', Float),
        Column('subtotaal', Float),
        Column('resterend', Float))

    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcalc = select([calculaties, clusters]).where(and_(calculaties.c\
       .calculatie == int(mcalnr), calculaties.c.clusterID == clusters.c.clusterID))
    rpcalc = con.execute(selcalc)
    selclart = select([cluster_artikelen,artikelen]).where(and_(cluster_artikelen.c.\
      artikelID == artikelen.c.artikelID, calculaties.c.clusterID ==\
      cluster_artikelen.c.clusterID, calculaties.c.calculatie == (int(mcalnr))))\
      .order_by(cluster_artikelen.c.clusterID, cluster_artikelen.c.artikelID)
    rpclart = con.execute(selclart)
    for record in rpcalc:
        updcalc = update(calculaties).where(and_(calculaties.c.calculatie == record[3],\
           calculaties.c.clusterID == clusters.c.clusterID)).values(verwerkt = 1, \
           uren_constr = calculaties.c.uren_constr+clusters.c.uren_constr*calculaties.c.hoeveelheid,\
           uren_mont = calculaties.c.uren_mont+clusters.c.uren_mont*calculaties.c.hoeveelheid,\
           uren_retourlas = calculaties.c.uren_retourlas+clusters.c.uren_retourlas*calculaties.c.hoeveelheid,\
           uren_telecom = calculaties.c.uren_telecom+clusters.c.uren_telecom*calculaties.c.hoeveelheid,\
           uren_bfi = calculaties.c.uren_bfi+clusters.c.uren_bfi*calculaties.c.hoeveelheid,\
           uren_voeding = calculaties.c.uren_voeding+clusters.c.uren_voeding*calculaties.c.hoeveelheid,\
           uren_bvl = calculaties.c.uren_bvl+clusters.c.uren_bvl*calculaties.c.hoeveelheid,\
           uren_spoorleg = calculaties.c.uren_spoorleg+clusters.c.uren_spoorleg*calculaties.c.hoeveelheid,\
           uren_spoorlas = calculaties.c.uren_spoorlas+clusters.c.uren_spoorlas*calculaties.c.hoeveelheid,\
           uren_inhuur = calculaties.c.uren_inhuur+clusters.c.uren_inhuur*calculaties.c.hoeveelheid,\
           sleuvengraver = calculaties.c.sleuvengraver+clusters.c.sleuvengraver*calculaties.c.hoeveelheid,\
           persapparaat = calculaties.c.persapparaat+clusters.c.persapparaat*calculaties.c.hoeveelheid,\
           atlaskraan = calculaties.c.atlaskraan+clusters.c.atlaskraan*calculaties.c.hoeveelheid,\
           kraan_groot = calculaties.c.kraan_groot+clusters.c.kraan_groot*calculaties.c.hoeveelheid,\
           mainliner = calculaties.c.mainliner+clusters.c.mainliner*calculaties.c.hoeveelheid,\
           hormachine = calculaties.c.hormachine+clusters.c.hormachine*calculaties.c.hoeveelheid,\
           wagon = calculaties.c.wagon+clusters.c.wagon*calculaties.c.hoeveelheid,\
           locomotor = calculaties.c.locomotor+clusters.c.locomotor*calculaties.c.hoeveelheid,\
           locomotief = calculaties.c.locomotief+clusters.c.locomotief*calculaties.c.hoeveelheid,\
           montagewagen = calculaties.c.montagewagen+clusters.c.montagewagen*calculaties.c.hoeveelheid,\
           stormobiel = calculaties.c.stormobiel+clusters.c.stormobiel*calculaties.c.hoeveelheid,\
           robeltrein = calculaties.c.robeltrein+clusters.c.robeltrein*calculaties.c.hoeveelheid,
           lonen = calculaties.c.uren_constr+clusters.c.uren_constr*rppar[8][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_mont+clusters.c.uren_mont*rppar[9][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_retourlas+clusters.c.uren_retourlas*rppar[15][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_telecom+clusters.c.uren_telecom*rppar[18][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_bfi+clusters.c.uren_bfi*rppar[10][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_voeding+clusters.c.uren_voeding*rppar[11][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_bvl+clusters.c.uren_bvl*rppar[12][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_spoorleg+clusters.c.uren_spoorleg*rppar[13][1]*calculaties.c.hoeveelheid+\
           calculaties.c.uren_spoorlas+clusters.c.uren_spoorlas*rppar[14][1]*calculaties.c.hoeveelheid,
           inhuur = calculaties.c.uren_inhuur+clusters.c.uren_inhuur*rppar[7][1]*calculaties.c.hoeveelheid,
           materieel = calculaties.c.sleuvengraver+clusters.c.sleuvengraver*rppar[19][1]*calculaties.c.hoeveelheid+\
           calculaties.c.persapparaat+clusters.c.persapparaat*rppar[20][1]*calculaties.c.hoeveelheid+\
           calculaties.c.atlaskraan+clusters.c.atlaskraan*rppar[21][1]*calculaties.c.hoeveelheid+\
           calculaties.c.kraan_groot+clusters.c.kraan_groot*rppar[22][1]*calculaties.c.hoeveelheid+\
           calculaties.c.mainliner+clusters.c.mainliner*rppar[23][1]*calculaties.c.hoeveelheid+\
           calculaties.c.hormachine+clusters.c.hormachine*rppar[24][1]*calculaties.c.hoeveelheid+
           calculaties.c.wagon+clusters.c.wagon*rppar[25][1]*calculaties.c.hoeveelheid+\
           calculaties.c.locomotor+clusters.c.locomotor*rppar[26][1]*calculaties.c.hoeveelheid+\
           calculaties.c.locomotief+clusters.c.locomotief*rppar[27][1]*calculaties.c.hoeveelheid+\
           calculaties.c.montagewagen+clusters.c.montagewagen*rppar[28][1]*calculaties.c.hoeveelheid+\
           calculaties.c.stormobiel+clusters.c.stormobiel*rppar[29][1]*calculaties.c.hoeveelheid+\
           calculaties.c.robeltrein+clusters.c.robeltrein*rppar[30][1]*calculaties.c.hoeveelheid)
        con.execute(updcalc)
        for row in rpclart:
            selart = select([materiaallijsten.c.artikelID, materiaallijsten.c.calculatie]).where(and_(materiaallijsten.\
                c.artikelID == row[1], materiaallijsten.c.calculatie == record[3]))
            rpart = con.execute(selart).first()
            if rpart:
                updmatlijst = update(materiaallijsten).where(and_(materiaallijsten.c.\
                  artikelID == row[1], materiaallijsten.c.calculatie == record[3]))\
                 .values(hoeveelheid = materiaallijsten.c.hoeveelheid+(record[5]*row[3]),\
                artikelprijs = row[6]*(1+rppar[6][1]), subtotaal = materiaallijsten.\
                c.subtotaal+record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(updmatlijst)
            elif not rpart:
                mmatlijstnr = (con.execute(select([func.max(materiaallijsten.c.matlijstID,\
                        type_=Integer).label('mmatlijstnr')])).scalar())
                mmatlijstnr += 1
                insmatlijst = insert(materiaallijsten).values(matlijstID = mmatlijstnr,\
                    calculatie = record[3], artikelID = row[1],\
                    hoeveelheid = record[5]*row[3], resterend = record[5]*row[3],\
                    artikelprijs = row[6]*(1+rppar[6][1]),\
                    subtotaal = record[5]*row[3]*row[6]*(1+rppar[6][1]))
                con.execute(insmatlijst)
        selber = select([calculaties.c.calcID, calculaties.c.calculatie])\
                           .where(calculaties.c.calculatie == mcalnr)
        rpselber = con.execute(selber)
        for regel in rpselber:
            updber = update(calculaties).where(calculaties.c.calculatie==mcalnr)\
             .values(prijs=calculaties.c.materialen+calculaties.c.materieel+\
              calculaties.c.lonen+calculaties.c.diensten+calculaties.c.inhuur,\
              werkomschrijving = mwerkomschr)
            con.execute(updber)
    opvragenCalc(mcalnr, mwerkomschr, mverw, m_email)
                        
def printCalculatie(mcalnr):
    from sys import platform
    metadata = MetaData()
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('koppelnummer', Integer),
        Column('calculatie', Integer),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('werkomschrijving', String))
    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpcal = con.execute(selcal)
    
    mblad = 1
    rgl = 0
    mmat = 0
    mlon = 0
    mmater = 0
    minh = 0
    mtotaal = 0
    for row in rpcal:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename = '.\\forms\\Extern_Clustercalculaties\\clustercalculatie-'+str(row[3])+'-'+str(row[2])+'.txt'
            else:
                filename = './forms/Extern_Clustercalculaties/clustercalculatie-'+str(row[3])+'-'+str(row[2])+'.txt'
            kop=\
    ('Werknummer: '+ str(row[2])+' '+'{:<24s}'.format(str(row[13]))+'  Calculatie: '+str(row[3])+'  Datum: '+str(datetime.datetime.now())[0:10]+'  Blad : '+str(mblad)+'\n'+
    '=====================================================================================================\n'+
    'Cluster  Omschrijving        Eenheid Aantal  Materialen      Lonen  Materieel     Inhuur     Bedrag  \n'+
    '=====================================================================================================\n')
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<9s}'.format(row[1])+'{:<22.21s}'.format(row[4])+'{:<6s}'.format(row[6])+'{:5.2f}'.format(row[5])+'  '+'{:11.2f}'.format(row[8])+'{:11.2f}'.format(row[9])+'{:11.2f}'.format(row[11])+'{:11.2f}'.format(row[12])+'{:12.2f}'.format(row[7])+'\n')
        mmat = mmat+row[8]
        mlon = mlon+row[9]
        mmater = mmater+row[11]
        minh = minh+row[12]
        mtotaal = mtotaal+row[7]
        rgl += 1
    tail =(\
    '-------------------------------------------------------------------------------------------------------\n'+
    'Totalen                                     '+'{:11.2f}'.format(mmat)+'{:11.2f}'.format(mlon)+'{:11.2f}'.format(mmater)+'{:11.2f}'.format(minh)+'{:12.2f}'.format(mtotaal)+'\n'
    '=======================================================================================================\n')    
    open(filename,'a').write(tail)
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()
                     
def printArtikellijst(mcalnr):
    from sys import platform
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('calculatie', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('subtotaal', Float))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('art_eenheid', String),
         Column('locatie_magazijn', String))
    calculaties = Table('calculaties', metadata,
        Column('calculatie', Integer),
        Column('koppelnummer', Integer))
                                    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selmat = select([materiaallijsten, artikelen])\
      .where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.artikelID == artikelen.c.artikelID,\
      materiaallijsten.c.calculatie == mcalnr)).order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)
    selkop = select([calculaties]).where(calculaties.c.calculatie == mcalnr)
    rpkop = con.execute(selkop).first()
    mblad = 1
    rgl = 0
    for row in rpmat:
        if rgl == 0 or rgl%57 == 0:
            if platform == 'win32':
                filename =  filename = '.\\forms\\Extern_Clustercalculaties\\materiaallijst-'+str(rpkop[0])+'-'+str(rpkop[1])+'.txt'
            else:
                filename =  filename = './forms/Extern_Clustercalculaties/materiaallijst-'+str(rpkop[0])+'-'+str(rpkop[1])+'.txt'
            kop=\
    ('Werknummer:   '+ str(rpkop[1])+'  Calculatie: '+str(rpkop[0])+'   Datum: '+str(datetime.datetime.now())[0:10]+'  Blad :  '+str(mblad)+'\n'+
    '=============================================================================================\n'+
    'Artikelnr  Omschrijving                        Eenheid       Prijs      Aantal               \n'+
    '=============================================================================================\n')
            if rgl == 0:
                open(filename, 'w').write(kop)
            elif rgl%57 == 0:
                open(filename, 'a').write(kop)
            mblad += 1
            
        open(filename,'a').write('{:<11d}'.format(row[6])+'{:<37.35s}'.format(row[7])+'{:<8.6s}'.format(row[8])+'{:10.2f}'.format(row[3])+'  '+'{:10.2f}'.format(row[4])+'\n')
        rgl += 1
    if platform == 'win32':
        os.startfile(filename, "print")
    else:
        os.system("lpr "+filename)
    printing()

def toonCalculatie(mcalnr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(50, 50, 1500, 900)
            self.setWindowTitle('Clustercalculatie')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                              Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.hideColumn(1)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(ShowSelection)
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
            return str(self.mylist[index.row()][index.column()])
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
             
    header = ['ID','Calculatie','Clusternr', 'Omschrijving','Hoeveelheid',\
              'Eenheid', 'Koppelnr', 'Totaalprijs','Materialen', 'Lonen',\
              'Diensten','Materieel', 'Inhuur','Uren\nConstruktie','Uren\nMontage',\
              'Uren\nRetourlas', 'Uren\nTelecom', 'Uren\nBFI','Uren\nVoeding',\
              'Uren\nBovenleiding','Uren\nSpoorleg','Uren\nSpoorlas','Uren\nInhuur',\
              'Uren\nSleuvengraver','Uren\nPersapparaat', 'Uren\nAtlaskraan',\
              'Uren\nKraan_groot','Uren\nMainliner','Uren\nHormachine','Uren\nWagon',\
              'Uren\nLocomotor','Uren\nLocomotief','Uren\nMontagewagen',\
              'Uren\nStormobiel','Uren\nRobeltrein','Werkomschrijving','Verwerkt']

    metadata = MetaData()               
    calculaties = Table('calculaties', metadata,
        Column('calcID', Integer(), primary_key=True),
        Column('calculatie', Integer),
        Column('clusterID', None, ForeignKey('clusters.clusterID')),
        Column('omschrijving', String),
        Column('hoeveelheid', Float),
        Column('eenheid', String),
        Column('koppelnummer', Integer),
        Column('prijs', Float),
        Column('materialen', Float),
        Column('lonen', Float),
        Column('diensten', Float),
        Column('materieel', Float),
        Column('inhuur', Float),
        Column('uren_constr', Float),
        Column('uren_mont', Float),
        Column('uren_retourlas', Float),
        Column('uren_telecom', Float),
        Column('uren_bfi', Float),
        Column('uren_voeding', Float),
        Column('uren_bvl', Float),
        Column('uren_inhuur', Float),
        Column('uren_spoorleg', Float),
        Column('uren_spoorlas', Float),
        Column('uren_inhuur', Float),
        Column('sleuvengraver', Float),
        Column('persapparaat', Float),
        Column('atlaskraan', Float),
        Column('kraan_groot', Float),
        Column('mainliner', Float),
        Column('hormachine', Float),
        Column('wagon', Float),
        Column('locomotor', Float),
        Column('locomotief', Float),
        Column('montagewagen', Float),
        Column('stormobiel', Float),
        Column('robeltrein', Float),
        Column('werkomschrijving', String),
        Column('verwerkt', Integer))
                                               
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selcal = select([calculaties]).where(calculaties.c.calculatie == mcalnr).\
     order_by(calculaties.c.clusterID)
    rpcal = con.execute(selcal)
      
    data_list=[]
    for row in rpcal:
        data_list += [(row)]
        
    def ShowSelection(idx):
        mcalnr = idx.data()
        if  idx.column() == 0:

            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
            selcal = select([calculaties]).where(calculaties.c.calcID == mcalnr)
            rpcal = con.execute(selcal).first()
            
            header = ['ID','Calculatie','Clusternr', 'Omschrijving','Hoeveelheid',\
                      'Eenheid', 'Koppelnr', 'Totaalprijs','Materialen', 'Lonen',\
                      'Diensten','Materieel', 'Inhuur','Uren\nConstruktie','Uren\nMontage',\
                      'Uren\nRetourlas', 'Uren\nTelecom', 'Uren\nBFI','Uren\nVoeding',\
                      'Uren\nBovenleiding','Uren\nSpoorleg','Uren\nSpoorlas','Uren\nInhuur',\
                      'Uren\nSleuvengraver','Uren\nPersapparaat', 'Uren\nAtlaskraan',\
                      'Uren\nKraan_groot','Uren\nMainliner','Uren\nHormachine','Uren\nWagon',\
                      'Uren\nLocomotor','Uren\nLocomotief','Uren\nMontagewagen',\
                      'Uren\nStormobiel','Uren\nRobeltrein','Werkomschrijving', 'Verwerkt']
                              
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Opvragen Clustercalculatie")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Opvragen Clustercalculatie'),0, 2, 1, 3)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 5, 1, 1, Qt.AlignRight)                
                    index = 3
                    for item in header:
                        horpos = index%3
                        verpos = index
                        if index%3 == 1:
                            verpos = index - 1
                        elif index%3 == 2:
                            verpos = index -2
                        self.lbl = QLabel('{:15}'.format(header[index-3]))
                        
                        self.Gegevens = QLabel()
                        q1Edit = QLineEdit('{:30}'.format(str(rpcal[index-3])))
                        q1Edit.setFixedWidth(300)
                        q1Edit.setDisabled(True)
                        grid.addWidget(self.lbl, verpos, horpos+horpos%3)
                        grid.addWidget(q1Edit, verpos, horpos+horpos%3+1)
                        
                        index +=1
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, verpos+1, 5, 1 , 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100) 
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), verpos+2, 2, 1, 2)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(100, 100, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
            mainWin.raise_()
            mainWin.activateWindow()
            
    win = MyWindow(data_list, header)
    win.exec_()
            
def toonArtikellijst(mcalnr):
    class MyWindow(QDialog):
        def __init__(self, data_list, header, *args):
            QWidget.__init__(self, *args,)
            self.setGeometry(100, 50, 1200, 900)
            self.setWindowTitle('Materiaallijst')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
            self.setWindowFlags(self.windowFlags()| Qt.WindowSystemMenuHint |
                                                    Qt.WindowMinMaxButtonsHint)
            table_model = MyTableModel(self, data_list, header)
            table_view = QTableView()
            table_view.setModel(table_model)
            font = QFont("Arial", 10)
            table_view.setFont(font)
            table_view.setColumnHidden(6, True)
            table_view.resizeColumnsToContents()
            table_view.setSelectionBehavior(QTableView.SelectRows)
            #table_view.clicked.connect(selectRow)
            table_view.clicked.connect(showSelart)
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
            return str(self.mylist[index.row()][index.column()])
        def headerData(self, col, orientation, role):
            if orientation == Qt.Horizontal and role == Qt.DisplayRole:
                return self.header[col]
            return None
              
    header = ['Artikelnr','Omschrijving','Reserveringsaldo','LijstID','Calculatie',\
              'Werknummer','Orderinkoopnummer', 'Artikelnr','ArtikelPrijs',\
              'Hoeveelheid','Afroep','Resterend','Subtotaal','Reserveringdatum',\
              'Levering eind','Levering begin','Categorie']
                   
    metadata = MetaData()
    materiaallijsten = Table('materiaallijsten', metadata,
         Column('matlijstID', Integer, primary_key=True),
         Column('calculatie', Integer),
         Column('werknummerID', Integer),
         Column('orderinkoopID', Integer),
         Column('artikelID', None, ForeignKey('artikelen.artikelID')),
         Column('artikelprijs', Float),
         Column('hoeveelheid', Float),
         Column('afroep', Float),
         Column('resterend', Float),
         Column('subtotaal', Float),
         Column('reserverings_datum', String),
         Column('levertijd_end', String),
         Column('levertijd_begin', String),
         Column('categorie', Integer))
    artikelen = Table('artikelen', metadata,
         Column('artikelID', Integer(), primary_key=True),
         Column('artikelomschrijving', String),
         Column('reserveringsaldo', Float))
                                    
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    
    selmat = select([artikelen,materiaallijsten]).where(and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
         materiaallijsten.c.artikelID == artikelen.c.artikelID,\
         materiaallijsten.c.calculatie == mcalnr))\
         .order_by(materiaallijsten.c.artikelID)
    rpmat = con.execute(selmat)
    
    data_list=[]
    for row in rpmat:
        data_list += [(row)]
        
    def showSelart(idx):
        martnr = idx.data()
        if idx.column() == 0:
            engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
            con = engine.connect()
                
            selmat = select([artikelen, materiaallijsten]).where(\
                 and_(materiaallijsten.c.artikelID == artikelen.c.artikelID,\
                 materiaallijsten.c.artikelID == int(martnr),\
                 materiaallijsten.c.calculatie == mcalnr))\
                 .order_by(materiaallijsten.c.artikelID)
            rpmat = con.execute(selmat).first()
             
            header = ['Artikelnr','Omschrijving','Reserveringsaldo','LijstID','Calculatie',\
              'Werknummer','Orderinkoopnummer', 'Artikelnr','ArtikelPrijs',\
              'Hoeveelheid','Afroep','Resterend','Subtotaal','Reserveringdatum',\
              'Levering eind','Levering begin', 'Categorie']
 
            class MainWindow(QDialog):
                def __init__(self):
                    QDialog.__init__(self)
                    
                    grid = QGridLayout()
                    grid.setSpacing(20)
                    
                    self.setWindowTitle("Opvragen Artikelen Clustercalculatie")
                    self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                    
                    self.setFont(QFont('Arial', 10))   
                                                      
                    self.lbl = QLabel()
                    self.pixmap = QPixmap('./images/logos/verbinding.jpg')
                    self.lbl.setPixmap(self.pixmap)
                    grid.addWidget(self.lbl , 0, 0)
                    
                    grid.addWidget(QLabel('Opvragen Artikelen Calculatie'),0, 1, 1, 2)
            
                    self.logo = QLabel()
                    self.pixmap = QPixmap('./images/logos/logo.jpg')
                    self.logo.setPixmap(self.pixmap)
                    grid.addWidget(self.logo , 0, 3, 1, 1, Qt.AlignRight)                
                    index = 1
                    for item in header:
                        self.lbl = QLabel('{:15}'.format(header[index-1]))
                        self.Gegevens = QLabel()
                        if index == 1:
                            q1Edit = QLineEdit('{:10}'.format(str(rpmat[index-1])))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, 1, 0)
                            grid.addWidget(q1Edit, index, 1, 1, 2)
                        elif index == 2:
                            q1Edit = QLineEdit('{:40}'.format(str(rpmat[index-1])))
                            q1Edit.setFixedWidth(400)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, 2, 0)
                            grid.addWidget(q1Edit, index, 1, 1, 3)
                        elif index%2 == 0:
                            q1Edit = QLineEdit('{:10}'.format(str(rpmat[index-1])))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, index, 0)
                            grid.addWidget(q1Edit, index, 1)
                        else:
                            q1Edit = QLineEdit('{:10}'.format(str(rpmat[index-1])))
                            q1Edit.setFixedWidth(100)
                            q1Edit.setDisabled(True)
                            grid.addWidget(self.lbl, index+1, 2)
                            grid.addWidget(q1Edit, index+1, 3)
                        index += 1
                        
                    terugBtn = QPushButton('Sluiten')
                    terugBtn.clicked.connect(self.accept)
            
                    grid.addWidget(terugBtn, index+1, 3, 1, 1, Qt.AlignRight)
                    terugBtn.setFont(QFont("Arial",10))
                    terugBtn.setFixedWidth(100)
                    terugBtn.setStyleSheet("color: black;  background-color: gainsboro")
                    
                    grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), index+2, 0, 1, 4, Qt.AlignCenter)
                                                                            
                    self.setLayout(grid)
                    self.setGeometry(400, 200, 150, 150)
                            
            mainWin = MainWindow()
            mainWin.exec_()
            
    win = MyWindow(data_list, header)
    win.exec_()   
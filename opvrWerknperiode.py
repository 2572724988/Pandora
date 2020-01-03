from login import hoofdMenu
from PyQt5.QtWidgets import QLabel, QLineEdit, QGridLayout, QPushButton,\
               QDialog, QMessageBox
from PyQt5.QtGui import QRegExpValidator, QFont, QPixmap, QIcon
from PyQt5.QtCore import Qt, QRegExp
from sqlalchemy import (Table, Column, Integer, String, Float, Boolean,\
                        ForeignKey,  MetaData, create_engine)
from sqlalchemy.sql import select, and_

def geenBetaalgeg():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen betaalgegevens voor\ndeze periode gevonden!')
    msg.setWindowTitle('Werknemers periodegegevens opvragen')
    msg.exec_()
    
def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def ongInvoer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Foutieve invoer\nzoekterm opnieuw invoeren s.v.p.!')
    msg.setWindowTitle('Werknemers periodegegevens opvragen')               
    msg.exec_() 

def geenRecord():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen urenmutaties van deze persoon gevonden\nin deze periode maak een andere selektie s.v.p.!')
    msg.setWindowTitle('Werknemers periodegegevens opvragen')               
    msg.exec_() 
    
def foutWerknemer():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Werknemer niet gevonden\nen/of geen geldige periode opgegeven!')
    msg.setWindowTitle('Werknemers periodegegevens opvragen')
    msg.exec_()
               
def _11check(minput):
    number = str(minput)
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
    
def zoekWerknemer(m_email):     
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle('Periodegegevens opvragen')
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
    
            self.setFont(QFont('Arial', 10))
    
            self.Werknemer = QLabel()
            werknemerEdit = QLineEdit()
            werknemerEdit.setFixedWidth(100)
            werknemerEdit.setFont(QFont("Arial",10))
            werknemerEdit.textChanged.connect(self.werknemerChanged)
            reg_ex = QRegExp('^[1]{1}[0-9]{8}$')
            input_validator = QRegExpValidator(reg_ex, werknemerEdit)
            werknemerEdit.setValidator(input_validator)
            
            self.Betaalperiode = QLabel()
            betEdit = QLineEdit()
            betEdit.setFixedWidth(100)
            betEdit.setFont(QFont("Arial",10))
            betEdit.textChanged.connect(self.betChanged)
            reg_ex = QRegExp('^[2]{1}[01]{1}[0-9]{2}[-][0-1]{1}[0-9]{1}$')
            input_validator = QRegExpValidator(reg_ex, betEdit)
            betEdit.setValidator(input_validator)
                            
            grid = QGridLayout()
            grid.setSpacing(20)
    
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl , 0, 0, 1, 2)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 0, 1, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
     
            grid.addWidget(QLabel('Account-werknemer'), 1, 0)
            grid.addWidget(werknemerEdit, 1, 1)
            
            grid.addWidget(QLabel('Betaalperiode jjjj-mm'), 2, 0)
            grid.addWidget(betEdit, 2, 1)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 4, 0, 1, 2)
              
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email))
         
            applyBtn = QPushButton('Zoeken')
            applyBtn.clicked.connect(self.accept)
                  
            grid.addWidget(applyBtn, 3, 1)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro")
         
            grid.addWidget(cancelBtn, 3, 0, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
            
            self.setLayout(grid)
            self.setGeometry(400, 300, 150, 150)
    
        def werknemerChanged(self, text):
            self.Werknemer.setText(text)
            
        def betChanged(self, text):
            self.Betaalperiode.setText(text)
    
        def returnWerknemer(self):
            return self.Werknemer.text()
        
        def returnBetaalperiode(self):
            return self.Betaalperiode.text()
    
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnWerknemer(), dialog.returnBetaalperiode()]
       
    window = Widget()
    data = window.getData()
    if data[0]:
        maccountnr = data[0]
    else:
        foutWerknemer()
        zoekWerknemer(m_email)
    if data[1]:
        mbetaalper = data[1]
    else:
        mbetaalper = '2000-01'
               
    metadata = MetaData()

    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')))
   
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([werknemers]).where(werknemers.c.accountID == maccountnr)
    rpwerkn = conn.execute(sel).first()
     
    if (len(str(maccountnr)) == 9 and _11check(maccountnr) and rpwerkn)\
          and (len(mbetaalper) == 7):
        maccountnr = rpwerkn[1]
        mwerknmrnr = rpwerkn[0]
        opvrWerknperiode(mwerknmrnr,mbetaalper, m_email)
    else:
        foutWerknemer()
        zoekWerknemer(m_email)

def opvrWerknperiode(mwerknmrnr,mbetaalper, m_email):
    mbegin = str(mbetaalper[0:8]+'-'+'01')
    mtot = str(mbetaalper[0:8]+'-'+'31')
    midx = int(mbetaalper[5:7])
    mbet = ['Januari','Februari',' Maart', 'April', 'Mei', 'Juni', 'Juli',\
                'Augustus','September', 'Oktober', 'November', 'December']
    mbetmaand = str(mbet[midx-1])
    mbetjr = str(mbetaalper[0:4])

    metadata = MetaData()   
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')), 
        Column('loontrede', Integer),
        Column('reiskosten_vergoeding', Float),
        Column('loonheffing', Float),
        Column('pensioenpremie', Float),
        Column('reservering_vakantietoeslag', Float),
        Column('werkgevers_pensioenpremie', Float),
        Column('periodieke_uitkeringen', Float),
        Column('overige_inhoudingen', Float),
        Column('overige_vergoedingen', Float),
        Column('bedrijfsauto', Float),
        Column('indienst', String),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float)) 
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('reisuur', Float),
        Column('maandloon', Float)) 
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('soort', String),
        Column('meerwerkstatus', Boolean),
        Column('bruto_loonbedrag', Float))
    accounts = Table('accounts', metadata,
        Column('accountID', Integer, primary_key=True),
        Column('voornaam', String),
        Column('achternaam', String),
        Column('geboortedatum', String))
         
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    conn = engine.connect()
    sel = select([werknemers, lonen, wrkwnrln, accounts]).where(and_\
      (werknemers.c.werknemerID == mwerknmrnr, werknemers.c.loonID ==\
       lonen.c.loonID, accounts.c.accountID == werknemers.c.accountID))
    rpwerkn = conn.execute(sel).first()
    mwerknmrnr = rpwerkn[0]
    maccountnr = rpwerkn[1]
    mloonnr = rpwerkn[2]
    mtrede = rpwerkn[3]*0.03
    mreisk = float(rpwerkn[4])
   
    #mloonh = (uurloon*40*13)/3 #tabelloon.loonheffing
    if rpwerkn[2] < 37:
        mbruto = rpwerkn[17]*520/3*(1+mtrede)
        muurl = rpwerkn[17]*(1+mtrede)
    else:
        mbruto =  rpwerkn[19]*(1+mtrede)
        muurl = mbruto*3/520
    #loonheffing pensioenpremie
    metadata =  MetaData()
    params = Table('params', metadata,
        Column('paramID', Integer, primary_key=True),
        Column('tarief', Float),
        Column('item', String),
        Column('lock', Boolean),
        Column('ondergrens', Float),
        Column('bovengrens', Float))
        
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selpar = select([params]).order_by(params.c.paramID)
    rppar = con.execute(selpar).fetchall()
    
    mauto = rpwerkn[12]*12
     #pensioenpremie
    if rpwerkn[2] < 37:
        mbruto = rpwerkn[17]*520/3*(1+mtrede)
        muurl = rpwerkn[17]*(1+mtrede)
    else:
        mbruto =  rpwerkn[2]*(1+mtrede)
        muurl = mbruto*3/520
    
    mjaarink = mbruto*12.96
    mpensink = mjaarink
    if mpensink >  rppar[44][5]:
        mpensprjr = (rppar[44][5]-rppar[44][4])*rppar[44][1]
    else:
        mpensprjr = (mpensink-rppar[44][4])*rppar[44][1]
    mpenspr = (mpensprjr)/12.96/3
    mpensprwg = mpenspr*2
    mresvak = mbruto*.08
    mbelink = mjaarink-mpensprjr+(mauto*12)

    mwerkg_WAO_IVA_WGA = rppar[69][1]*mjaarink/12.96
    mwerkg_AWF = rppar[70][1]*mjaarink/12.96 
    mwerkg_ZVW = rppar[71][1]*mjaarink/12.96
    # Bijzonder tarief bepalen
    if mbelink > 0 and mbelink <= 6512:
        mbyz = 0.3655
    elif mbelink > 6512 and mbelink <= 10226:
        mbyz = 0.3479
    elif mbelink > 10226 and mbelink <=18937:
        mbyz = 0.0849
    elif mbelink > 18937 and mbelink <= 20143:
        mbyz = 0.3655
    elif mbelink > 20143 and mbelink <= 22029:
        mbyz = 0.4553
    elif mbelink > 22029 and  mbelink <= 33113:
        mbyz = 0.4553
    elif mbelink > 33113 and mbelink <= 33995:
        mbyz = 0.4913
    elif mbelink > 33995 and mbelink <= 34405:
        mbyz = 0.4913
    elif mbelink > 34405 and mbelink <= 68508:
        mbyz = 0.4913
    elif mbelink > 68508 and mbelink <= 133232:
        mbyz = 0.5555
    elif mbelink > 133232:
        mbyz = 0.5195

    mloonh = rpwerkn[5]
    mbyztar = mbyz*100
    #mwerkglasten = float(rpwerkn[8])
    mperiodiek = float(rpwerkn[9])
    moverig = float(rpwerkn[10])
    mindienst = rpwerkn[13]
    mverlofsaldo = rpwerkn[14]
    mextraverlof = rpwerkn[15]
    mvoorn = rpwerkn[28]
    machtern = rpwerkn[29]
    mgeboren = str(rpwerkn[30])[8:10]+str(rpwerkn[30])[4:7]+'-'+str(rpwerkn[30])[0:4]
   
    if rpwerkn[18]:
        mreisuurl = round(rpwerkn[18],2)
    else:
        mreisuurl = 0

    selwrkwnrln = select([wrkwnrln]).where(and_(wrkwnrln.c.werknemerID == mwerknmrnr,\
     werknemers.c.werknemerID == wrkwnrln.c.werknemerID,\
     (wrkwnrln.c.boekdatum >= mbegin), (wrkwnrln.c.boekdatum <= mtot)))
    if conn.execute(selwrkwnrln).fetchone():
        rpwrkwnrln = conn.execute(selwrkwnrln)
    else:
        geenRecord()
        zoekWerknemer(m_email)
    mreisuren = 0
    muren = 0
    muren125 = 0
    muren150 = 0
    muren200 = 0
    mverlof = 0
    mziek = 0
    mfeest = 0
    mdokter = 0
    mgverzuim = 0
    moverzuim = 0
    muurlbedr = 0
    muurl125bedr = 0
    muurl150bedr = 0
    muurl200bedr = 0
    mreisbedr = 0
    mverlofbedr = 0
    mziekbedr = 0
    mfeestbedr = 0
    mdokterbedr = 0
    mgverzuimbedr = 0
    moverzuimbedr = 0
    for row in rpwrkwnrln:
        if row[4] == 'Reis':
            mreisuren = mreisuren + float(row[3])
        if row[4] == '100%':
            muren = muren + float(row[3])
        if row[4] == '125%':
            muren125 = muren125 + float(row[3])
        if row[4] == '150%':
            muren150 = muren150 + float(row[3])
        if row[4] == '200%':
            muren200 = muren200 + float(row[3])
        if row[4] == 'Verlof':
            mverlof = mverlof + float(row[3])
        if row[4] == 'Extra verlof':
            mextraverlof = mextraverlof + float(row[3])
        if row[4] == 'Ziekte':
            mziek = mziek + float(row[3])
        if row[4] == 'Feestdag':
            mfeest = mfeest + float(row[3])
        if row[4] == 'Dokter':
            mdokter = mdokter + float(row[3])
        if row[4] == 'Geoorl. Verzuim':
            mgverzuim = mgverzuim + float(row[3])
        if row[4] == 'Ong. Verzuim':
            moverzuim = moverzuim + float(row[3])
            
        mreisuurl = rpwerkn[18]
        muurl = (rpwerkn[17]+rpwerkn[17]/100*row[3])
            
        mreisbedr = round(float(str(mreisuren*mreisuurl)),2)
        muurlbedr = round(float(str(muren*muurl)),2)
        muurl125bedr = round(float(str(muren125*muurl*1.25)),2)
        muurl150bedr = round(float(str(muren150*muurl*1.5)),2)
        muurl200bedr = round(float(str(muren200*muurl*2)),2)
        mverlofbedr =  round(float(str(mverlof*muurl)),2)
        mziekbedr = round(float(str(mziek*muurl)),2)
        mfeestbedr = round(float(str(mfeest*muurl)),2)
        mdokterbedr = round(float(str(mdokter*muurl)),2)
        mgverzuimbedr = round(float(str(mgverzuim*muurl)),2)
        moverzuimbedr = round(float(str(moverzuim*muurl)),2)
                                       
    class Widget(QDialog):
         def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Werknemerperiodegegevens opvragen")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg')) 
                                  
            self.setFont(QFont('Arial', 10))
                
            self.Accountnummer = QLabel()
            q2Edit = QLineEdit(str(maccountnr))
            q2Edit.setFixedWidth(90)
            q2Edit.setDisabled(True)
            q2Edit.setFont(QFont("Arial",10))
            q2Edit.setDisabled(True)
                        
            self.Loontabelnummer = QLabel()
            q4Edit = QLineEdit(str(mloonnr))
            q4Edit.setFixedWidth(30)
            q4Edit.setFont(QFont("Arial",10))
            q4Edit.setDisabled(True)
            
            self.Loontrede = QLabel()
            q5Edit = QLineEdit(str(int(mtrede/0.03)))
            q5Edit.setFixedWidth(30)
            q5Edit.setFont(QFont("Arial",10))
            q5Edit.setDisabled(True)
           
            self.Loonheffing = QLabel()
            q6Edit = QLineEdit(str(round(mloonh,2)))
            q6Edit.setFixedWidth(100)
            q6Edit.setFont(QFont("Arial",10))
            q6Edit.setDisabled(True)
                              
            self.Reiskostenvergoeding = QLabel()
            q8Edit = QLineEdit(str(mreisk))
            q8Edit.setFixedWidth(100)
            q8Edit.setFont(QFont("Arial",10))
            q8Edit.setDisabled(True)
       
            self.Pensioen = QLabel()
            q9Edit = QLineEdit(str(round(mpenspr,2)))
            q9Edit.setFixedWidth(70)
            q9Edit.setFont(QFont("Arial",10))
            q9Edit.setDisabled(True)
            
            self.Reserveringvakantie = QLabel()
            q10Edit = QLineEdit(str(round(mresvak,2)))
            q10Edit.setFixedWidth(100)
            q10Edit.setDisabled(True)
               
            self.Werkgeverpensioenpremie = QLabel()
            q11Edit = QLineEdit(str(round( mpensprwg,2)))
            q11Edit.setFixedWidth(100)
            q11Edit.setFont(QFont("Arial",10))
            q11Edit.setDisabled(True)
            
            self.Auto = QLabel()
            q18Edit = QLineEdit(str(round(mauto/12,2)))
            q18Edit.setFixedWidth(70)
            q18Edit.setFont(QFont("Arial",10))
            q18Edit.setDisabled(True)
             
            self.Periodiekeuitkering = QLabel()
            q12Edit = QLineEdit(str(mperiodiek))
            q12Edit.setFixedWidth(100)
            q12Edit.setFont(QFont("Arial",10))
            q12Edit.setDisabled(True)
            
            self.Overigeinhoudingen = QLabel()
            q13Edit = QLineEdit(str(moverig))
            q13Edit.setFixedWidth(100)
            q13Edit.setFont(QFont("Arial",10))
            q13Edit.setDisabled(True)
  
            self.Overigevergoedingen = QLabel()
            q19Edit = QLineEdit(str(moverig))
            q19Edit.setFixedWidth(100)
            q19Edit.setFont(QFont("Arial",10))
            q19Edit.setDisabled(True)
    
            self.Indienst = QLabel()
            q14Edit = QLineEdit(mindienst)
            q14Edit.setFixedWidth(100)
            q14Edit.setFont(QFont("Arial",10))
            q14Edit.setDisabled(True)
                        
            self.Brutoloon = QLabel()
            q15Edit = QLineEdit(str(round(mbruto,2)))
            q15Edit.setDisabled(True)
            q15Edit.setFixedWidth(100)
            q15Edit.setFont(QFont("Arial",10))
                        
            self.Verlofsaldo = QLabel()
            q16Edit = QLineEdit(str(mverlofsaldo))
            q16Edit.setDisabled(True)
            q16Edit.setFixedWidth(100)
            q16Edit.setFont(QFont("Arial",10))
            
            self.ExtraVerlof = QLabel()
            q17Edit = QLineEdit(str(mextraverlof))
            q17Edit.setFixedWidth(100)
            q17Edit.setFont(QFont("Arial",10))
            q17Edit.setDisabled(True)
             
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,1 , 0)
            
            logo = QLabel()
            pixmap = QPixmap('./images/logos/logo.jpg')
            logo.setPixmap(pixmap)
            grid.addWidget(logo , 1, 3, 1, 1, Qt.AlignRight)
    
            self.setFont(QFont('Arial', 10))
            grid.addWidget(QLabel('Opvragen werknemergegevens van\n'+mvoorn+\
                ' '+machtern+'\nGeboren: '+mgeboren), 1, 1, 1, 3)
            
            grid.addWidget(QLabel('Bruto maandloon'), 3, 2)
            grid.addWidget(q15Edit, 3, 3) 
                                                
            grid.addWidget(QLabel('Accountnummer'), 3, 0)
            grid.addWidget(q2Edit, 3, 1)
            
            grid.addWidget(QLabel('Loontabel'), 7, 0)
            grid.addWidget(q4Edit, 7 , 1) 
             
            grid.addWidget(QLabel('Loontrede'), 8, 0)
            grid.addWidget(q5Edit, 8, 1)
                            
            grid.addWidget(QLabel('Loonheffing'), 4, 2)
            grid.addWidget(q6Edit, 4, 3)
                          
            grid.addWidget(QLabel('Reiskostenvergoeding'), 6, 0)
            grid.addWidget(q8Edit, 6, 1)
             
            grid.addWidget(QLabel('Pensioenafdracht'), 5, 2)
            grid.addWidget(q9Edit, 5, 3)
            
            grid.addWidget(QLabel('Reservering vakantiegeld      '), 5, 0)
            grid.addWidget(q10Edit, 5, 1)  
     
            grid.addWidget(QLabel('Werkgeversdeel pensioenpremie'), 6, 2)
            grid.addWidget(q11Edit, 6, 3)
                   
            grid.addWidget(QLabel('Periodieke uitkering belast'), 4, 0)
            grid.addWidget(q12Edit, 4, 1) 
            
            grid.addWidget(QLabel('Overige inhoudingen onbelast'), 7, 2)
            grid.addWidget(q13Edit, 7, 3) 
            
            grid.addWidget(QLabel('Bijtelling Bedrijfsauto'), 8, 2)
            grid.addWidget(q18Edit, 8, 3) 
            
            grid.addWidget(QLabel('Werkgeversdeel Arbeidsongeschiktheid'), 9, 2)
            grid.addWidget(QLabel(str(round(mwerkg_WAO_IVA_WGA,2))), 9, 3)
            grid.addWidget(QLabel('Werkgeversdeel Werkloosheidswet'), 10, 2)
            grid.addWidget(QLabel(str(round(mwerkg_AWF, 2))), 10,3)
            grid.addWidget(QLabel('Werkgeversdeel Zorgverzekering'), 11, 2)
            grid.addWidget(QLabel(str(round(mwerkg_ZVW,2))), 11, 3)
            grid.addWidget(QLabel('Bijzonder tarief   % '), 12, 2)
            grid.addWidget(QLabel(str(round(mbyztar, 2))), 12,3)
            
            grid.addWidget(QLabel('Overige Vergoedingen onbelast'), 11, 0)
            grid.addWidget(q19Edit, 11, 1) 
       
            grid.addWidget(QLabel('Datum indiensttreding'), 12, 0)
            grid.addWidget(q14Edit, 12, 1) 
            
            grid.addWidget(QLabel('Verlofsaldo in uren'), 9, 0)
            grid.addWidget(q16Edit, 9, 1)
            
            grid.addWidget(QLabel('Extra verlof in uren'), 10, 0)
            grid.addWidget(q17Edit, 10, 1)
            
            grid.addWidget(QLabel('Uurloon'), 21, 0)
            grid.addWidget(QLabel(str(round(muurl, 2))), 21, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Reisuurloon'), 21, 2)
            grid.addWidget(QLabel(str(round(mreisuurl, 2))), 21, 3, 1 ,1, Qt.AlignRight)
            
            grid.addWidget(QLabel('\u00A9 2017 all rights reserved dj.jansen@casema.nl'), 22, 0, 1, 3, Qt.AlignCenter)
            grid.addWidget(QLabel('Periode gegevens van '+mbetmaand+' '+mbetjr), 13, 1, 1, 2)
            grid.addWidget(QLabel('Uren'), 14, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel('Bedragen'), 14, 1, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel('Uren'), 14, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel('Bedragen'), 14, 3, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel('Werkuren 125%'), 15, 2)
            grid.addWidget(QLabel(str(round(muren125, 2))), 15, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(muurl125bedr, 2))), 15, 3, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Werkuren 150%'), 16, 2)
            grid.addWidget(QLabel(str(round(muren150,2))), 16, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(muurl150bedr,2))), 16, 3, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Werkuren 200%'), 17, 2)
            grid.addWidget(QLabel(str(round(muren200,2))), 17, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(muurl200bedr, 2))), 17, 3, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Reisuren'), 15, 0)
            grid.addWidget(QLabel(str(round(mreisuren, 2))), 15, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mreisbedr, 2))), 15, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Te betalen uren'), 16, 0) 
            grid.addWidget(QLabel('173.3'), 16, 0, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Werkuren 100%'), 17 ,0)
            grid.addWidget(QLabel(str(round(muren, 2))), 17, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(muurlbedr, 2))), 17, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Verlof'), 18, 0)
            grid.addWidget(QLabel(str(round(mverlof,2))), 18, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mverlofbedr,2))), 18, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Ziekte'), 18, 2)
            grid.addWidget(QLabel(str(round(mziek,2))), 18, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mziekbedr,2))), 18, 3, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Feestdag'), 19, 0)
            grid.addWidget(QLabel(str(round(mfeest,2))), 19, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mfeestbedr,2))), 19, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Dokter'), 19, 2)
            grid.addWidget(QLabel(str(round(mdokter,2))), 19, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mdokterbedr,2))), 19, 3, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Geoorloofd verzuim'), 20, 0)
            grid.addWidget(QLabel(str(round(mgverzuim,2))), 20, 0, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(mgverzuimbedr,2))), 20, 1, 1, 1, Qt.AlignRight) 
            grid.addWidget(QLabel('Ongeoorloofd verzuim'), 20, 2)
            grid.addWidget(QLabel(str(round(moverzuim,2))), 20, 2, 1, 1, Qt.AlignRight)
            grid.addWidget(QLabel(str(round(moverzuimbedr,2))), 20, 3, 1, 1, Qt.AlignRight) 
            
            self.setLayout(grid)
            self.setGeometry(400, 50, 350, 300)
                     
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(self.close)
        
            grid.addWidget(cancelBtn, 22, 3, 1, 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro")
  
    window = Widget()
    window.exec_()
    zoekWerknemer(m_email)

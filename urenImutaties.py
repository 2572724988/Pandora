from login import hoofdMenu
import datetime
from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QPixmap, QRegExpValidator, QIcon
from PyQt5.QtWidgets import QLabel, QPushButton,\
     QMessageBox, QLineEdit, QGridLayout, QDialog, QCheckBox, QComboBox
from sqlalchemy import (Table, Column, Integer, String, Float, MetaData, \
                            ForeignKey, create_engine, Boolean)
from sqlalchemy.sql import select, update, func, and_
         
def _11check(mcontr):
    number = str(mcontr)
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

def foutAccount():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Foutief accountnummer opgegeven,\n en/of account niet geldig voor deze bewerking!')
        msg.setWindowTitle('Uren werkorders muteren')
        msg.exec_()
              
def foutWerk():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Critical)
        msg.setText('Foutief werkorder\nopgegeven!')
        msg.setWindowTitle('Uren werkorders muteren')
        msg.exec_()
        
def werkGereed():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Werkorder is afgemeld,\nboekingen niet meer mogelijk!')
    msg.setWindowTitle('Uren werkorders muteren')
    msg.exec_()
    
def geenKeuze():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Geen kostensoort\nkeuze gemaakt')
    msg.setWindowTitle('Uren werkorders muteren')               
    msg.exec_()
    
def ongDatum():
    msg = QMessageBox()
    msg.setStyleSheet("color: black;  background-color: gainsboro")
    msg.setIcon(QMessageBox.Warning)
    msg.setText('Ongeldige datum ingevoerd')
    msg.setWindowTitle('Uren werkorders muteren')               
    msg.exec_()
        
def invoerOK():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Information)
        msg.setText('Uren zijn ingevoerd')
        msg.setWindowTitle('Uren werkorders muteren')
        msg.exec_()
        
def geenUren():
        msg = QMessageBox()
        msg.setStyleSheet("color: black;  background-color: gainsboro")
        msg.setIcon(QMessageBox.Warning)
        msg.setText('Geen uren ingevoerd!')
        msg.setWindowTitle('Uren werkorders muteren')
        msg.exec_()

def windowSluit(self, m_email):
    self.close()
    hoofdMenu(m_email)
    
def urenMut(maccountnr, mwerknr, m_email):
    class Widget(QDialog):
        def __init__(self, parent=None):
            super(Widget, self).__init__(parent)
            self.setWindowTitle("Muteren uren")
            self.setWindowIcon(QIcon('./images/logos/logo.jpg'))
    
            self.setFont(QFont('Arial', 10))
    
            self.Account = QLabel()
            zkaccEdit = QLineEdit(str(maccountnr))
            zkaccEdit.setFixedWidth(150)
            zkaccEdit.setFont(QFont("Arial",10))
            zkaccEdit.textChanged.connect(self.zkaccChanged)
            reg_ex = QRegExp("^[1]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, zkaccEdit)
            zkaccEdit.setValidator(input_validator)
            
            self.Werknummer = QLabel()
            zkwerknEdit = QLineEdit(str(mwerknr))
            zkwerknEdit.setFixedWidth(150)
            zkwerknEdit.setFont(QFont("Arial",10))
            zkwerknEdit.textChanged.connect(self.zkwerknChanged) 
            reg_ex = QRegExp("^[7]{1}[0-9]{8}$")
            input_validator = QRegExpValidator(reg_ex, zkwerknEdit)
            zkwerknEdit.setValidator(input_validator)
     
            self.Soort = QLabel()
            k0Edit = QComboBox()
            k0Edit.setFixedWidth(150)
            k0Edit.setFont(QFont("Arial",10))
            k0Edit.setStyleSheet("color: black;  background-color: gainsboro; selection-background-color: gainsboro; selection-color: black")
            k0Edit.addItem('100%')
            k0Edit.addItem('125%')
            k0Edit.addItem('150%')
            k0Edit.addItem('200%')
            k0Edit.addItem('Reis')
            k0Edit.addItem('Verlof')
            k0Edit.addItem('Extra verlof')
            k0Edit.addItem('Ziekte')
            k0Edit.addItem('Feestdag')
            k0Edit.addItem('Dokter')
            k0Edit.addItem('Geoorl. verzuim')
            k0Edit.addItem('Ong. verzuim')
            k0Edit.activated[str].connect(self.k0Changed) 
                        
            self.Werkuren = QLabel()
            urenEdit = QLineEdit()
            urenEdit.setFixedWidth(150)
            urenEdit.setFont(QFont("Arial",10))
            urenEdit.textChanged.connect(self.urenChanged) 
            reg_ex = QRegExp("^[0-9.]{0,9}$")
            input_validator = QRegExpValidator(reg_ex, urenEdit)
            urenEdit.setValidator(input_validator)
            
            mboekd = str(datetime.datetime.now())[0:10]
            self.Boekdatum = QLabel()
            boekdatumEdit = QLineEdit(mboekd)
            boekdatumEdit.setFixedWidth(150)
            boekdatumEdit.setFont(QFont("Arial",10))
            boekdatumEdit.textChanged.connect(self.boekdatumChanged) 
            reg_ex = QRegExp("^[2]{1}[0-1]{1}[0-9]{2}[-]{1}[0-1]{1}[0-9]{1}[-]{1}[0-3]{1}[0-9]{1}$")
            input_validator = QRegExpValidator(reg_ex, boekdatumEdit)
            boekdatumEdit.setValidator(input_validator)
           
            grid = QGridLayout()
            grid.setSpacing(20)
            
            lblt = QLabel(' Muteren uren (werken - lonen) niet cumulatief')
            grid.addWidget(lblt , 1, 0, 1, 3, Qt.AlignCenter)
                                
            lbl = QLabel()
            pixmap = QPixmap('./images/logos/verbinding.jpg')
            lbl.setPixmap(pixmap)
            grid.addWidget(lbl ,0, 0)
            
            lbl5 = QLabel()
            lbl5.setAlignment(Qt.AlignCenter)
            pixmap = QPixmap('./images/logos/logo.jpg')
            lbl5.setPixmap(pixmap)
            grid.addWidget(lbl5 , 0, 2, 1, 1, Qt.AlignRight)
                 
            grid.addWidget(QLabel('  \u00A9 2017 all rights reserved - dj.jansen@casema.nl'), 8, 0, 1, 3, Qt.AlignCenter)
                                              
            lbl1 = QLabel('Accountnummer')  
            lbl1.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl1, 2, 0)
            grid.addWidget(zkaccEdit, 2, 1)
           
            lbl2 = QLabel('Werkorder')  
            lbl2.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl2, 3, 0)
            grid.addWidget(zkwerknEdit,3, 1)
            
            lbl4 = QLabel('Aanwezig/Afwezig')  
            lbl4.setAlignment(Qt.AlignRight)
            grid.addWidget(lbl4, 4, 0)
            grid.addWidget(k0Edit, 4, 1)
     
            lbl3 = QLabel('Aantal uren')  
            lbl3.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl3, 5, 0)
            grid.addWidget(urenEdit,5, 1)
        
            lbl5 = QLabel('Boekdatum')  
            lbl5.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
            grid.addWidget(lbl5, 6, 0)
            grid.addWidget(boekdatumEdit, 6, 1)
                      
            cBox = QCheckBox('Meerwerk')
            cBox.stateChanged.connect(self.cBoxChanged)
            grid.addWidget(cBox, 5, 2)
                      
            self.setLayout(grid)
            self.setGeometry(500, 300, 150, 150)
    
            applyBtn = QPushButton('Muteren')
            applyBtn.clicked.connect(self.accept)
    
            grid.addWidget(applyBtn,7, 2 , 1 , 1, Qt.AlignRight)
            applyBtn.setFont(QFont("Arial",10))
            applyBtn.setFixedWidth(100)
            applyBtn.setStyleSheet("color: black;  background-color: gainsboro") 
            
            cancelBtn = QPushButton('Sluiten')
            cancelBtn.clicked.connect(lambda: windowSluit(self, m_email)) 
    
            grid.addWidget(cancelBtn, 7, 1, 1 , 1, Qt.AlignRight)
            cancelBtn.setFont(QFont("Arial",10))
            cancelBtn.setFixedWidth(100)
            cancelBtn.setStyleSheet("color: black;  background-color: gainsboro") 
       
        def zkaccChanged(self, text):
            self.Account.setText(text)
            
        def zkwerknChanged(self, text):
            self.Werknummer.setText(text)
            
        def k0Changed(self,text):
            self.Soort.setText(text)
            
        def urenChanged(self,text):
            self.Werkuren.setText(text)
            
        def boekdatumChanged(self, text):
            self.Boekdatum.setText(text)
                    
        state = False  
        def cBoxChanged(self, state):
             if state == Qt.Checked:
                 self.state = True
      
        def returnzkacc(self):
            return self.Account.text()
        
        def returnzkwerkn(self):
            return self.Werknummer.text()
        
        def returnk0(self):
            return self.Soort.text()
        
        def returnuren(self):
            return self.Werkuren.text()
             
        def returnboekdatum(self):
            return self.Boekdatum.text()
    
        def returncBox(self):
            return self.state
           
        @staticmethod
        def getData(parent=None):
            dialog = Widget(parent)
            dialog.exec_()
            return [dialog.returnzkacc(), dialog.returnzkwerkn(),dialog.returnk0(),\
                    dialog.returnuren(), dialog.returncBox(), dialog.returnboekdatum()]  
      
    window = Widget()
    data = window.getData()
    muren = 0
    mu125 = 0
    mu150 = 0
    mu200 = 0
    mreis = 0
    mmeerw100 = 0
    mmeerw125 = 0
    mmeerw150 = 0
    mmeerw200 = 0
    mverlof = 0
    mextraverlof = 0
    mziek = 0
    mfeest = 0
    mdokter = 0
    mgverzuim = 0
    moverzuim = 0
    mboekd = str(datetime.datetime.now())[0:10]
     
    if data[0] and len(data[0]) == 9 and _11check(data[0]):
        maccountnr = int(data[0])
    elif not data[0] and len(str(maccountnr)) == 9 and _11check(maccountnr):
        maccountnr = int(maccountnr)
    else:
       foutAccount()
       return('', mwerknr)
    if data[1] and len(data[1])== 9  and _11check(data[1]):
        mwerknr = int(data[1])
    elif not data[1] and len(str(mwerknr)) == 9 and _11check(mwerknr):
        mwerknr = int(mwerknr) 
    else:
        foutWerk()
        return(maccountnr, '')
                
    metadata = MetaData()
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer, primary_key=True),
        Column('voortgangstatus', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('verlofsaldo', Float),
        Column('extraverlof', Float))
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    selwerk = select([orders_intern]).where(orders_intern.c.werkorderID == mwerknr)
    rpwerk = con.execute(selwerk).first()
       
    if data[2]:
        keuze = data[2]
    elif data[2] == '':
        keuze = '100%'
    else:
        geenKeuze()
        return(maccountnr, mwerknr)
    if data[4]:
        mstatus = True
    else:
        mstatus = False
    if data[5]:
        mboekdatum = data[5]
        if len(mboekdatum) != 10 or int(mboekdatum[0:4]) < 2018 or int(mboekdatum\
             [0:4]) > 2099 or int(mboekdatum[5:7]) >12 or int(mboekdatum[8:10]) > 31:
            ongDatum()
            return(maccountnr, mwerknr)
    else:
        mboekdatum =  mboekd
     
    if rpwerk[1] == 'H':
        mwerknr = 1
        werkGereed()
        return(maccountnr, mwerknr)
    elif not data[3] or int(data[3]) == 0:
        geenUren()
        return(maccountnr, mwerknr)
    elif data[3] and keuze == '100%' and mstatus:
        mmeerw100 = float(data[3])
    elif data[3] and keuze == '100%':
        muren = float(data[3])
    elif data[3] and keuze == '125%' and mstatus:
        mmeerw125 = float(data[3])
    elif data[3] and keuze == '125%':
        mu125 = float(data[3])
    elif data[3] and keuze == '150%' and mstatus:
        mmeerw150 = float(data[3])
    elif data[3] and keuze == '150%':
        mu150 = float(data[3])
    elif data[3] and keuze == '200%' and mstatus:
        mmeerw200 = float(data[3])
    elif data[3] and keuze == '200%':
        mu200 = float(data[3])
    elif data[3] and keuze == 'Reis':
        mreis = float(data[3])
    elif data[3] and keuze == 'Verlof':
        mverlof = float(data[3])
        mstatus = False
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(verlofsaldo = werknemers.c.verlofsaldo - mverlof)
        con.execute(upd) 
    elif data[3] and keuze == 'Extra verlof':
        mextraverlof = float(data[3])
        mstatus = False
        upd = update(werknemers).where(werknemers.c.accountID ==\
            maccountnr).values(extraverlof = werknemers.c.extraverlof - mextraverlof)
        con.execute(upd)       
    elif data[3] and keuze == 'Ziekte':
        mziek = float(data[3])
    elif data[3] and keuze == 'Feestdag':
        mfeest = float(data[3])
        mstatus = False
    elif data[3] and keuze == 'Dokter':
        mdokter = float(data[3])
        mstatus = False
    elif data[3] and keuze == 'Geoorl. verzuim':
        mgverzuim = float(data[3]) 
        mstatus = False
    elif data[3] and keuze == 'Ong. verzuim':
        moverzuim = float(data[3])  
        mstatus = False
                       
    metadata = MetaData()
    wrkwnrln = Table('wrkwnrln', metadata,
        Column('wrkwnrurenID', Integer, primary_key=True),
        Column('werknemerID', None, ForeignKey('werknemers.werknemerID')),
        Column('werknummerID', Integer),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('boekdatum', String),
        Column('aantaluren', Float),
        Column('tabelloon', Float),
        Column('reisloon', Float),
        Column('bruto_loonbedrag', Float),
        Column('meerwerkstatus', Boolean),
        Column('soort', String))
    werknemers = Table('werknemers', metadata,
        Column('werknemerID', Integer(), primary_key=True),
        Column('accountID', None, ForeignKey('accounts.accountID')),
        Column('loonID', None, ForeignKey('lonen.loonID')),
        Column('wnrloonID', Integer))
    orders_intern = Table('orders_intern', metadata,
        Column('werkorderID', Integer(), primary_key=True),
        Column('werkomschrijving', String),
        Column('voortgangstatus', String),
        Column('statusweek', String),
        Column('boekdatum', String),
        Column('begroot_totaal', Float),
        Column('werk_totaal', Float),
        Column('begr_materialen', Float),
        Column('werk_materialen', Float),
        Column('begr_lonen', Float),
        Column('werk_lonen', Float),
        Column('wzagen', Float),
        Column('wschaven', Float),
        Column('wsteken', Float),
        Column('wboren', Float),
        Column('wfrezen', Float),
        Column('wdraaien_klein', Float),
        Column('wdraaien_groot', Float),
        Column('wtappen', Float),
        Column('wnube_draaien', Float),
        Column('wnube_bewerken', Float),
        Column('wknippen', Float),
        Column('wkanten', Float),
        Column('wstansen', Float),
        Column('wlassen_co2', Float),
        Column('wlassen_hand', Float),
        Column('wverpakken', Float),
        Column('wverzinken', Float),
        Column('wmoffelen', Float),
        Column('wschilderen', Float),
        Column('wspuiten', Float),
        Column('wponsen', Float),
        Column('wpersen', Float),
        Column('wgritstralen', Float),
        Column('wmontage', Float),
        Column('werk_reis_uren', Float),
        Column('meerminderwerk', Float))
    lonen = Table('lonen', metadata,
        Column('loonID', Integer, primary_key=True),
        Column('tabelloon', Float),
        Column('werkuur', Float),
        Column('reisuur', Float))
     
    engine = create_engine('postgresql+psycopg2://postgres@localhost/bisystem')
    con = engine.connect()
    mw = select([werknemers]).where(and_(werknemers.c.accountID == maccountnr, werknemers.c.loonID > 52))
    result = con.execute(mw).first()
    if not result:
        foutAccount()
        return(maccountnr, mwerknr)
    mwrkwnruren=(con.execute(select([func.max(wrkwnrln.c.wrkwnrurenID, type_=Integer)\
                                   .label('mwrkwnruren')])).scalar())
    wrkgr = result[2]
    wrkgr2 = result[3]
    loonsel = select([lonen]).where(lonen.c.loonID == wrkgr)
    loonsel2 = select([lonen]).where(lonen.c.loonID == wrkgr2)
    loonres = con.execute(loonsel).first()
    loonres2 = con.execute(loonsel2).first()
    muurloon = loonres2[1]
    mwerkuur = loonres[2]
    mreisuur = loonres[3]
    mwrku125 = mwerkuur*1.25
    mwrku150 = mwerkuur*1.5
    mwrku200 = mwerkuur*2
    loonk = (muren*mwerkuur)+(mreis*mreisuur)+(mu125*mwrku125)+(mu150*mwrku150)+\
             (mu200*mwrku200)+(mmeerw100*mwerkuur)+(mmeerw125*mwerkuur)+(mmeerw150*\
             mwerkuur)+(mmeerw200*mwerkuur)
    meerk = (mmeerw100*mwerkuur)+(mmeerw125*mwrku125)+\
            (mmeerw150*mwrku150)+(mmeerw200*mwrku200)
    lonen = (muren*muurloon)+(mu125*muurloon*1.25)+(mu150*muurloon*1.5)+(mu200\
             *muurloon*2)+(mreis*mreisuur)+(mmeerw100*muurloon)+\
             (mmeerw125*muurloon*1.25)+(mmeerw150*muurloon*1.5)+\
             (mmeerw200*muurloon*2)+(mverlof*muurloon)+(mextraverlof*muurloon)+\
             (mziek*muurloon)+(mfeest*muurloon)+(mdokter*muurloon)+\
             (mgverzuim*muurloon)+(moverzuim*muurloon)
     
    inswrkwnrln = wrkwnrln.insert().values(
    wrkwnrurenID = mwrkwnruren+1,
    werknemerID = result[0],
    boekdatum = mboekdatum,
    aantaluren = muren+mu125+mu150+mu200+mreis+mmeerw100+mmeerw125+mmeerw150+\
      mmeerw200+mverlof+mextraverlof+mziek+mfeest+mdokter+mgverzuim+moverzuim,
    soort = keuze,
    werknummerID = mwerknr,
    tabelloon = muurloon,
    reisloon = mreisuur,
    bruto_loonbedrag = lonen,
    meerwerkstatus = mstatus,
    loonID=wrkgr2)
    con.execute(inswrkwnrln)
                
    if wrkgr > 52 and wrkgr < 56:
        stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
               wzagen = orders_intern.c.wzagen+muren+mu125+mu150+mu200\
               +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
               werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
               meerminderwerk = orders_intern.c.meerminderwerk + meerk)
        con.execute(stmt)
    elif wrkgr > 55 and wrkgr < 59:   
      stmt = update(orders_intern).where(orders_intern.c.werkorderID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wschaven = orders_intern.c.wschaven+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 58 and wrkgr < 62:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wsteken = orders_intern.c.wsteken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 61 and wrkgr < 65:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wboren = orders_intern.c.wboren+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
            meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 64 and wrkgr < 68:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wfrezen = orders_intern.c.wfrezen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 67 and wrkgr < 71:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wdraaien_klein = orders_intern.c.wdraaien_klein+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
            meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.xecute(stmt)
    elif wrkgr > 70 and wrkgr < 74:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
      values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wdraaien_groot = orders_intern.c.wdraaien_groot+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 73 and wrkgr < 77:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
          values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wtappen = orders_intern.c.wtappen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)
    elif wrkgr > 76 and wrkgr < 80:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wnube_draaien = orders_intern.c.wnube_draaien+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 79 and wrkgr < 83:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wnube_bewerken = orders_intern.c.wnube_bewerken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 72 and wrkgr < 86:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wknippen = orders_intern.c.wknippen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 75 and wrkgr < 89:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wkanten = orders_intern.c.wkanten+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 88 and wrkgr < 92:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wstansen = orders_intern.c.wstansen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 91 and wrkgr < 95:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wlassen_co2 = orders_intern.c.wlassen_co2+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 94 and wrkgr < 98:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wlassen_hand = orders_intern.c.wlassen_hand+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 97 and wrkgr < 101:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wverpakken = orders_intern.c.wverpakken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 100 and wrkgr < 104:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wverzinken = orders_intern.c.wverzinken+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 103 and wrkgr < 107:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wmoffelen = orders_intern.c.wmoffelen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 106 and wrkgr < 110:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wschilderen = orders_intern.c.wschilderen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 109 and wrkgr < 113:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wspuiten = orders_intern.c.wspuiten+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 112 and wrkgr < 116:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wponsen = orders_intern.c.wponsen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 115 and wrkgr < 119:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wpersen = orders_intern.c.wpersen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 118 and wrkgr < 122:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wgritstralen = orders_intern.c.wgritstralen+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
    elif wrkgr > 121 and wrkgr < 125:
      stmt = update(orders_intern).where(orders_intern.c.werknummerID == mwerknr).\
        values(werk_lonen = orders_intern.c.werk_lonen+loonk,
           wmontage = orders_intern.c.wmontage+muren+mu125+mu150+mu200\
           +mmeerw100+mmeerw125+mmeerw150+mmeerw200,\
           werk_reis_uren = orders_intern.c.werk_reis_uren+mreis,\
           meerminderwerk = orders_intern.c.meerminderwerk + meerk)
      con.execute(stmt)  
    con.close   
    invoerOK()
    return(maccountnr, mwerknr) 

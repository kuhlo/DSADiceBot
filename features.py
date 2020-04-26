import random
import dice
import pandas
import kampf
import time
from tabulate import tabulate

#########
# Ermittle Random Dinge
#########

# Werfe eine Münze

def getCoinFace():
  coinFaces = ['Kopf', 'Pferd']
  return random.choice(coinFaces)

# Begrüßung
def getBegruessung():
  begrueßung = ['Den Zwölfen zum Gruße', 'Die Zwölfe mit euch!', 'Preiset die Schönheit!'] 
  return random.choice(begruessung)

def getTag():
    tag = ['Windstag', 'Erdstag', 'Markttag', 'Praiostag', 'Rohalstag', 'Feuertag', 'Wassertag']
    return random.choice(tag)


#########
# Prügel Funktionen
#########
# Prügel Verletzungen

def getPruegelVerletzung11():
  verletzungen = ['ausgerenkten Finger', 'gebrochenen Zeh'] 
  return random.choice(verletzungen)

def getPruegelVerletzung12():
  verletzungen = ['einen ausgeschlagenen Zahn', 'ausgerissene Haare', 'eine Schnittwunde'] 
  return random.choice(verletzungen)

# Prügel Verletzungen

 #Verletzungen aus Optional Regeln Prügeln
def verletzung_select(erg):
 verletzung = {
    2: {'T':'Du erleidest eine Abschürfung' ,'L':0.1},
    3: {'T':'Du erleidest Nasenbluten' ,'L':0.1},
    4: {'T':'Du erleidest eine verstauchte Hand' ,'L':0.1},
    5: {'T':'Du erleidest eine Beule' ,'L':0.2},
    6: {'T':'Du erleidest einen Kratzer' ,'L':0.2},
    7: {'T':'Du erleidest ein Veilchen' ,'L':0.2},
    8: {'T':'Du erleidest zwei Veilchen' ,'L':0.25},
    9: {'T':'Du erleidest eine Platzwunde' ,'L':0.25},
    10: {'T':'Du erleidest mehrere Platzwunden' ,'L':0.33},
    11: {'T':'Du erleidest einen {0}'.format(getPruegelVerletzung11()) ,'L':0.33},
    12: {'T':'Du erleidest {0}'.format(getPruegelVerletzung12()) ,'L':0.5}

 }

 return verletzung.get(erg, 'Kein  gültiger Wurf')

# Nachkampftechniken

def getNahkampftechnik():
  technik = ['m Fußfeger', 'r harten Rechten', 'r schnellen Linken', 'm Kopfstoß', 'm Würgegriff', 'm Knietritt', 'm Zehensteiger', 'm Augenstechen', 'm Solarplexusschlag', 'm Tiefschlag']
  return random.choice(technik)

#########
# Talentwahrscheinlichkeiten
#########

# Ermittle Talentwahrscheinlichkeiten
# Idee und Umsetzung von http://dsa5.mueller-kalthoff.com/
def pEigenschaft(e1, e2, e3, taw):
  erfolge = 0
  for x in range (1,21):
    for y in range (1,21):
      for z in range (1,21):
        erfolg = False
        p = taw
        # Check ob möglich
        if p>=0 and e1>0 and e2>0 and e3>0:
          # Kritischer Erfolg
          if ((x==1 and (y==1 or z==1)) or (y==1 and z==1)):
            erfolg = True
          
          # Patzer
          elif ((x==20 and (y==20 or z==20)) or (y==20 and z==20)): erfolg = False

          #normaler Wurf
          else:
            if p==0:
              erfolg = (x<=e1 and y<=e2 and z<=e3)
            else:
              if (x > e1): p = p-(x-e1)
              if (y > e2): p = p-(y-e2)
              if (z > e3): p = p-(z-e3)
              erfolg = (p>-1)
          
          # Probe unmöglich
        else: erfolg = False

          
        if erfolg == True: 
         # print(x,y,z)
          erfolge = erfolge +1

  return erfolge / 8000
        

#########
# Patzer
#########
# Patzer Generator:
#http://www.ulisses-regelwiki.de/index.php/OR_Patzertabellen.html

def patzer_select(erg):
 patzer = {
    2: {'A':'Die Waffe ist unwiederbringlich zerstört. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.' ,'P':'Die Waffe ist unwiederbringlich zerstört. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.', 'F':'Die Waffe ist unwiederbringlich zerstört. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.', 'M':'Der Geist des Zauberers tauscht für 1W6 Tage den Körper mit dem nächsten Lebewesen in seiner Nähe, das größer ist als eine Ratte.', 'G': 'Im Umkreis von 2W6 Metern gehen brennbare Materialien in Flammen auf (außer Lebewesen und die Kleidung des Geweihten).'},
    3: {'A':'Die Waffe ist nicht mehr verwendbar, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.' ,'P':'Die Waffe ist nicht mehr verwendbar, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt', 'F':'Die Waffe ist nicht mehr einsetzbar, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.', 'M':'Der Zauberer wird für 1W6 Tage von einem Mindergeist verfolgt.','G':'Die gewirkte Liturgie/Zeremonie hat einen gegenteiligen Effekt. Ein Bann des Lichts erzeugt Licht, ein Heilsegen fügt dem Ziel Schaden zu usw.'},
    4: {'A':'Die Waffe ist beschädigt worden. Alle Proben auf Attacke und Parade sind um 2 erschwert, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.' ,'P':'Die Waffe ist beschädigt worden. Alle Proben auf Attacke und Parade sind um 2 erschwert, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.', 'F':'Die Waffe ist beschädigt worden. Alle Proben auf Fernkampf sind um 4 erschwert, bis sie repariert wird. Bei unzerstörbaren Waffen wird das Ergebnis wie bei 5 behandelt.', 'M':'Das Ziel des Zaubers ändert sich zufällig nach Wahl des Meisters.', 'G':'Das Ziel der Liturgie/Zeremonie ändert sich zufällig nach Wahl des Meisters.'},
    5: {'A':'Die Waffe ist zu Boden gefallen.' ,'P':'Die Waffe ist zu Boden gefallen.', 'F':'Die Waffe ist zu Boden gefallen.', 'M':'Der Zauberer verwandelt sich für 1W6 Stunden in ein Kleintier nach Wahl des Spielleiters.', 'G':'Der Geweihte hat für 1W6 Tage nachts seltsame Visionen und Alpträume.'},
    6: {'A':'Die Waffe des Helden ist in einem Baum, einer Holzwand, dem Boden oder Ähnlichem stecken geblieben. Um sie zu befreien, ist 1 Aktion und eine um 1 erschwerte Probe auf Kraftakt (Ziehen & Zerren) notwendig.' ,'P':'Die Waffe des Helden ist in einem Baum, einer Holzwand, dem Boden oder Ähnlichem stecken geblieben. Um sie zu befreien, ist 1 Aktion und eine um 1 erschwerte Probe auf Kraftakt (Ziehen & Zerren) notwendig.', 'F':'Das Geschoss trifft aus Versehen einen Freund oder einen am Kampf Unbeteiligten. Ist kein solches Ziel in der Nähe, wird diese Auswirkung wie 11 Selbst verletzt behandelt. Der Schaden der Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt.','M': 'Die gesamte Astralkraft verlässt den Körper des Zauberers und manifestiert sich als Regen aus bunten Funken, illusionären Schmetterlingen und kleinen Regenbögen. Die verlorenen Astralpunkte können regulär regeneriert werden.', 'G':'Durch einen Blick in die Sphären ist der Geweihte so eingeschüchtert, dass er einen Tag lang 3 Stufen Furcht erhält.'},
    7: {'A':'Der Held stolpert und stürzt, wenn seinem Spieler nicht eine um 2 erschwerte Probe auf Körperbeherrschung (Balance) gelingt. Sollte er das nicht schaffen, erhält der Held den Status Liegend.' ,'P':'Der Held stolpert und stürzt, wenn seinem Spieler nicht eine um 2 erschwerte Probe auf Körperbeherrschung (Balance) gelingt. Sollte er das nicht schaffen, erhält der Held den Status Liegend.', 'F':'Der spektakuläre Fehlschuss trifft ein Objekt (Ladenschild herunter geschossen, Glasfenster zu Bruch gegangen etc.).', 'M':'Der Zauberer verliert für 1W6 Tage die Fähigkeit, auf seinen AE-Vorrat zuzugreifen.', 'G':'Der Geweihte verliert für 1W6 Tage die Fähigkeit, auf seinen KE-Vorrat zuzugreifen.'},
    8: {'A':'Der Held stolpert, seine nächste Handlung ist um 2 erschwert.' ,'P':'Der Held stolpert, seine nächste Handlung ist um 2 erschwert.', 'F':'Der Held hat Rückenschmerzen und erleidet für die nächsten 3 Kampfrunden eine Stufe Schmerz.', 'M':'Der Zauberer hat für die nächsten 1W6 Tage pochende Kopfschmerzen. Er leidet während dieser Zeit unter einer Stufe des Zustands Betäubung.', 'G':'Der Geweihte erhält für einen Tag 4 Stufen Entrückung.'},
    9: {'A':'Der Held erhält für 3 Kampfrunden eine Stufe Schmerz.' ,'P':'Der Held erhält für 3 Kampfrunden eine Stufe Schmerz.', 'F':'Der Held benötigt 2 komplette Kampfrunden, um die Waffe wieder einsatzbereit zu machen.', 'M': 'Die gesamte Astralkraft verlässt den Körper des Zauberers und springt auf das nächste magisch begabte Ziel über. Das Ziel erhält die gesamten Astralpunkte des Zauberers, auch über sein natürliches Maximum an Astralenergie hinaus. Der Zauberer kann die verlorenen Astralpunkte regulär regenerieren.', 'G': 'Der Geweihte ist für einen Tag lang verwirrt und redet unverständliches Zeug, an das er sich später nicht mehr erinnert. Er erhält 3 Stufen Verwirrung.'},
    10: {'A':'Der Held hat sich im Eifer des Gefechts den Kopf gestoßen. Er erhält für eine Stunde eine Stufe Betäubung.' ,'P':'Der Held hat sich im Eifer des Gefechts den Kopf gestoßen. Er erhält für eine Stunde eine Stufe Betäubung.', 'F':'Der Held ist mit Zielen oder mit seiner Waffe beschäftigt. Bis zu seiner nächsten Aktion kann er keine Verteidigungen ausführen.', 'M':'Der Zauberer verliert für 1W6 Tage seine Befähigung zu sprechen.', 'G': 'Der Geweihte verliert für 1W6 Tage seine Befähigung zu sprechen.'},
    11: {'A':'Der Held hat sich selbst verletzt und erleidet Schaden. Der Schaden seiner Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt. Bei unbewaffneten Kämpfern wird 1W6 TP angenommen.' ,'P':'Der Held hat sich selbst verletzt und erleidet Schaden. Der Schaden seiner Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt. Bei unbewaffneten Kämpfern wird 1W6 TP angenommen.', 'F':'Der Held hat sich selbst verletzt und erleidet Schaden. Der Schaden der Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt.', 'M':'Haar und Bart des Zauberers färben sich bunt, wachsen später jedoch in der ursprünglichen Farbe nach.', 'G': 'Für einen Tag erhält der Geweihte ein Stigma.'},
    12: {'A':'Ein schwerer Eigentreffer des Helden. Der Schaden seiner Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt und dann verdoppelt. Bei unbewaffneten Kämpfern wird 1W6 TP angenommen. ' ,'P':'Ein schwerer Eigentreffer des Helden. Der Schaden seiner Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt und dann verdoppelt. Bei unbewaffneten Kämpfern wird 1W6 TP angenommen.', 'F':'Ein schwerer Eigentreffer. Der Schaden der Waffe wird unter Einbeziehung des Schadensbonus ausgewürfelt und dann verdoppelt.','M':'Eine ätherische Stimme erklingt aus demNichts und sagt „Tu das nie wieder!“', 'G':'Der Geweihte verwurzelt mit dem Boden und kann seine Füße für 1W6 Minuten nicht bewegen. Er erhält währenddessen den Status Fixiert.'}

 }

 return patzer.get(erg, 'Kein  gültiger Wurf')



#########
# Testdinge
#########

def sieben_sauf():
  wurf = dice.roll('2d6')
  return wurf


def get_talentwert(talent):
  pass
  return True


def musik_select():
  musik_url = {
    '🦄':'https://www.youtube.com/watch?v=4ceowgHn8BE' , 
    '🍺': 'https://www.youtube.com/watch?v=fIuO3RpMvHg',
    '☠': 'https://www.youtube.com/watch?v=QHWAzBZ2hDA',
    '😳': 'https://www.youtube.com/watch?v=DeXoACwOT1o',
    '🏘': 'https://www.youtube.com/watch?v=xu2pESvXcmM',
    '🕷': 'https://www.youtube.com/watch?v=rMETfcg71f8',
    '⚔': 'https://www.youtube.com/watch?v=w0sUw735gRw'

  }
  return musik_url



def getSteigerung():
    tables = None
    steigerungstable = None
    tables = pandas.read_html("http://www.ulisses-regelwiki.de/index.php/Heldenerschaffung.html", header=0, flavor='html5lib')
    steigerungstable = tables[4]
    steigerungstable.columns = ['Wert', 'A', 'B', 'C', 'D', 'E']
    #print('wert:' + str(steigerungstable[0, 'Wert']))
    #steigerungstable.at[0, 'Wert'] = 0
    return tabulate(steigerungstable, headers='keys', tablefmt='psql', showindex=False, numalign="right")


def getAspekte():
    tables = None
    aspekte = None
    tables = pandas.read_html("https://www.ulisses-regelwiki.de/index.php/aspekte.html", header=0, flavor='html5lib')
    print(tables)
    return tabulate(tables, headers='keys', tablefmt='psql', showindex=False, numalign="right")

def prettyprintDF(df):
    prettytable = tabulate(df, headers='keys', tablefmt='psql', showindex=False, numalign="right")
    return prettytable

def prettyprintlist(tabelle, ueberschriften):
    prettytable = tabulate(tabelle, ueberschriften, tablefmt='simple', showindex=False)
    return prettytable


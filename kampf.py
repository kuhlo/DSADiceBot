import dice
import gspread
import pygsheets
import pandas as pd
from tabulate import tabulate
from oauth2client.service_account import ServiceAccountCredentials

#########
# Öffne Worksheet in gspread
#########

scope = [
    'https://spreadsheets.google.com/feeds',
    'https://www.googleapis.com/auth/drive'
]

credentials = ServiceAccountCredentials.from_json_keyfile_name(
    'cred.json', scope)
gc = gspread.authorize(credentials)
wks = gc.open("DSA_Discord - Aventurien")
sheet = wks.sheet1

pyggc = pygsheets.authorize(service_file='cred.json')
wks_pyggc = pyggc.open("DSA_Discord - Aventurien")
pyg_sheet = wks_pyggc.sheet1
pyg_karten_sheet = wks_pyggc.worksheet('title', 'Karten')

# Sheet für Pflanzen-Gebiete und Pflanzen
pflanzen_gebiete_sheet = wks_pyggc.worksheet('title', 'Gebiete_Pflanzen')


#######
# Funktionen um df für Pflanzen zu laden
#######

### Update end!

def loadPflanzendf():
	pflanzen_df = pflanzen_gebiete_sheet.get_as_df(has_header=True, start='A1', end='Q750')
	return pflanzen_df

#########
# Alle Funktionen rund um den Kampf
#########


# Load gsheets data into dataframe
def loadDF():
    data = pyg_sheet.get_as_df(has_header=True, start='A1', end='AE30')
    return data


# Make data pretty
def tabulateDF():
    inidf = pyg_sheet.get_as_df(has_header=True, start='A1', end='F30')
    inidf = inidf[::2]
    print(inidf)
    return inidf


def ermittleInitative():
    inidf = None
    inidf = pyg_sheet.get_as_df(has_header=True, start='A1', end='AE61')
    # copy inidf in new dataframe
    kampfdf = inidf
    kampfdf = kampfdf[inidf.Active == 'x']

    # get each third row
    inidf = inidf[::3]
    #print(inidf)
    # get only characters which are active
    inidf = inidf[inidf.Active == 'x']
    inidf['INI'] = 0
    # Calculate final Initiative
    inidf['INI'] = inidf.apply(lambda x: int(x['INIBasis']) + int(dice.roll('1d6')), axis=1)
    # Calculate Reihenfolge
    reihenfolge = inidf[['ID', 'Char', 'INIBasis', 'INI']]
    reihe = reihenfolge.sort_values(by=['INI', 'INIBasis', ], ascending = False)
    reihe['Reihenfolge'] = range(1,len(reihe.index)+1)
    return reihe, inidf


def ermittleKampfdaten():
    kampfdf = None
    return None



def getKarten(kat):
    kartendf = None
    kartendf = pyg_karten_sheet.get_as_df(has_header=True, start='A1', end='E28')
    kartendf = kartendf[kartendf.Kategorie == kat]
    kartendf = kartendf[kartendf.Active == 'x']
    try: 
        pfaddf= kartendf.sample(n=1)
    except: 
        print('No active card') 
    return pfaddf.Pfad.item()

def attacke(ATID, VTID, Mod, Zone = 0):
    kampfwerte = pd.read_csv(filepath_or_buffer='kampfdf.csv')
    
    # Reichweiten unterschied 
    ATWaffenlänge = kampfwerte.loc[kampfwerte['ID']==int(ATID), 'Reichweite'].item()
    VTWaffenlänge = kampfwerte.loc[kampfwerte['ID']==int(VTID), 'Reichweite'].item()
    reichweite = {'kurz' : -2, 'mittel' : 0, 'lang' : 2}
    if ATWaffenlänge != 'FK' and VTWaffenlänge != 'FK':
        reichweite_mod =reichweite[ATWaffenlänge] - reichweite[VTWaffenlänge]
    else:
        reichweite_mod = 0
    print('Reichweite')
    print(reichweite_mod)
    # Welche Zone
    print('Zone (0, K, T, A, B)')
    print(Zone)
    if Zone == str(0): 
        Zonemod = 0
    else: 
        if kampfwerte.loc[kampfwerte['ID']==int(ATID), 'Gez. Schuss / Angriff'].item() == 'x':
            divisor = 2
        else: divisor = 1
        if Zone == 'K':
            Zonemod = 10 / divisor
        elif Zone == 'T':
            Zonemod = 4 / divisor
        elif Zone == 'A':
            Zonemod = 8 / divisor
        elif Zone == 'B':
            Zonemod = 8 / divisor
    ATWert = int(kampfwerte.loc[kampfwerte['ID']==int(ATID), 'Eff. AT'].item()) + int(Mod) - int(Zonemod) - int(kampfwerte.loc[kampfwerte['ID']==int(ATID), 'A AT'].item()) * 3 + reichweite_mod
    print('Attackebasis & Modifikation - Zonemod')
    print(int(kampfwerte.loc[kampfwerte['ID']==int(ATID), 'Eff. AT'].item()))
    print(int(Mod) - int(Zonemod))
    ATAnzahl = kampfwerte.loc[kampfwerte['ID']==int(ATID), 'A AT'].item() + 1
    print('AttackeAnzahl')
    print(ATAnzahl)
    #print('Dataframe')
    #print(kampfwerte)
    kampfwerte.at[int(ATID)-1,'A AT'] = ATAnzahl
    print('Wert A AT im DF')
    print(kampfwerte.at[int(ATID)-1,'A AT'])
    kampfwerte.to_csv(path_or_buf='kampfdf.csv', sep=',', header=True, index=False)
    wurf = sum(dice.roll('1d20'))
    print('Attackewurf')
    print(wurf)
    #wurf = 1
    if wurf == 1:
        wurf_bestätigung = sum(dice.roll('1d20'))
        print('AT: Wurf Bestätigung')
        print(wurf_bestätigung)
        if wurf_bestätigung <= ATWert:
            # Geschafft, Wurf, halbe Verteidigung, Bestätigt (= doppelter Schaden)
            return True, wurf, True, True  
        else:
            # Geschafft, Wurf, halbe Verteidigung, Bestätigt (= doppelter Schaden)
            return True, wurf, True, False 
    elif wurf == 20:
        wurf_bestätigung = sum(dice.roll('1d20'))
        print('AT: Wurf Bestätigung')
        print(wurf_bestätigung)
        if wurf_bestätigung >= ATWert:
            # Daneben, Wurf, irrelevant, Bestätigt (= Patzer) 
            return False, wurf, False, True  
        else:
            # Daneben, Wurf, irrelevant, Bestätigt (= Patzer) 
            return False, wurf, False, False 
    elif  wurf <= ATWert:
        #Attacke erfolgreich, Wurfergebnis, nicht kritisch
        return True, wurf, False, False  
    else:
        #Attacke nicht erfolgreich, Wurfergebnis, kein patzer
        return False, wurf, False, False 

def parade(ATID, VTID, Mod, kritisch = 1):
    kampfwerte = pd.read_csv(filepath_or_buffer='kampfdf.csv')
    print('Parade Divisor w/ Kritisch')
    print(kritisch)
    # Zweig für Verteidigung gegen FK - AW - 4 statt PA 
    if kampfwerte.loc[kampfwerte['ID']==int(ATID), 'Reichweite'].item() == 'FK':
        PAWert = round((int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'Ausweichen'].item()) - int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'A PA'].item()) * 3 - 4) / int(kritisch),0)
    else:
        PAWert = round((int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'Eff. PA'].item()) - int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'A PA'].item()) * 3) / int(kritisch),0)
    print('PAWert')
    print(PAWert)
    VTAnzahl = kampfwerte.loc[kampfwerte['ID']==int(ATID), 'A PA'].item() + 1 
    kampfwerte.at[int(VTID)-1,'A PA'] = VTAnzahl
    #print('Dataframe')
    #print(kampfwerte)
    kampfwerte.to_csv(path_or_buf='kampfdf.csv', sep=',', header=True, index=False)
    wurf = sum(dice.roll('1d20'))
    print('Verteidigungswert')
    print(int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'Eff. PA'].item()))
    print('Verteidigungwurf')
    print(wurf)
    if wurf == 1:
        wurf_bestätigung = sum(dice.roll('1d20'))
        print('PA: Wurf Bestätigung')
        print(wurf_bestätigung)
        if wurf_bestätigung <= PAWert:
            # Geschafft, Wurf, Kritisch Bestätigt (= Passierschlag), kein Patzer
            print('PA: Kritisch bestätigt, Passierschlag')
            return True, wurf, True, False
        else:
            # Geschafft, Wurf, nicht Bestätigt, kein Patzer
            print('PA: Kritisch nicht bestätigt')
            return True, wurf, False, False 
    elif wurf == 20:
        wurf_bestätigung = sum(dice.roll('1d20'))
        print('PA: Wurf Bestätigung')
        print(wurf_bestätigung)
        if wurf_bestätigung >= PAWert:
            print('PA: Bestätigter Patzer')
            # Nicht verteidigt, Wurf, Nicht Bestätigt kritisch, Patzer
            return False, wurf, False, True  
        else:
            # Nicht verteidigt, Wurf, Nicht Bestätigt kritisch, Patzer 
            print('PA: Nicht bestätigter Patzer')
            return False, wurf, False, False 
    elif  wurf <= PAWert:
        print('PA: Verteidigt, kein kritisch')
        #verteidigt, Wurfergebnis, nicht kritisch, kein Patzer
        return True, wurf, False, False  
    else:
        print('PA: Nicht verteidigt, kein Patzer')
        # nicht verteidigt, Wurfergebnis, kein patzer
        return False, wurf, False, False 


def attacke_schaden(ATID, VTID, Zone = 0):
    # Read CSV
    kampfwerte = pd.read_csv(filepath_or_buffer='kampfdf.csv')
    # Get Weapon damage
    TP = kampfwerte.loc[kampfwerte['ID']==int(ATID), 'TP'].item()
    # How much dice 1-9
    AnzahlWürfe = int(TP[0])
    print('Anzahl Würfe')
    print(AnzahlWürfe)
    # How many sides (d1-d9)
    AnzahlSeiten = int(TP[2])
    print('Anzahl Seiten')
    print(AnzahlSeiten)
    # Modification 0-100
    Modifikator = int(TP[4:])
    print('TP Modifikation')
    print(Modifikator)
    string = str(AnzahlWürfe) + 'd' + str(AnzahlSeiten)
    print(str(string))
    schaden = int(dice.roll(string)) + Modifikator
    print('Schaden')
    print(schaden)
    print('Zone')
    print(Zone)
    print(type(Zone))
    if Zone == str(0):
        wurf = sum(dice.roll('1d20'))
        print('Wurf Auswahl Zone')
        print(wurf)
        größe = kampfwerte.loc[kampfwerte['ID']==int(VTID), 'Größe'].item()
        print('Größe gem. Sheet')
        print(größe)
        größe = größe_translation(größe)
        print('Größe gem. Dict')
        print(größe)
        Zone = trefferzone_select(wurf)[größe]
        print('Gew. Zone')
        print(Zone)
        if Zone == 'K':
            trefferzone = 'Kopf'
        elif Zone == 'T':
            trefferzone = 'Torso'
        elif Zone == 'A':
            trefferzone = 'Arme'
        elif Zone == 'B':
            trefferzone = 'Beine'
    else:
        if Zone == 'K':
            trefferzone = 'Kopf'
        elif Zone == 'T':
            trefferzone = 'Torso'
        elif Zone == 'A':
            trefferzone = 'Arme'
        elif Zone == 'B':
            trefferzone = 'Beine'
    
    #Teste für Wundschwelle
    if schaden >= round(int(kampfwerte.loc[kampfwerte['ID']==int(VTID), 'KO'].item())/2,0):
        # Teste Selbstbeherrschung
        if probe_selbstbeherrschung(VTID) == False:
            wert = int(dice.roll('1d6'))
            schlimme_verletzung = schlimme_verletzung_select(trefferzone, wert)
   
    return schaden, trefferzone, schlimme_verletzung

def größe_translation(größe):
    if größe == 'Humanoid klein':
        return 'Hk'
    elif größe == 'Humanoid mittel':
        return 'Hm'
    elif größe == 'Humanoid groß':
        return 'Hg'
    elif größe == 'Vierbeinig klein':
        return 'Vk'
    elif größe == 'Vierbeinig mittel':
        return 'Vm'
    elif größe == 'Vierbeinig groß':
        return 'Vg'
    elif größe == 'sechs Gliedmaßen groß':
        return 'Sg'
    elif größe == 'sechs Gliedmaßen riesig':
        return 'Sr'
    elif größe == 'Fangarme':
        return 'F'
    elif größe == 'sonstige':
        return 'S'

def trefferzone_select(erg):
    trefferzone = {
        1: {
            'Hk': 'K',
            'Hm': 'K',
            'Hg': 'K',
            'Vk': 'K',
            'Vm': 'K',
            'Vg': 'K',
            'Sg': 'K',
            'Sr': 'K',
            'F':  'K',
            'S':  'S'  
        },
         2: {
            'Hk': 'K',
            'Hm': 'K',
            'Hg': 'K',
            'Vk': 'K',
            'Vm': 'K',
            'Vg': 'K',
            'Sg': 'K',
            'Sr': 'K',
            'F':  'K',
            'S':  'S'  
        },
         3: {
            'Hk': 'K',
            'Hm': 'T',
            'Hg': 'T',
            'Vk': 'K',
            'Vm': 'K',
            'Vg': 'K',
            'Sg': 'K',
            'Sr': 'T',
            'F':  'K',
            'S':  'S'  
        },
         4: {
            'Hk': 'K',
            'Hm': 'T',
            'Hg': 'T',
            'Vk': 'K',
            'Vm': 'K',
            'Vg': 'K',
            'Sg': 'K',
            'Sr': 'T',
            'F':  'K',
            'S':  'S'  
        },
         5: {
            'Hk': 'K',
            'Hm': 'T',
            'Hg': 'T',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'K',
            'Sg': 'K',
            'Sr': 'T',
            'F':  'T',
            'S':  'S'  
        },
         6: {
            'Hk': 'K',
            'Hm': 'T',
            'Hg': 'T',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'T',
            'Sg': 'K',
            'Sr': 'T',
            'F':  'T',
            'S':  'S'  
        },
         7: {
            'Hk': 'T',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'T',
            'Sg': 'K',
            'Sr': 'T',
            'F':  'A',
            'S':  'S'  
        },
         8: {
            'Hk': 'T',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'T',
            'Sg': 'T',
            'Sr': 'T',
            'F':  'A',
            'S':  'S'  
        },
         9: {
            'Hk': 'T',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'T',
            'Sg': 'T',
            'Sr': 'T',
            'F':  'A',
            'S':  'S'  
        },
         10: {
            'Hk': 'T',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'T',
            'Vg': 'T',
            'Sg': 'T',
            'Sr': 'T',
            'F':  'A',
            'S':  'S'  
        },
         11: {
            'Hk': 'A',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'A',
            'Vg': 'T',
            'Sg': 'T',
            'Sr': 'A',
            'F':  'A',
            'S':  'S'  
        },
         12: {
            'Hk': 'A',
            'Hm': 'T',
            'Hg': 'A',
            'Vk': 'T',
            'Vm': 'A',
            'Vg': 'A',
            'Sg': 'T',
            'Sr': 'A',
            'F':  'A',
            'S':  'S'  
        },
         13: {
            'Hk': 'A',
            'Hm': 'A',
            'Hg': 'A',
            'Vk': 'A',
            'Vm': 'A',
            'Vg': 'A',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'A',
            'S':  'S'  
        },
         14: {
            'Hk': 'A',
            'Hm': 'A',
            'Hg': 'A',
            'Vk': 'A',
            'Vm': 'A',
            'Vg': 'A',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'B',
            'S':  'S'  
        },
         15: {
            'Hk': 'A',
            'Hm': 'A',
            'Hg': 'A',
            'Vk': 'A',
            'Vm': 'A',
            'Vg': 'A',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'B',
            'S':  'S'  
        },
         16: {
            'Hk': 'A',
            'Hm': 'A',
            'Hg': 'A',
            'Vk': 'A',
            'Vm': 'A',
            'Vg': 'A',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'B',
            'S':  'S'  
        },
         17: {
            'Hk': 'A',
            'Hm': 'B',
            'Hg': 'B',
            'Vk': 'B',
            'Vm': 'B',
            'Vg': 'B',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'B',
            'S':  'S'  
        },
         18: {
            'Hk': 'A',
            'Hm': 'B',
            'Hg': 'B',
            'Vk': 'B',
            'Vm': 'B',
            'Vg': 'B',
            'Sg': 'A',
            'Sr': 'A',
            'F':  'B',
            'S':  'S'  
        },
         19: {
            'Hk': 'B',
            'Hm': 'B',
            'Hg': 'B',
            'Vk': 'B',
            'Vm': 'B',
            'Vg': 'B',
            'Sg': 'B',
            'Sr': 'B',
            'F':  'B',
            'S':  'S'  
        },
         20: {
            'Hk': 'B',
            'Hm': 'B',
            'Hg': 'B',
            'Vk': 'B',
            'Vm': 'B',
            'Vg': 'B',
            'Sg': 'B',
            'Sr': 'B',
            'F':  'B',
            'S':  'S'  
        },
    }

    return trefferzone.get(erg, 'Kein  gültiger Wurf')


# def schlimme_verletzung_select(trefferzone, wert):
#     effekt = {
#         1: {
#             'Kopf': 
#                 'Nase', 'Der Held hat einen Treffer gegen die Nase abbekommen. Er ist etwas desorientiert und erleidet 1 SP.'
#             'Torso':
#                 'Rippe', 'Ein Treffer gegen die Rippe raubt dem Helden die Luft und er erleidet 1W3  SP zusätzlich.'
#             'Arm':
#                 'Oberarm', 'Ein Treffer gegen den Oberarm sorgt dafür, dass der Arm leicht gelähmt ist. 2 SP.'


#         }






#     }

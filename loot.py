import random


def getMünzVerteilung():
    coinNbr = []
    coinNbr.append(random.choice(range(4)))
    coinNbr.append(random.choice(range(4, 9)))
    coinNbr.append(random.choice(range(9, 16)))

    return coinNbr


def getFremdmünzen(wurf):
    if wurf < 17: region = 'Bornland'
    elif wurf < 19: region = 'Vallusa'
    elif wurf < 41: region = 'Horasreich'
    elif wurf < 48: region = 'Bergkönigreich'
    elif wurf < 50: region = 'Xeraanien (schwarze Lande)'
    elif wurf < 52: region = 'Oron (schwarze Lande)'
    elif wurf < 68: region = 'Mhaharanyat Aranien'
    elif wurf < 79: region = 'Kalifat'
    elif wurf < 88: region = 'Großemirat Mengbilla'
    elif wurf < 104: region = 'Alanfanisches Imperium'
    elif wurf < 111: region = 'Káhet Ni Kemi'

    return region


# Ermittle Geld, Wertvolles

#'Karfunkel' wenn diese auch gefunden werden sollen
def getWertvolles():
    geld_wertvoll = [
        'Kleingeld', 'Kleingeld (Fremdwährung)', 'Edelsteine', 'schöne Steine',
        'Pokal', 'Kleingeld', 'Kleingeld', 'Kleingeld'
    ]

    return random.choice(geld_wertvoll)


# Ermittle Bau- und Rohstoffe


def getMetallRohstoffe():
    metall_rohstoffe = ['Metalle', 'Hölzer', 'Minerale', 'Bein']

    return random.choice(metall_rohstoffe)


# Ermittle Bau- und Elexiere


def getKräuterTränkeElixire():
    kräuter_tränke_elixiere = [
        'Heilpflanze', 'Nutzpflanze', 'Giftpflanze',
        'Tränke, Elixiere, Gifte & Salben', 'Tabak'
    ]

    return random.choice(kräuter_tränke_elixiere)


def getMetalle(wert):
    if wert < 11: metall = 'Eisen'
    elif wert < 21: metall = 'Kupfer'
    elif wert < 31: metall = 'Bronze'
    elif wert < 41: metall = 'Messing'
    elif wert < 51: metall = 'Zinn'
    elif wert < 61: metall = 'Nickel'
    elif wert < 71: metall = 'Katzengold'
    elif wert < 76: metall = 'Neckkupfer'
    elif wert < 81: metall = 'Stahl'
    elif wert < 83: metall = 'unbekannt 81-82'
    elif wert < 85: metall = 'unbekannt 83-84'
    elif wert < 86: metall = 'unbekannt 85'
    elif wert < 88: metall = 'Silber'
    elif wert < 89: metall = 'unbekannt 88'
    elif wert < 91: metall = 'Gold'
    elif wert < 93: metall = 'unbekannt 91-92'
    elif wert < 95: metall = 'unbekannt 93 - 94'
    elif wert < 97: metall = 'Mondsilber/Platin'
    elif wert < 100: metall = 'unbekannt 99'

    return metall


def getHölzer(wert):
    if wert < 11: holz = 'Fichte'
    elif wert < 21: holz = 'Kiefer'
    elif wert < 26: holz = 'Lärche'
    elif wert < 31: holz = 'Tanne'
    elif wert < 36: holz = 'Ahorn'
    elif wert < 41: holz = 'Birke'
    elif wert < 46: holz = 'Bosparanie'
    elif wert < 51: holz = 'Buche'
    elif wert < 56: holz = 'Erle'
    elif wert < 61: holz = 'Esche'
    elif wert < 66: holz = 'Espe'
    elif wert < 71: holz = 'Hainbuche'
    elif wert < 76: holz = 'Linde'
    elif wert < 78: holz = 'Pappel'
    elif wert < 80: holz = 'Rosskastanie'
    elif wert < 82: holz = 'Weide'
    elif wert < 84: holz = 'Eibe'
    elif wert < 86: holz = 'Pinie'
    elif wert < 88: holz = 'Zeder'
    elif wert < 90: holz = 'Zypresse'
    elif wert < 92: holz = 'unbekannt 90-91'
    elif wert < 94: holz = 'unbekannt 92-93'
    elif wert < 95: holz = 'unbekannt 94'
    elif wert < 96: holz = 'unbekannt 95'
    elif wert < 97: holz = 'unbekannt 96'
    elif wert < 99: holz = 'unbekannt 97-98'
    elif wert < 101: holz = 'unbekannt 99-100'

    return holz


def getMinerale(wert):
    if wert < 11: mineral = 'Sandstein'
    elif wert < 21: mineral = 'Basalt'
    elif wert < 26: mineral = 'Kalkstein'
    elif wert < 36: mineral = 'Granit'
    elif wert < 56: mineral = 'unbekannt 36-55'
    elif wert < 61: mineral = 'unbekannt 56-60'
    elif wert < 66: mineral = 'unbekannt 61-65'
    elif wert < 76: mineral = 'unbekannt 66-75'
    elif wert < 81: mineral = 'unbekannt 76-80'
    elif wert < 86: mineral = 'unbekannt 81-85'
    elif wert < 88: mineral = 'unbekannt 86-87'
    elif wert < 92: mineral = 'unbekannt 88-91'
    elif wert < 93: mineral = 'unbekannt 92'
    elif wert < 94: mineral = 'unbekannt 93'
    elif wert < 95: mineral = 'unbekannt 94'
    elif wert < 96: mineral = 'unbekannt 95'
    elif wert < 97: mineral = 'unbekannt 96'
    elif wert < 98: mineral = 'unbekannt 97'
    elif wert < 99: mineral = 'unbekannt 98'
    elif wert < 100: mineral = 'unbekannt 99'
    elif wert < 101: mineral = 'unbekannt 100'

    return mineral


def getEdelsteine(wert):
    if wert < 6: edelstein = 'Tierzahn'
    elif wert < 10: edelstein = 'Tierhorn'
    elif wert < 14: edelstein = 'Tierknochen'
    elif wert < 18: edelstein = 'Koralle'
    elif wert < 22: edelstein = 'Meerschaum'
    elif wert < 26: edelstein = 'Schildpatt'
    elif wert < 30: edelstein = 'Perlmutt'
    elif wert < 34: edelstein = 'Perle'
    elif wert < 38: edelstein = 'unbekannt 34-37'
    elif wert < 42: edelstein = 'Obsidian'
    elif wert < 46: edelstein = 'unbekannt 42-45'
    elif wert < 50: edelstein = 'Roter Obsidian'
    elif wert < 53: edelstein = 'Onyx'
    elif wert < 55: edelstein = 'Baryt'
    elif wert < 57: edelstein = 'Malachit'
    elif wert < 59: edelstein = 'Amethyst'
    elif wert < 61: edelstein = 'Achat'
    elif wert < 65: edelstein = 'Karneol'
    elif wert < 67: edelstein = 'Bergkristall'
    elif wert < 69: edelstein = 'Aquamarin'
    elif wert < 71: edelstein = 'Rosenquarz'
    elif wert < 73: edelstein = 'Aventurin'
    elif wert < 75: edelstein = 'Rauchquarz'
    elif wert < 77: edelstein = 'Magnetit'
    elif wert < 79: edelstein = 'Turmalin'
    elif wert < 81: edelstein = 'Granat'
    elif wert < 83: edelstein = 'Lapislazuli'
    elif wert < 85: edelstein = 'Topas'
    elif wert < 87: edelstein = 'Opal'
    elif wert < 89: edelstein = 'Feuer Opal'
    elif wert < 91: edelstein = 'Rosa Jade'
    elif wert < 93: edelstein = 'Perlmutt'
    elif wert < 95: edelstein = 'Bernstein'
    elif wert < 97: edelstein = 'Zirkon'
    elif wert < 98: edelstein = 'Smaragd'
    elif wert < 99: edelstein = 'Saphir'
    elif wert < 100: edelstein = 'Rubin'
    elif wert < 101: edelstein = 'Diamant'

    return edelstein


def getGiftigePflanzen(wert):
    if wert < 2: pflanze = 'Rattenpilz'
    elif wert < 6: pflanze = 'Hollbeere'

    return pflanze


def getHeilpflanzen(wert):
    if wert < 5: pflanze = 'Donf'
    elif wert < 9: pflanze = 'Tarnele'
    elif wert < 13: pflanze = 'Wirselkraut'
    elif wert < 18: pflanze = 'Einbeere'

    return pflanze


def getNutzpflanzen(wert):
    if wert < 9: pflanze = 'Alraune'
    elif wert < 10: pflanze = 'Alveranie'
    elif wert < 11: pflanze = 'Messergras'
    elif wert < 16: pflanze = 'Carlog'
    elif wert < 21: pflanze = 'Egelschreck'
    elif wert < 26: pflanze = 'Gulmond'
    elif wert < 35: pflanze = 'Rahjalieb'

    return pflanze


def getTEGS(wert):
    if wert < 2: pflanze = 'Ghulgift'
    elif wert < 3: pflanze = 'Gonede'
    elif wert < 4: pflanze = 'Purpurblitz'
    elif wert < 5: pflanze = 'Schwarzer Lotos'
    elif wert < 7: pflanze = 'Unsichtbarkeitselixier'
    elif wert < 9: pflanze = 'Verwandlungselixier'
    elif wert < 11: pflanze = 'Boabungaha'
    elif wert < 13: pflanze = 'Feuerzunge'
    elif wert < 15: pflanze = 'Halbgift'
    elif wert < 18: pflanze = 'Rattenpilzgift'
    elif wert < 23: pflanze = 'Bannstaub'
    elif wert < 28: pflanze = 'Berserkerelixier'
    elif wert < 33: pflanze = 'Schwadenbeutel'
    elif wert < 38: pflanze = 'Brabacudagift'
    elif wert < 43: pflanze = 'Kelmon'
    elif wert < 48: pflanze = 'Kukris'
    elif wert < 53: pflanze = 'Visarnetgift'
    elif wert < 61: pflanze = 'Alchimistensäure'
    elif wert < 69: pflanze = 'Antidot'
    elif wert < 77: pflanze = 'Liebestrunk'
    elif wert < 85: pflanze = 'Schlaftrunk'
    elif wert < 93: pflanze = 'Wasserodem'
    elif wert < 101: pflanze = 'Zaubertrank'
    elif wert < 109: pflanze = 'Mandragora'
    elif wert < 117: pflanze = 'Marbos Ruhe'
    elif wert < 127: pflanze = 'Heiltrank'
    elif wert < 137: pflanze = 'Leuchtkreide'
    elif wert < 147: pflanze = 'Pastillen gegen Schmerzen'
    elif wert < 157: pflanze = 'Waffenbalsam'
    elif wert < 167: pflanze = 'Betäubungsgift'
    elif wert < 177: pflanze = 'Höhlenspinnengift'
    elif wert < 187: pflanze = 'Hollbeerenbrechmittel'
    elif wert < 197: pflanze = 'Höhlenbovistgift'

    return pflanze


#########
# Loot
#########
def loot_select(erg):
    loot = {
        # Außergewöhnliches
        1: {
            1: 'magisches Artefakt',
            2: 'leuchtender Gegenstand',
            3: '3 Abenteuerpunkte',
            4: 'unbekannter Gegenstand',
            'T': 'Außergewöhnliches'
        },
        2: {
            1: 'Zeitmessung',
            2: 'Lokalisationsinstrumente',
            3: 'Spiegel',
            4: 'Buch',
            5: 'Feinwerkzeug',
            6: 'Honig',
            7: 'Silberflöte',
            8: 'Lupe',
            9: 'Brennglas',
            10: 'Abakus',
            11: 'Trommel',
            12: 'Gravurwerkzeug',
            13: 'Fernrohr, klein',
            14: 'Fernrohr, aufschiebbar',
            15: 'Brille',
            16: 'Kristallkugel',
            17: 'Fanfare',
            18: 'Laute',
            19: 'Harfe',
            20: 'Alchemieset',
            'T': 'Besonderes'
        },
        3: {
            1: 'Banner, Wappen',
            2: 'Brief',
            3: 'Spezialität',
            4: 'Heimaterde',
            5: 'Selbstgebrautes',
            6: 'Wasserpfeife',
            'T': 'Regionales, Persönliches'
        },
        6: {
            1: 'Zähne',
            2: 'Haut, Leder',
            3: 'Pfoten, Ohren',
            4: 'Federn',
            5: 'Horn',
            6: 'alchemistische Zutat (Blut, Auge, Schwanz, Speichel)',
            'T': 'Tierisches'
        },
        7: {
            1: 'Salzfleisch',
            2: 'Dörrobst',
            3: 'Trockenobst',
            4: 'Körner',
            5: 'Wurst',
            6: 'Käse',
            'T': 'Nahrung, Verderbliches'
        },
        9: {
            1: 'Angelhaken',
            2: 'Schnur',
            3: 'Kohlestifte',
            4: 'Hufeisen',
            5: 'Leine',
            6: 'Sattel',
            7: 'Käfig',
            8: 'Fischernetz',
            9: 'Stundenglas',
            10: 'Kerzenständer',
            11: 'Pfeife',
            12: 'Tabakdose',
            13: 'Holzflöte',
            'T': 'Sonstiges, Kram'
        },
        10: {
            1: 'Korsett',
            2: 'Hemd, Bluse',
            3: 'Hose',
            4: 'Handschuhe',
            5: 'Kopfbedeckung',
            6: 'Socken',
            7: 'Unterkleidung',
            8: 'Gürtel ',
            9: 'Schuhe',
            10: 'Mantel, Weste',
            11: 'Jacke',
            12: 'Tuche',
            13: 'Pelze',
            14: 'Fell',
            15: 'Tunika',
            16: 'Umhang',
            17: 'Lederschürze mit Taschen',
            18: 'Horasiches Ballkleid, teuer',
            19: 'Stiefel',
            20: 'Robe',
            'T': 'Kleidung'
        },
        11: {
            1: 'Ring',
            2: 'Armband',
            3: 'Halskette',
            4: 'Fusskette',
            5: 'Stirmreif, Diadem',
            6: 'Ohrringe',
            7: 'Spangen',
            8: 'Fibel',
            9: 'Knopf',
            10: 'Fächer, Elfenbein und Seide',
            'T': 'Schmuck'
        },
        12: {
            1: 'Kohlestifte',
            2: 'Federkiele',
            3: 'Tusche',
            4: 'Lineal',
            5: 'Blatt',
            6: 'Pergament',
            7: 'Pinsel',
            8: 'Heft',
            9: 'Buch',
            10: 'Schriftrolle',
            11: 'Federmesser',
            12: 'Schiefertafel',
            13: 'Siegelwachs',
            'T': 'Schreibtischmaterial'
        },
        13: {
            1: 'Messer',
            2: 'Hammer',
            3: 'Säge',
            4: 'Zange',
            5: 'Brecheisen',
            6: 'Beil',
            7: 'Feile',
            8: 'Schere',
            9: 'Sichel',
            10: 'Hobel',
            11: 'Handschellen',
            12: 'Dreschflegel',
            13: 'Hammer',
            14: 'Spitzhacke',
            15: 'Spaten',
            16: 'Holzeimer',
            17: 'Tätowierwerkzeug',
            'T': 'Werkzeug'
        },
        14: {
            1: 'Figur',
            2: 'Puppe',
            3: 'Würfel',
            4: 'Holzwaffe',
            5: 'Jonglierball',
            6: 'Kartenspiel',
            7: 'Bild',
            8: 'Glöckchen',
            9: 'Brettspiel, Holz',
            'T': 'Spielzeug, Deko'
        },
        15: {
            1: 'Decke',
            2: 'Seil, 5 Schritt',
            3: 'Seil, 10 Schritt',
            4: 'Netz',
            5: 'Kette',
            6: 'Pflöcke',
            7: 'Zelt',
            8: 'Schlafsack',
            9: 'Wanderstab',
            10: 'Hängematte',
            11: 'Kletterhaken, 5',
            12: 'Wurfhaken',
            13: 'Nadel und Garn',
            14: 'Proviantpaket, 3 Tage',
            15: 'Strickleiter, 10 Schritt',
            16: 'Wundnähzeug',
            17: 'Verbände',
            18: 'Feldflasche',
            19: 'Wasserschlauch',
            20: 'Wolldecke, dick',
            'T': 'Reisebedarf'
        },
        16: {
            1: 'Seife',
            2: 'Öl (Reinigung)',
            3: 'Kamm',
            4: 'Schwamm',
            5: 'Schminke',
            6: 'Puder',
            7: 'Duftflächschen',
            8: 'Rasiermesser',
            9: 'Lippenrot',
            10: 'Bürste',
            'T': 'Körperpflege'
        },
        17: {
            1: 'Schatulle',
            2: 'Tasche',
            3: 'Gürteltasche',
            4: 'Sack',
            5: 'Beutel',
            6: 'Flasche',
            7: 'Rucksack',
            8: 'Salbendöschen',
            9: 'kleiner Rucksack',
            10: 'Umhängetasche',
            'T': 'Behälter'
        },
        18: {
            1: 'Becher',
            2: 'Teller',
            3: 'Besteckset',
            4: 'Schöpfkelle',
            5: 'Topf',
            6: 'Pfanne',
            7: 'Schlauch (Flüssigkeiten)',
            8: 'Brotbeutel',
            9: 'Bratspieß',
            10: 'Trinkhorn',
            'T': 'Geschirr'
        },
        19: {
            1: 'Kerze',
            2: 'Pechfackel',
            3: 'Öllampe',
            4: 'Lampenöl',
            5: 'Feuerstein & Stahl',
            6: 'Zunderkästchen',
            7: 'Laterne',
            8: 'Sturmlaterne',
            9: 'Stundenkerze',
            10: 'Kerzenleuchter',
            'T': 'Beleuchtung'
        },
        20: {
            1: 'Schwertscheide',
            2: 'Dolchscheide',
            3: 'Waffengurt (Wurfmesser)',
            4: 'Gehänge (Axt)',
            5: 'Köcher (Pfeile)',
            6: 'Wetzstahl',
            7: 'Waffenpflegeöl',
            8: 'Bogensehne',
            9: 'Köcher (Bolzen)',
            10: 'Schultergurt',
            11: 'Salbenfett',
            12: 'Armbrustsehne',
            'T': 'Waffenzubehör'
        },
    }

    return loot.get(erg, 'Kein  gültiger Wurf')


def zustand_select(erg):
    zustand = {
        1: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        2: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        3: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        4: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        5: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        6: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        7: {'schlecht, reparaturbedürftig, verbogen, fast leer'},
        8: {'gebraucht, nicht neu aber erhalten'},
        9: {'gebraucht, nicht neu aber erhalten'},
        10: {'gebraucht, nicht neu aber erhalten'},
        11: {'gebraucht, nicht neu aber erhalten'},
        12: {'gebraucht, nicht neu aber erhalten'},
        13: {'gebraucht, nicht neu aber erhalten'},
        14: {'gebraucht, nicht neu aber erhalten'},
        15: {'(fast) wie neu'},
        16: {'(fast) wie neu'},
        17: {'(fast) wie neu'},
        18: {'(fast) wie neu'},
        19: {'besonders schönes Stück, sehr gut erhalten'},
        20: {'besonders schönes Stück, sehr gut erhalten'}
    }

    return zustand.get(erg, 'Kein  gültiger Wurf')


def qualität_select(erg):
    qualität = {
        1: {
            'G': 'sehr klein, ein Karat',
            'V': 'einfach',
            'A': 1
        },
        2: {
            'G': 'sehr klein, ein Karat',
            'V': 'handwerklich gut',
            'A': 1
        },
        3: {
            'G': 'sehr klein, ein Karat',
            'V': 'einfach',
            'A': 2
        },
        4: {
            'G': 'sehr klein, ein Karat',
            'V': 'handwerklich gut',
            'A': 2
        },
        5: {
            'G': 'sehr klein, ein Karat',
            'V': 'meisterlich',
            'A': 1
        },
        6: {
            'G': 'klein, zwei Karat',
            'V': 'einfach',
            'A': 1
        },
        7: {
            'G': 'klein, zwei Karat',
            'V': 'handwerklich gut',
            'A': 1
        },
        8: {
            'G': 'klein, zwei Karat',
            'V': 'einfach',
            'A': 2
        },
        9: {
            'G': 'klein, zwei Karat',
            'V': 'handwerklich gut',
            'A': 2
        },
        10: {
            'G': 'klein, zwei Karat',
            'V': 'meisterlich',
            'A': 1
        },
        11: {
            'G': 'mittel, fünf Karat',
            'V': 'einfach',
            'A': 1
        },
        12: {
            'G': 'mittel, fünf Karat',
            'V': 'handwerklich gut',
            'A': 1
        },
        13: {
            'G': 'mittel, fünf Karat',
            'V': 'einfach',
            'A': 2
        },
        14: {
            'G': 'mittel, fünf Karat',
            'V': 'handwerklich gut',
            'A': 2
        },
        15: {
            'G': 'mittel, fünf Karat',
            'V': 'meisterlich',
            'A': 1
        },
        16: {
            'G': 'groß, zehn Karat',
            'V': 'einfach',
            'A': 1
        },
        17: {
            'G': 'groß, zehn Karat',
            'V': 'handwerklich gut',
            'A': 1
        },
        18: {
            'G': 'groß, zehn Karat',
            'V': 'einfach',
            'A': 2
        },
        19: {
            'G': 'groß, zehn Karat',
            'V': 'handwerklich gut',
            'A': 2
        },
        20: {
            'G': 'groß, zehn Karat',
            'V': 'meisterlich',
            'A': 1
        },
    }

    return qualität.get(erg, 'Kein  gültiger Wurf')


def karfunkel_select(erg):
    karfunkel = {
        1: {
            'G': 'Stecknadelkopf',
            'D': 'Baumdrachen',
            'A': 'jungen'
        },
        2: {
            'G': 'Stecknadelkopf',
            'D': 'Baumdrachen',
            'A': 'ausgewachsen'
        },
        3: {
            'G': 'Stecknadelkopf',
            'D': 'Baumdrachen',
            'A': 'uralten'
        },
        4: {
            'G': 'Erbsen',
            'D': 'Meckerdrachen',
            'A': 'jungen'
        },
        5: {
            'G': 'Erbsen',
            'D': 'Meckerdrachen',
            'A': 'ausgewachsen'
        },
        6: {
            'G': 'Erbsen',
            'D': 'Meckerdrachen',
            'A': 'uralten'
        },
        7: {
            'G': 'Erbsen',
            'D': 'Höhlendrachen',
            'A': 'jungen'
        },
        8: {
            'G': 'Erbsen',
            'D': 'Höhlendrachen',
            'A': 'ausgewachsen'
        },
        9: {
            'G': 'Erbsen',
            'D': 'Höhlendrachen',
            'A': 'uralten'
        },
        10: {
            'G': 'Daumenkuppen',
            'D': 'Westwinddrachen',
            'A': 'jungen'
        },
        11: {
            'G': 'Daumenkuppen',
            'D': 'Westwinddrachen',
            'A': 'ausgewachsen'
        },
        12: {
            'G': 'Daumenkuppen',
            'D': 'Westwinddrachen',
            'A': 'uralten'
        },
        13: {
            'G': 'Daumenkuppen',
            'D': 'Perldrachen',
            'A': 'jungen'
        },
        14: {
            'G': 'Daumenkuppen',
            'D': 'Perldrachen',
            'A': 'ausgewachsen'
        },
        15: {
            'G': 'Daumenkuppen',
            'D': 'Perldrachen',
            'A': 'uralten'
        },
        16: {
            'G': 'Hühnerei',
            'D': 'Kaiserdrachen',
            'A': 'jungen'
        },
        17: {
            'G': 'Hühnerei',
            'D': 'Kaiserdrachen',
            'A': 'ausgewachsen'
        },
        18: {
            'G': 'Hühnerei',
            'D': 'Kaiserdrachen',
            'A': 'uralten'
        },
    }

    return karfunkel.get(erg, 'Kein  gültiger Wurf')


def münzen_select(region):
    münzen = {
        'Bornland': {
            1: 'Deut',
            2: 'Groschen',
            3: 'Batzen'
        },
        'Vallusa': {
            1: 'Flindrich',
            2: 'Stüber',
            3: 'Witten'
        },
        'Horasreich': {
            1: 'Heller',
            2: 'Silber',
            3: 'Dukat'
        },
        'Bergkönigreich': {
            1: 'Atebrox',
            2: 'Arganbrox',
            3: 'Auromox'
        },
        'Xeraanien (schwarze Lande)': {
            1: 'Splitter',
            2: 'Zholvaro',
            3: 'Borbaradstaler'
        },
        'Oron (schwarze Lande)': {
            1: 'Heller',
            2: 'Silber',
            3: 'Dukat'
        },
        'Mhaharanyat Aranien': {
            1: 'Hallah',
            2: 'Schekel',
            3: 'Dinar'
        },
        'Kalifat': {
            1: 'Muwlat',
            2: 'Zechine',
            3: 'Marawedi'
        },
        'Großemirat Mengbilla': {
            1: 'Tessar',
            2: 'Telár',
            3: 'Dekat'
        },
        'Alanfanisches Imperium': {
            1: 'Dirham',
            2: 'Oreal',
            3: 'Dublone'
        },
        'Káhet Ni Kemi': {
            1: 'Chryskl',
            2: 'Hedsch',
            3: 'Suvar'
        }
    }

    return münzen.get(region, 'Kein  gültiger Wurf')


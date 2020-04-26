import discord
import os
import random
import dice
import re
import logging
import io
import aiohttp
import asyncio
import pandas as pd
import datetime
from collections import Counter
from keep_alive import keep_alive
from features import *
from loot import *
from kampf import *
from geld import *
from pflanzen import *
from time import sleep

# ToDo
# Schlimme Verletzungen https://ulisses-regelwiki.de/index.php/Fokus_Schlimme_Verletzungen.html
# (K)SF einbauen hinsichtlich Modifikationen AT/PA und Schaden
# Anzahl Verteidigungen
# Modifikationen aus Waffenlänge
#1. Mod AT
#2. Mod PA (inkl. Fähigkeiten des Angreifers)
#3. Schaden Modifikationen aus (K)SF
# Schmerzstufen
# :20: für 20er bei .e und .t


#https://ulisses-regelwiki.de/index.php/Alkohol_Regeln.html
#https://ulisses-regelwiki.de/index.php/OR_PruegelRegeln.html
#http://ulisses-regelwiki.de/index.php/Fokus_Trinkspiele.html

# logger = logging.getLogger('discord')
# logger.setLevel(logging.DEBUG)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %message)s'))
# logger.addHandler(handler)

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in...')
    print('Username: ' + str(client.user.name))
    print('Client ID: ' + str(client.user.id))
    print('Version: ' + discord.__version__)
    print('I am in ' + str(len(client.guilds)) + ' Guilds.')
    for server in client.guilds:
        print(' ', server)
        roleCounter = Counter()
        leiterList = []
        for member in server.members:
            for role in member.roles:
                roleCounter[str(role)] = +1
                if str(role) == 'Spielleiter':
                    leiterList.append(member.name)
        print('Vorhandene Rollen auf dem Guild sind:')
        print(list(roleCounter))
        print('User mit Rolle Spielleiter sind:')
        print(leiterList)
    print(' ', 'Invite URL: ' +
          'https://discordapp.com/oauth2/authorize?&client_id=' +
          str(client.user.id) + '&scope=bot&permissions=0')


@client.event
async def on_message(message):
	if message.author == client.user:
		return

	# leave guilds which are not specified
	elif message.content == ('.leaveguilds'):
		guild = client.guilds
		for g in guild:
			msg =  ('I will leave {0}').format(g)
			if g.name not in ('Die verphexte 20', 'KuhloTest'):
				await g.leave()
		await message.channel.send(msg)
		
    # Sag Hallo
	elif message.content == ('.hello'):
		msg = '{0} {1.author.mention}. Steig hinab in tiefe Dungeons voller Ungeheuer aus den Niederhöllen, oder erkunde fremde Sphären voller Magie... '.format(GetBegruessung(), message)
		await message.channel.send(msg)
    
		# Münzwurf
	elif message.content.lower() == ('.m'):
		msg = '{0.author.mention} hat {1} geworfen.'.format(message, getCoinFace())
		await message.channel.send(msg)

    # W6
	elif message.content.lower() == ('.w6'):
		msg = '{0.author.mention} hat {1} mit einem W6 geworfen.'.format(message, dice.roll('1d6'))
		await message.channel.send(msg)
    
    #Statistik
     # W6
	elif message.content.lower() == ('.sum(w6)'):
		ergebnis = dice.roll('600d6')
		b = {}
		for i in ergebnis:
			b[i] = b.get(i, 0) + 1
			ergebnis = sum(dice.roll('600d6'))
		msg = '{0.author.mention} hat {1} mit sechshundert W6 geworfen (Erwartungswert 2100). {2}'.format(message, ergebnis, b)
		await message.channel.send(msg)

    # W20
	elif message.content.lower() == ('.w20'):
		msg = '{0.author.mention} hat {1} mit einem W20 geworfen.'.format(
            message, dice.roll('1d20x'))
		await message.channel.send(msg)

	elif message.content.lower() == ('.t'):
		msg = '{0.author.mention} hat mit 3W20 gewürfelt: {1}'.format(
            message, dice.roll('3d20'))
		await message.channel.send(msg)

	elif message.content.lower() == ('.zechen'):
		msg = '{0.author.mention} möchte mal wieder zechen: {1}'.format(
            message, dice.roll('3d20'))
		await message.channel.send(msg)

#DSK  Katze
	elif message.content.lower() == ('.miau'):
		ergebnis = dice.roll('2d20')
		if sum(ergebnis) == 2:
			msg = '{0.author.mention} hat einen kritischen Erfolg geworfen. {1}'.format(message, ergebnis)
		elif sum(ergebnis) == 40:
			msg = '{0.author.mention} hat einen Patzer geworfen. {1}'.format(message, ergebnis)
		else:
			msg = '{0.author.mention} hat toll geworfen (Miau!). {1} / {2}'.format(message, ergebnis, sum(ergebnis))
		await message.channel.send(msg)

	elif message.content.lower().startswith('.mg('):

		if message.content.lower() == ('.mg(stand)'):
			stand = dskkontoabfrage(message.author.nick, message.author.id)
			msg = '{0.author.mention} du hast {1} Mondglöckchen in deiner Geldbörse :purse:!'.format(
                message, stand)
			await message.channel.send(msg)
			return

		else:
			anzahl = int(message.content[4:-1])
			print(anzahl)
			saldo = dskboerse(anzahl, message.author.nick, message.author.id)
			if anzahl > 0: 
				aktion_text = 'eingezahlt'
				artikel = 'in deine'
				emoji = ':inbox_tray:'
			elif anzahl < 0:
				aktion_text = 'ausgezahlt'
				artikel = 'aus deiner'
				emoji = ':outbox_tray:'
			else:
				aktion_text = 'Error!'
				artikel = 'Error!'

		msg = '{0}{1.author.mention} du hast {2} :purse: {3} Mondglöckchen {4}! Du hast {5} Mondglöckchen.'.format(
               emoji, message, artikel, abs(anzahl), aktion_text, saldo)

		await message.channel.send(msg)

# Patzer
	elif message.content.lower() == ('.patzer'):
        # Rolle 2W6
		wurf = sum(dice.roll('2d6'))
        # Adjustiere Nahkampf bei < 7 um +5 bei unbewaffnet
		wurf_unbewaffnet = wurf
		if wurf < 7: wurf_unbewaffnet += 5
        # Selektiere den richtigen Text
		msg_Attacke = patzer_select(wurf)['A']
		msg_Unbewaffnet = patzer_select(wurf_unbewaffnet)['A']
		msg_Parade = patzer_select(wurf)['P']
		msg_Fern = patzer_select(wurf)['F']
		msg_Magie = patzer_select(wurf)['M']
		msg_Götter = patzer_select(wurf)['G']
		msg = '{0.author.mention} du Held! Lauter Patzer mit einem Wurf von {1} mit 2W6: \n\nUnbewaffnet: {2} \n\nNahkampf: {3} \n\nParade: {4} \n\nFernkampf: {5} \n\nMagie: {6} \n\nLiturgien: {7}'.format(
            message, wurf, msg_Unbewaffnet, msg_Attacke, msg_Parade, msg_Fern,
            msg_Magie, msg_Götter)
		await message.channel.send(msg)


# Pflanzen
	elif message.content.lower() == ('.pflanzen'):
		ueberschriften_reg = ['Region', 'Kürzel']
		ueberschriften_ter = ['Terrain', 'Kürzel']
		ueberschriften_wet = ['Wetter', 'Modifikation']
		ueberschriften_mod = ['Terrain', 'Modifikation']

		table_reg = [['Nordlande', 'NO'], ['Thorwal', 'TH'], ['Bornland', 'BO'], ['Firnelfen', 'FI'], ['Au- und Waldelfen', 'EL'], ['Orkland', 'OR'], ['Weiden und Greifenfurt', 'WE'], ['Havena, Albernia, Windhag auch Nostria und Andergast', 'HA'], ['Zentrales Mittelreich', 'GA'], ['Eisenwald, Amboss und Kosch', 'EI'], ['Punin, Almada', 'PU'], ['Zentrales Horasreich', 'HO'], ['Zyklopeninseln', 'ZY'], ['Khomwueste', 'KH'], ['Mhanadistan und Aranien', 'MH'], ['Maraskan', 'MA'], ['Al’Anfa, Trahelien, Selem', 'AL'], ['Mohagebiete', 'MO'], ['Waldinseln', 'WA'], ['Tobrien', 'TO']]
		table_ter = [['Wald', 'WA'], ['Eis', 'EI'], ['Ebene', 'EB'], ['Flussauen', 'FL'], ['Gebirge', 'GE'], ['Moor', 'MO'], ['Hoehlen', 'HO'], ['Kueste', 'KU'], ['Wueste', 'WU']]
		table_wet = [['Regen/Schnee', -1], ['Sturm', -2], ['Orkan', -3], ['Sonstiges', 0]]
		table_mod = [['Dschungel', -2], ['Eiswüste', -5], ['Flussauen', -1], ['Gebirge', -1], ['Kulturland', 1], ['Steppe', 0], ['Sumpf', -1], ['Wald', 2],['Waldrand', 1], ['Wüste', -5], ['Wüstenrand', -3]]
		msg_1 = '{0.author.mention} Also du willst Pflanzen suchen? Gut, wir müssen ein paar Informationen sammeln. In welcher Region befindest du dich?'.format(message)
		msg_2 = 'Was ist das aktuelle Terrain?'
		msg_3 = 'Welche QS hast du nach folgenden Modifikationen in Pflanzenkunde?'
		msg_4 = 'Wetter Modifikationen:'
		msg_5 = 'Terrain Modifikationen:'
		msg_6 = '''{0.author.mention} Antworte mit: .pflanzen(Regions Kürzel,Terrain Kürzel,QS). Wenn du eine spezifische 
			Pflanze suchst kannst du dir mit .pflanzen(Regions Kürzel, Terrain Kürzel, 0) eine Liste
			ausgeben lassen. '''.format(message)

		await message.channel.send(msg_1)
		msg = '```\n' + prettyprintlist(table_reg, ueberschriften_reg) + '```'
		await message.channel.send(msg)

		await message.channel.send(msg_2)
		msg = '```\n' + prettyprintlist(table_ter, ueberschriften_ter) + '```'
		await message.channel.send(msg)

		await message.channel.send(msg_3)
		await message.channel.send(msg_4)
		msg = '```\n' + prettyprintlist(table_wet, ueberschriften_wet) + '```'
		await message.channel.send(msg)

		await message.channel.send(msg_5)
		msg = '```\n' + prettyprintlist(table_mod, ueberschriften_mod) + '```'
		await message.channel.send(msg)

		await message.channel.send(msg_6)

	elif message.content.startswith('.pflanzen('):
		region = message.content.upper()[10:12]
		terrain = message.content.upper()[13:15]
		QS = int(message.content[16])
		#print(region)
		#print(terrain)
		#print(QS)
		#print(type(QS))
		if region not in ['NO', 'TH', 'BO', 'FI', 'EL', 'OR', 'WE', 'HA', 'GA', 'EI', 'PU', 'HO', 'ZY', 'KH', 'MH', 'MA', 'AL', 'MO', 'WA', 'TO']:
			msg = '{0.author.mention} Keine gültige Regionenangabe'.format(message)
			await message.channel.send(msg)

		elif terrain not in ['WA', 'EI', 'EB', 'FL', 'GE', 'MO', 'HO', 'KU', 'WU']:
			msg = '{0.author.mention} Keine gültige Terrainangabe'.format(message)
			await message.channel.send(msg)
		else:
			plant_df = loadPflanzendf()
			plant_df = plant_df[plant_df['Kuerzel'] == region]
			plant_df = plant_df[plant_df.Aktiv == 1]
			plant_df = plant_df[plant_df[terrain] == 1]
			if QS == 0:
				plant_list = plant_df[['Pflanze', 'Suchschwierigkeit', 'Bestimmungsschwierigkeit', 'Link']].values.tolist()
				msg = '{0.author.mention} Es gibt folgende  Pflanzen. Teste bitte noch ob du diese auch findest und bestimmen kannst und wieviele Anwendungen du von deiner QS bekommst.'.format(message)
				msg_2 = '```\n'+  prettyprintlist(plant_list, ['Name', 'Suchschwierigkeit', 'Bestimmungschwierigkeit', 'Weblink']) + '```'
				await message.channel.send(msg)
				await message.channel.send(msg_2)

			else:
				anz_plants = plant_num(QS)
				#Implement here the selection of plants based on the numbers, differentiate the plants based on suchschwierigkeit
				plant_df['Wkeit'] = plant_df['Suchschwierigkeit'].apply(convert_suchschwierigkeit)
				sum_Wkeit = plant_df['Wkeit'].sum()
				plant_df['relWkeit'] = plant_df['Wkeit'].apply(relative_schwierigkeit, args=(sum_Wkeit,))
				plant_df['cumrelWkeit'] = plant_df['relWkeit'].cumsum()
				plant_df = plant_df.sample(n=anz_plants, weights = 'Wkeit', replace=True)
				plant_list = plant_df[['Pflanze','Bestimmungsschwierigkeit','Link']].values.tolist()
				msg = '{0.author.mention} Du findest {1} Pflanzen. Teste bitte noch ob du diese auch bestimmen kannst und wieviele Anwendungen du von deiner QS bekommst.'.format(message, anz_plants)
				msg_2 = '```\n' +  prettyprintlist(plant_list, ['Name', 'Schwierigkeit', 'Weblink']) +  '```'
				await message.channel.send(msg)
				await message.channel.send(msg_2)

# Loot	

	elif message.content.lower() == ('.loot'):
        # Rolle Erstwurf um 66% Wahrscheinlichkeit auf Wertvolles (und dort 50% auf Münzen zu geben), ansonsten 1W20 für andere Dinge
		erstwurf = sum(dice.roll('1d6'))
		#print(erstwurf)
		if erstwurf < 5: 
			wurf_kategorie = 4
		else:
			wurf_kategorie = sum(dice.roll('1d20'))
		#print (wurf_kategorie)
		
        # Zum testen der einzelnen Kategorien
        #wurf_kategorie = 8

        # Weiche für verschiedene Ergebnisse

        # Geld, Wertvolles 4
		if wurf_kategorie == 4 :
			stoff = getWertvolles()

			if stoff == 'Kleingeld':
				verteilung = getMünzVerteilung()
				gut = 'eine Ansammlung von Münzen mit {0} Dukaten {1} Silber sowie {2} Heller aus dem Mittelreich'.format(
                    verteilung[0], verteilung[1], verteilung[2])

			elif stoff == 'Kleingeld (Fremdwährung)':
				münzRegion = getFremdmünzen(sum(dice.roll('1d110')))
				münzen = münzen_select(münzRegion)
				verteilung = getMünzVerteilung()
				gut = 'eine Ansammlung von Münzen mit {0} {1}, {2} {3} sowie {4} {5} aus dem {6}'.format(
                    verteilung[0], münzen[3], verteilung[1], münzen[2],
                    verteilung[2], münzen[1], münzRegion)

			elif stoff == 'schöne Steine':
				qualität = qualität_select(sum(dice.roll('1d20')))
				gut = '{0} {1} gearbeitete schöne Steine in Größe {2}'.format(
                    qualität['A'], qualität['V'], qualität['G'])

			elif stoff == 'Edelsteine':
				wurf = sum(dice.roll('1d100'))
				qualität = qualität_select(sum(dice.roll('1d20')))
				gut = '{0} {1} gearbeitete {2} in Größe {3}'.format(
                    qualität['A'], qualität['V'], getEdelsteine(wurf),
                    qualität['G'])

			elif stoff == 'Pokal':
				qualität = qualität_select(sum(dice.roll('1d20')))
				gut = '{0} {1} gearbeitete Pokale in Größe {2}'.format(
                    qualität['A'], qualität['V'], qualität['G'])

            # Als Kategorie enthalten, wird aber nicht ausgewählt durch getWertvolles()
			elif stoff == 'Karfunkel':
				qualität = karfunkel_select(sum(dice.roll('1d18')))
				gut = 'ein {0} großer Karfunkel eines {1} {2}'.format(
                    qualität['G'], qualität['A'], qualität['D'])

			msg = '{0.author.mention} findet {1}! Bei näherer Betrachtung glaubt er, dass es {2} ist/sind.'.format(
                message, stoff, gut)

        # Bau- und Rohstoffe 5
		elif wurf_kategorie == 5:
			stoff = getMetallRohstoffe()
			if stoff == 'Metalle':
				wurf = sum(dice.roll('1d99'))
				gut = getMetalle(wurf)
			elif stoff == 'Hölzer':
				wurf = sum(dice.roll('1d100'))
				gut = getHölzer(wurf)
			elif stoff == 'Minerale':
				wurf = sum(dice.roll('1d100'))
				gut = getMinerale(wurf)
			else:
				gut = 'Bein'
			msg = '{0.author.mention} findet {1}! Bei näherer Betrachtung glaubt er, dass es {2} ist.'.format(
                message, stoff, gut)

        # Kräuter, Tränke, Elixiere 8
		elif wurf_kategorie == 8:

            # Konstruiere Liste der Spielleiter:
			leiterList = []
			for member in message.guild.members:
				for role in member.roles:
					if str(role) == 'Spielleiter':
						leiterList.append(member.id)
			stoff = getKräuterTränkeElixire()

			if stoff == 'Giftpflanze':
				wurf = sum(dice.roll('1d5'))
				gut = 'Pflanze'
				gut_secret = getGiftigePflanzen(wurf)

			if stoff == 'Heilpflanze':
				wurf = sum(dice.roll('1d17'))
				gut = 'Pflanze'
				gut_secret = getHeilpflanzen(wurf)

			if stoff == 'Nutzpflanze':
				wurf = sum(dice.roll('1d33'))
				gut = 'Pflanze'
				gut_secret = getNutzpflanzen(wurf)

			if stoff == 'Tabak':
				gut = stoff

			if stoff == 'Tränke, Elixiere, Gifte & Salben':
				wurf = sum(dice.roll('1d196'))
				gut = getTEGS(wurf)

			if len(leiterList) == 0:
				msg = 'Bitte legt die Rolle <Spielleiter> auf dieser Discord Guilde an und gebt mindestens einem User diese Rolle!'
			else:
				if gut == 'Pflanze':
					msg_secret = '{0.author.mention} findet {1}! Bei näherer Betrachtung glaubt er, dass es {2} ist.'.format(
                        message, stoff, gut_secret)
					for leiter in leiterList:
						recipient = message.guild.get_member(leiter)
						await client.send_message(recipient, msg_secret)
					msg = '{0.author.mention} findet eine Pflanze.'.format(
                        message)
				else:
					msg = '{0.author.mention} findet {1}! Bei näherer Betrachtung glaubt er, dass es {2} ist.'.format(
                        message, stoff, gut)

        # Andere Kategorien	
		else:
            #Ermittle Anzahl Gegenstände einer Kategorie und würfle einen Wx
			Int_len_dict_klasse = len(loot_select(wurf_kategorie)) - 1
			Str_wurf_gegenstand = '1d{0}'.format(Int_len_dict_klasse)
			Int_wurf_gegenstand = sum(dice.roll(Str_wurf_gegenstand))
            # Ermittle Text des Gegenstands
			msg_loot = loot_select(wurf_kategorie)[Int_wurf_gegenstand]
            # Ermittle Zustand
			zustand_wurf = sum(dice.roll('1d20'))
			zustand_msg = zustand_select(zustand_wurf)
			msg = '{0.author.mention} findet etwas mit einer {1} mit 1W20! Es ist aus der Kategorie {2} und zwar ein {3} (bei einer {4} mit 1W{5}). Es befindet sich im Zustand {6}.'.format(
                message, wurf_kategorie,
                loot_select(wurf_kategorie)['T'], msg_loot,
                Int_wurf_gegenstand, Int_len_dict_klasse, str(zustand_msg))

		await message.channel.send(msg)

	elif message.content.lower() == ('.prügeln'):
        # http://www.ulisses-regelwiki.de/index.php/OR_PruegelRegeln.html
        #msg =
        # Rolle 2W6
		wurf = sum(dice.roll('2d6'))
        # Selektiere den richtigen Text
		msg_Verletzung = verletzung_select(wurf)['T']
		msg_Schaden = verletzung_select(wurf)['L'] * 100
		msg = '{0.author.mention} du Rüpel! {1}. Mit 2W6 würfelst du {2}. Du bekommst {3}% deiner Prügelpunkte als Schaden. '.format(
            message, msg_Verletzung, wurf, msg_Schaden)
		await message.channel.send(msg)

	elif message.content.lower() == ('.e'):
		msg = '{0.author.mention} hat eine Eigenschaftsprobe versucht: {1}'.format(
            message, dice.roll('1d20x'))
		await message.channel.send(msg)
        
	elif message.content.lower() == ('.paschok'):
		wurf = sorted(dice.roll('2d6'), reverse=True)
		print(wurf)
		wurf = int(str(wurf[0]) + str(wurf[1]))

		msg = '||{0.author.mention} hat bei Paschok gewürfelt: {1}||'.format(
            message, wurf)
		await message.channel.send(msg)

	elif message.content.lower().startswith('.timer('):
		length  = int(message.content[7:-1])
		await message.delete()
		await asyncio.sleep(length)
		msg = '@everyone Satinav blickt auf euch herab, entscheidet euch schnell!'
		await message.channel.send(msg)

    # Ziehe eine Karte
	elif message.content.lower().startswith('.karte('):
        # Parse die Kategorie
		kat = message.content[7:-1]
        # Ermittle die URL
		kartenurl = getKarten(kat)
        # Lade das Bild als BytesIO Objekt
		async with aiohttp.ClientSession() as session:
			async with session.get(kartenurl) as resp:
				if resp.status != 200:
					await message.channel.send('Could not download file...')
				data = io.BytesIO(await resp.read())
                #Schicke die Nachricht ab und beginne mit SPOILER_ um das Bild mit Spoiler zu maskieren (analog || ||, was bei Bildern nicht funktioniert). Benennung anschließend mit dem String aus URL
				await message.channel.send(file=discord.File(data, "SPOILER_" + kat + kartenurl[-6:]))

    # zahle Geld in die Börse ein, hebe ab oder deponiere auf die Bank
# für den geldbeutel und bank hmm :classical_building:
	elif message.content.lower().startswith('.geld('):

		if message.content.lower() == ('.geld(alle)'):
			gesamtliste = str(list(gesamtkonten()))
            #gesamtliste = prettyprintlist(str(gesamtliste))
			msg = '```\n' + gesamtliste + '```' 
			await message.channel.send(msg)
			return

		elif message.content.lower() == ('.geld(stand)'):
			stand = kontoabfrage(message.author.nick, message.author.id)
			beutelsaldo = cleansaldo(stand[0])
			kontosaldo = cleansaldo(stand[1])
			msg = '{0.author.mention} du hast Münzen im Wert von {1} Dukaten, {2} Silber und {3} Heller in deiner Geldbörse :purse:! Auf deinem Konto :classical_building: befinden sich Münzen im Wert von {4} Dukaten, {5} Silber und {6} Heller.'.format(
                message, int(beutelsaldo[0]),int(beutelsaldo[1]), int(beutelsaldo[2]), int(kontosaldo[0]), int(kontosaldo[1]), int(kontosaldo[2]))
			await message.channel.send(msg)
			return



		daten = message.content[6:-1].split(',')
		aktion = daten[0]
		anzahl = int(daten[1])
		try: 
			desc = daten[2]
		except:
			desc = ''
		kontostand = getboerse(aktion, anzahl, message.author.nick, message.author.id, desc)
		if aktion == 'g':
			ort = ['Geldbörse', 'Münzbestand']
			emojiort = ':purse:'
			saldo = int(kontostand[0])
		elif aktion == 'b':
			ort = ['Bank', 'Kontostand']
			saldo = int(kontostand[1])
			emojiort = ':classical_building:'
		if anzahl > 0: 
			aktion_text = 'eingezahlt'
			artikel = 'in deine'
			emoji = ':inbox_tray:'
		elif anzahl < 0:
			aktion_text = 'ausgezahlt'
			artikel = 'aus deiner'
			emoji = ':outbox_tray:'
		else:
			aktion_text = 'Error!'
			artikel = 'Error!'
        
		msg = '{0}{1.author.mention} du hast {2} {3} {4} Heller {5}! In deiner {6} {7} befinden sich Münzen im Wert von {8} Heller.'.format(
               emoji, message, artikel, ort[0], abs(anzahl), aktion_text, ort[0], emojiort, saldo)

		await message.channel.send(msg)


	elif message.content.lower() == ('.geld(transaktionen)'):
		t = transaktionen(message.author.nick, message.author.id)
		msg = t
		await message.channel.send(t)

	elif message.content.lower() == ('.v'):
		await message.channel.send('https://discordapp.com/channels/533654269442785290/533654269895639040')

	elif message.content.lower().startswith('.p('):
		if message.content.lower().startswith('.p(e,'):
            # Parse den Eigenschaftswert
			IntEigList = [int(x) for x in re.findall('\d+', message.content)]
			msg = '{0.author.mention} deine Eigenschaftsprobe hat eine Erfolgswahrscheinlichkeit von {1}% - ein Patzer hat eine Wahscheinlichkeit von {2}%'.format(
                message, IntEigList[0] / 20 * 100,
                (0.05 * ((20 - IntEigList[0]) / 20) * 100))

			await message.channel.send(msg)

		elif message.content.lower().startswith('.p(t,'):
			IntEigList = [int(x) for x in re.findall('\d+', message.content)]
			print(IntEigList)
			msg = '{0.author.mention} deine Talentprobe hat eine Erfolgswahrscheinlichkeit von {1}%'.format(
                message,
                round(
                    pEigenschaft(IntEigList[0], IntEigList[1], IntEigList[2],
                                 IntEigList[3]) * 100, 1))

			await message.channel.send(msg)

	elif (message.content.lower() == ('.h')
          or message.content.lower() == ('.help')):
		msg = '{0.author.mention} \ndie Arcanomechanische Manufactur hat mich mit folgenden Funktionen ausgestattet: \n\n:wave:\n.hello: Derische Grüße! \n\n:notes:\n Ich habe RythmBot versklavt Musik für dich zu spielen  \n\n:moneybag:\n.m: Bereit für einen Münzwurf? (Kopf, Pferd) \n\n:muscle:\n.t: Wirf 3W20 für eine Talentprobe \n\n.e Wirf einen W20 für eine Eigenschaftsprobe (wirft einen weiteren W20 bei einer 20) \n\n:ghost:\n.r: Ein legendärer Held wird zufällig erwählt um packende Abenteuer zu erleben... oder in eine Grube voller Speerspitzen zu fallen (selektiert keine Offline Spieler, Bots oder den Meister)  \n\n:dollar:\n.loot: Meeeiiiin Schaaatz. \n\n:facepalm:\nSchon wieder gepatzt? .patzer hilft - großes Ehrenwort.\n\nMal wieder geprügelt? .prügeln lässt dich in den Spiegel schauen. \n\n:bar_chart: \n.p(e, E): Erfahre die Erfolgswahrscheinlichkeit einer Eigenschaftsprobe bei Eigenschaftswerten von En \n\n.p(t, E1, E2, E3, TaW): Ich knoble dir deine Chancen für einen Erfolg bei einer Talentprobe aus! \n\n:game_die: \n.rNwX: Du willst Würfeln? Gib mir N und ich würfle dir diese auf X-seitigen Würfeln. Sei aber nachher nicht enttäuscht... \n\n.w6 und .w20 funktionieren aber auch \n\n:date:\n .wochentag hilft dir, wenn du das Datum vergessen hast.'.format(
            message)
		await message.channel.send(msg)

	elif message.content.startswith('.stat'):
		ergebnis = dice.roll('100000d20')
		b = {}
		for i in ergebnis:
			b[i] = b.get(i, 0) + 1

		await message.channel.send(b)

	elif message.content.lower() == ('.steigern'):
		tables = getSteigerung()
		msg = '```\n' + tables + '```'  
		await message.channel.send(msg)

	elif message.content.lower() == ('.aspekte'):
		tables = getAspekte()
		msg = '```\n' + tables + '```'  
		await message.channel.send(msg)

	elif message.content.lower() == ('.kampf'):
		b = 'Du willst einen Kampf starten? Kein Problem, der Meister füllt kurz die Gegnerliste und mit ".kampf start" startet der Fight!'
		await message.channel.send(b)

	elif message.content.lower() == ('.kampf start'):
        # unpin last pin
		pins = await message.channel.pins()
		try:
			last_pin = pins[-1]
			await last_pin.unpin()
		finally:
			a, b = ermittleInitative()
			a = prettyprintDF(a)
			msg = '```\n' + a + '```'  
			await message.channel.send(msg)
            # pin new message
			time.sleep(1)
			new_msg = await message.channel.fetch_message(message.channel.last_message_id)
			await new_msg.pin()

	elif message.content.lower() == ('.kampf runde'):
        #rundenzähler += 1
		kampfwerte = pd.read_csv(filepath_or_buffer='kampfdf.csv')
		msg = 'Neue Kampfrunde, setze alle AT/PA Zähler zurück.'
		kampfwerte['A AT'] = 0
		kampfwerte['A PA'] = 0
		kampfwerte['Runde'] += 1
		kampfwerte.to_csv(path_or_buf='kampfdf.csv', sep=',', header=True, index=False)
		await message.channel.send(msg)

    # Sybtax .a(IDAngreifer, IDVerteidiger, Modifikation durch (K)SF, Sicht aber ohne Zone, Zone[opt])
	elif message.content.lower().startswith('.a('):
        # Check if string is okay
		strAngriff = message.content[3:-1].split(',')
		print('Attacke Parameter')
		print(strAngriff)
        #print(len(strAngriff))
		if not 2 < len(strAngriff) < 5: await message.channel.send('Bitte als .a(IDAngreifer, IDVerteidiger, Modifikation durch (K)SF & Waffenlänge & Sicht aber ohne Zone , Zone[opt] angeben')
        #print(kampfwerte)
        #Read CSV
		kampfwerte = pd.read_csv(filepath_or_buffer='kampfdf.csv')
        # Name des Angreifers und Verteidiger
		nameAngreifer = kampfwerte.loc[kampfwerte['ID']==int(strAngriff[0]), 'Char'].item()
		nameVerteidiger = kampfwerte.loc[kampfwerte['ID']==int(strAngriff[1]), 'Char'].item()
        # Test für Attacke
		ergebnis = attacke(strAngriff[0],strAngriff[1],strAngriff[2] ,strAngriff[3])
        # Attacke erfolgreich
		if ergebnis[0] == True:
            # Halbierung PA, wenn Attacke mit einer 1
			if ergebnis[2] == True:
				print('PA Wert halbiert')
				verteidigung = parade(strAngriff[0],strAngriff[1],strAngriff[2], 2)
				msg_Attacke = '{0.author.mention}: {1} greift erfolgreich mit einer **{2}** kritisch an.'.format(message, nameAngreifer, ergebnis[1])
			else:
				verteidigung = parade(strAngriff[0],strAngriff[1],strAngriff[2], 1)
				msg_Attacke = '{0.author.mention}: {1} greift erfolgreich mit einer **{2}** an.'.format(message, nameAngreifer, ergebnis[1])
            # verteidigung
			if verteidigung[0] == True:
                # kritisch verteidigt
				if verteidigung[2] == True: 
					msg_Verteidigung = 'Das Ziel {0} verteidigt erfolgreich bestätigt kritisch (**{1}**) und bekommt einen Passierschlag.'.format(nameVerteidiger, verteidigung[1])     
                # normal verteidigt
				elif verteidigung[2] == False:
					msg_Verteidigung = 'Das Ziel {0} verteidigt erfolgreich (**{1}**).'.format(nameVerteidiger, verteidigung[1])
			elif verteidigung[0] == False:
				try: 
					zone = strAngriff[3]
				except IndexError: 
					zone = str(0)
				finally:         
					schadenswurf = attacke_schaden(strAngriff[0], strAngriff[1], zone)
                    #Bestätigter kritischer Angriff
					if ergebnis[3] == True: 
						damage = int(schadenswurf[0]) * 2
						msg_Attacke = msg_Attacke[:-3] + 'bestätigt an.'
                    # Bestätigter Verteidigungspatzer
					if verteidigung[3] == True:
						damage = int(schadenswurf[0])
						msg_Verteidigung = 'Das Ziel {0} **patzt** bestätigt (**{1}**) und bekommt **{2}** TP in der Trefferzone **{3}**.'.format(nameVerteidiger, verteidigung[1], damage, schadenswurf[1])
                    # Verteidigung ohne Patzer
					else:
						damage = int(schadenswurf[0])
						msg_Verteidigung = 'Das Ziel {0} verteidigt nicht (**{1}**) und bekommt **{2}** TP in der Trefferzone **{3}**.'.format(nameVerteidiger, verteidigung[1], damage, schadenswurf[1])
			msg = msg_Attacke + ' ' + msg_Verteidigung 
        # Attacke nicht erfolgreich (vorheriges if) und bestätigter Patzer
		elif ergebnis[3] == True:
			msg_Attacke = '{0.author.mention}: {1} schlägt mit einem bestätigten Patzer (**{2}**) daneben.'.format(message, nameAngreifer, ergebnis[1])
			msg = msg_Attacke
        # kein Erfolg, aber auch kein Patzer
		elif ergebnis[0] == False:
			msg_Attacke = '{0.author.mention}: {1} schlägt mit einer **{2}** daneben.'.format(message, nameAngreifer, ergebnis[1])
			msg = msg_Attacke
		await message.channel.send(msg)

	elif message.content.lower() == ('.r'):

        # Construct the list
		activeUser = []
        # Iterate through all online members which are not a bot
		for member in message.channel.members:
			if member.status != discord.Status.offline:
                #if member.bot == 'False':
				if member.name not in ('DSADiceBot', 'Rythm', 'MEE6'):
					if discord.utils.get(
                            member.roles, name='Freunde') == None:
						if discord.utils.get(
                                member.roles, name='Spielleiter') == None:
							if member.nick == None: activeUser.append(member.name)
							else: activeUser.append(member.nick)
		msg = 'Ich habe {0} tapfere Recken gefunden! Der von {1.author.mention} erwählte ist: {2}!'.format(
            len(activeUser), message, random.choice(activeUser))

		await message.channel.send(msg)

    # Sammelprobe
	elif message.content.lower().startswith('.sammelprobe'):
		qs = message.content[13:-1]
		print(qs)
          
    # Gebe zufälligen Wochentag aus	
	elif message.content.lower().startswith('.wochentag'):
		msg = 'Heute ist {0}.'.format(getTag())
		await message.channel.send(msg)

    #Sammle alle Nachrichten gem. Kriterien
	elif message.content.lower().startswith('.fetch('):
        #tupel = message.content[7:-1].split(',')
		messagelist = await message.channel.history(limit=None, before=None, after=datetime(2019,5,1)).flatten()
		print(messagelist[0])
		messagedf = pd.DataFrame(messagelist)
		print('sucess')
		messagedf.to_csv(path_or_buf='msg.csv', sep=',', header=True, index=False)
		print('.csv erstellt')

	elif message.content.lower().startswith('.'):
        # Get the number of dice
		IntNbrDice = re.search('\d+', message.content).group()
        # Get the sides of the dice
		IntSideDice = re.search('\d+$', message.content).group()
		if IntNbrDice.isdigit():
			if IntSideDice.isdigit():
                # Build the dice string
				StrDice = '{0}d{1}'.format(IntNbrDice, IntSideDice)
                # Build the message string
				msg = '{0.author.mention} hat mit {1}W{2} gewürfelt: {3}'.format(
                    message, IntNbrDice, IntSideDice, dice.roll(StrDice))
		await message.channel.send(msg)

keep_alive()

token = open('token.txt', 'r').readline()
client.run(token)

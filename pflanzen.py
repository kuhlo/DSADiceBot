import discord
import dice
import random
from kampf import *




######
#Funktion für ermittlung der Anzahl der Pflanzen
######

def plant_num(QS):
	if QS == 1:
		return 1
	elif QS == 2:
		return  1 + propability(33)
	elif QS == 3:
		return 1 + propability(50) + propability(33)
	elif QS == 4:
		return 1 + propability(66) + propability(50)
	elif QS == 5:
		return 1 + propability(75) + propability(50) + propability(33)
	elif QS == 6:
		return 1 + 1 + propability(50) + propability(33)

def propability(percentage):
	if  random.randrange(100) <  percentage:
		return 1
	else:
		return 0

def convert_suchschwierigkeit(suchschwierigkeit):
	return int(suchschwierigkeit * 10 + 100)

def relative_schwierigkeit(Wkeit, gesamtWkeit):
	return float(Wkeit / gesamtWkeit)

#def select_plants(df, anzahl):
	#return random.choices(df['Pflanzen'], weigths=df['Wkeit'], k=anzahl)


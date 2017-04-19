# coding: utf-8
# 2017 Jean-Hugues Roy, GNU GPL v3.
# Script basé sur l'explication de géomoulinette

import csv, os, glob, json, requests


entetes = {
    # user agent, habituellement le nom du navigateur, peut être changé par notre nom. nous nous annonçons. Fontions internes au protocole web http.
    "User-Agent" : "Geneviève Jetté - Requête pour mon cours EDM5240",
    "From" : "genevieve.jette1@gmail.com",
}


fichier1 = "CARTO_murales.csv"
fichier2 = "{}-geoocodeSVENNJETTÉ.csv".format(fichier1[:-4])
f1 = open(fichier1)
geo = csv.reader(f1)
next(geo)

# Cette fonction sert à passer à la ligne suivante, en mettant en ordre les lignes dans le .csv
n = 0


# On lit ensuite chacune des lignes de notre fichier pour aller chercher les colonnes que l'utilisateur a identifiées
for ligne in geo:
	n += 1
	lat = ligne[7]
	long = ligne[8]


# On utilise l'API de Google Maps pour géocoder l'adresse (en trouver les coordonnées)
# Dans la dernière portion de l'url, on doit mettre les informations qu'on a, pour nous donner quelque chose qu'on n'a pas
# Dans le script de géomoulinette, on avait l'adresse, mais maintenant je n'ai que la latitude et la longitude, donc on l'inscrit
	url = "https://maps.googleapis.com/maps/api/geocode/json?latlng=" + lat +","+ long + "&&language=fr"
	# print(url)
	req = requests.get(url)
	google = req.json()
	if len(google["results"]) != 0:
			# : [{ "types" : "sublocality_level_1" } ]]
			# sublocality = donnée de l'arrondissement dans l'api Google 
      # parfois, cette donnée apparaît en position 3 du premier ensemble de la request
      # parfois elle apparaît en 2ème position, donc mettre les deux entre crochets pour être certain
			
			if "sublocality_level_1" in google["results"][0]["address_components"][3]["types"]:
				arrondissement = google["results"][0]["address_components"][3]["long_name"]
				print(arrondissement)
				# On ajoute les coordonnées à chaque ligne du fichier
				ligne.append(arrondissement)
     
     # s'il n'y a rien, on passe à la prochaine ligne
     
			else:
				pass
				if "sublocality_level_1" in google["results"][0]["address_components"][2]["types"]:
					arrondissement = google["results"][0]["address_components"][2]["long_name"]
					print(arrondissement)
					# On ajoute les coordonnées à chaque ligne du fichier
					ligne.append(arrondissement)
				else:
					pass
	else:
		arrondissement = "?"
   

# On écrit notre nouveau fichier une ligne à la fois
# writerow = pour que les nouvelles données se trouvent à la dernière colonne
	yo = open(fichier2,"a")
	yolo = csv.writer(yo)
	yolo.writerow(ligne) 

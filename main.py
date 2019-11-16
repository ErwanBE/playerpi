# coding:utf-8
"""
To do list
Envoyer fichier log du player et l'envoyer sur le serveur
Créer playlist de lecture
Créer interface de configuration (Heure de début, nom du player etc ... )
Zipper les échanges en le player et serveur FTP
Créer des classes "Player, fichiers"
"""



import os
import time
import threading
from socket import *
import re
import subprocess



player_name = "player1"
jours = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
horsdiff = 'feh -F -z -D 5 Contenu/'
cmd = "bash /home/pi/Desktop/Contenu/config/MAJFTP.sh"
cmd1 = "wget http://checkip.dyndns.org -O - -o /dev/null | cut -d : -f 2 | cut -d \< -f 1"
cmd_image = "feh -F -z -D"
aujourdhui = jours[time.localtime()[6]]
heure = time.localtime()[3]
heure_debut = 7
heure_fin = 19
temps_MAJ = 600
lecture_active = 1
delay ='10'
dateandhourformat ="{}:{}:{} @ {}:{}:{}".format(time.localtime()[2],time.localtime()[1],time.localtime()[0],time.localtime()[3],time.localtime()[4],time.localtime()[5])

def lectureparjour():

    defaut_path = "/home/pi/Desktop/Contenu/"
    if heure_debut < heure < heure_fin:
        if time.localtime()[6] <5:
            subprocess.run(cmd_image+" "+delay+" "+defaut_path+aujourdhui,shell=True,check=True)
        else:
            subprocess.run(horsdiff, shell=True, check=True)

    else:
        subprocess.run(horsdiff,shell=True,check=True)


def majftp():
    excution = 1
    while excution == 1:
        subprocess.run(cmd,shell=True)
        print('mise à jour faite')
        time.sleep(temps_MAJ)


def sendIPadress():

    output = subprocess.run(cmd1,shell=True,capture_output=True)
    #output = "CompletedProcess(args='wget http://checkip.dyndns.org -O - -o /dev/null | cut -d : -f 2 | cut -d \\\\< -f 1', returncode=0, stdout=b' 92.170.36.17\\n', stderr=b'')"
    pattern = re.compile(r'[0-9][0-9]*.[0-9][0-9]*.[0-9][0-9]*.[0-9][0-9]*')
    myipadress = re.findall(pattern, str(output))
    myipadressformat = "{} : nom du player: {} Ip public: {}\n".format(dateandhourformat, player_name, myipadress[0])
    log = open("log.txt","a")
    log.write(myipadressformat)
    log.close()

    return myipadress[0]

    # écrire dans un fichier la variable puis l'envoyer sur le FTP
sendIPadress()
th1 = threading.Thread(target=lectureparjour)
th2 = threading.Thread(target=majftp)

th1.start()
th2.start()

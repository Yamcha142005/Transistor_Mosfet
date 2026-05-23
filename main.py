import numpy as np
from losses import switching_losses
from plot import plot_losses, plot_temp
from thermal import junction_temperature

#Grandeur électriques (tension et intensité)
#-------------------------------------------
V = 12 #Volts
I = 0.5 #Ampères

#-------------------------------------------

#Temps de commutation transistor en secondes(cas du TIP122)
#-------------------------------------------
transistor_tr = 200e-9 #temps de monté
transistor_tf = 500e-9 #temps de descente
#-------------------------------------------

#Temps de commutation mosfet en secondes(cas du IRLZ44N)
#-------------------------------------------
mosfet_tr = 84e-9 #temps de monté
mosfet_tf = 15e-9 #temps de descente
#-------------------------------------------

#Paramètres thermiques des composants
#-------------------------------------------
Ta = 25 #Température ambiante en degré celsisus
Tc_transistor = 150 #Température critique du transistor en degré celsisus
Rth_transistor = 62.5 #en degré celsisus par watt
Rth_mosfet = 62 #en degré celsisus par watt
#-------------------------------------------

#Tableau pour stocker les valeur des pertes par commutation
#-------------------------------------------
transistor_losses = []
mosfet_losses = []
#-------------------------------------------

#Tableau pour stocker les valeur des températures
#-------------------------------------------
transistor_temperatures = []
mosfet_temperatures = []
#-------------------------------------------

frequencies = np.linspace(1000, 1000000, 1000) #Valeurs de fréquence sur 100 points réparties uniformément

#Calcul des pertes et de la température en fonction des fréquences
#-------------------------------------------
for f in frequencies:
    transistor_loss = switching_losses(V, I, transistor_tr, transistor_tf, f)
    mosfet_loss = switching_losses(V, I, mosfet_tr, mosfet_tf, f)

    transistor_temperature = junction_temperature(Ta, transistor_loss, Rth_transistor)
    mosfet_temperature = junction_temperature(Ta, mosfet_loss, Rth_mosfet)

    transistor_losses.append(transistor_loss)
    mosfet_losses.append(mosfet_loss)

    transistor_temperatures.append(transistor_temperature)
    mosfet_temperatures.append(mosfet_temperature)

#-------------------------------------------

#Tracé des graphiques
#-------------------------------------------
programme = True
while(programme):
    choix = 0

    while choix not in [1, 2, 3]:
        print("Choisissez le graphe à afficher :")
        print("1 - Graphes des pertes")
        print("2 - Graphes de températures")
        print("3 - Arrêtez le programme")

        try:
            choix = int(input("Choix : "))
        except ValueError:
            print("Veuillez entrer un nombre valide.")


    if choix == 1:
        plot_losses(frequencies, transistor_losses, mosfet_losses) #Graphes de pertes
    elif choix == 2:
        plot_temp(frequencies, transistor_temperatures, mosfet_temperatures) #Graphes de températures
    else:
        programme = False
#-------------------------------------------




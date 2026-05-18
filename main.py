import numpy as np
from losses import switching_losses
from plot import plot_losses

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

#Tableau pour stocker les valeur des pertes par commutation
#-------------------------------------------
transistor_losses = []
mosfet_losses = []
#-------------------------------------------

frequencies = np.linspace(1000, 100000, 100) #Valeurs de fréquence sur 100 points réparties uniformément

#Calcul des pertes en fonction des fréquences
#-------------------------------------------
for f in frequencies:
    transistor_loss = switching_losses(V, I, transistor_tr, transistor_tf, f)
    mosfet_loss = switching_losses(V, I, mosfet_tr, mosfet_tf, f)

    transistor_losses.append(transistor_loss)
    mosfet_losses.append(mosfet_loss)
#-------------------------------------------


plot_losses(frequencies, transistor_losses, mosfet_losses) #Tracé des graphiques


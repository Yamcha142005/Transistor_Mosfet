import numpy as np

def thermal_simulation(pertes, Cth, Ta, T, dt, Rth, simulation_time):
    """
    pertes en watt
    Cth en J/degré celsisus
    Ta, T en température
    dt , simulation time en secondes
    Rth en C/W
    """
    times = np.arange(0, simulation_time, dt)

    temperatures = []

    T = Ta

    for t in times:
        #Modèle thermique
        dTdt = (pertes - (T-Ta)/Rth) / Cth
        
        #Méthode d'Euler
        T = T + dTdt * dt

        #Ajout de la température calculée
        temperatures.append(T)

    return times, temperatures
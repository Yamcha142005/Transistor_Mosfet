
def junction_temperature(Ta, P, Rth):
    """
    Calcul de la température de la jonction des composants
    Ta-> Température ambiante
    P-> Pertes par commutation
    Rth-> Résistance thermique de la jonction
    """
    return Ta + P * Rth
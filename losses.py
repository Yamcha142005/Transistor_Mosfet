
def switching_losses(V, I, tr, tf, f):
    """
    Les pertes par commutation utilisant:
    V-> la tension
    I-> le courant
    tr-> la période ON
    tf-> la période OFF
    f-> la fréquence de commutattion
    """
    return 0.5*V*I*(tr+tf)*f
import matplotlib.pyplot as plt

def plot_losses(frequencies, transistor_losses, mosfet_losses):
    #Traçer des graphiques de pertes du transistor et du mosfet
    #--------------------------------------------------------------
    plt.plot(frequencies, transistor_losses, label = "Transistor", color = "blue") 
    plt.plot(frequencies, mosfet_losses, label = "Mosfet", color = "red")
    #--------------------------------------------------------------

    plt.xlabel("Fréquences PWM (Hz)")
    plt.ylabel("Pertes par commutation(W)")
    plt.title("Comparaison des pertes de commutation")

    plt.legend()
    plt.grid(True)

    plt.show()
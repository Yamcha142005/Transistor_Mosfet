import streamlit as st
import numpy as np
from losses import switching_losses
from thermal import junction_temperature
import matplotlib.pyplot as plt
from thermal_dynamic import thermal_simulation


# =========================================================
# TITRE
# =========================================================

st.title("Transistor VS Mosfet")


# =========================================================
# CHOIX DES GRANDEURS ÉLECTRIQUES
# =========================================================

V = st.slider(
    "Choisir une tension en Volt",
    0,
    24,
    12
)

I = st.slider(
    "Choisir une intensité en Ampère",
    0,
    5,
    1
)

fd = st.slider("Choisir une fréquence en Hz", 1000, 100000, 50000)

simulation_time = st.slider("Temps de simulation en secondes", 0,7200,3600)


# =========================================================
# PARAMÈTRES TRANSISTOR (TIP122)
# =========================================================

transistor_tr = 200e-9
transistor_tf = 500e-9


# =========================================================
# PARAMÈTRES MOSFET (IRLZ44N)
# =========================================================

mosfet_tr = 84e-9
mosfet_tf = 15e-9


# =========================================================
# PARAMÈTRES THERMIQUES
# =========================================================

Ta = 25                     # Température ambiante
Tc_transistor = 150         # Température critique
Rth_transistor = 62.5
Rth_mosfet = 62
Cth_transistor = 10
Cth_mosfet = 15
dt = 0.1

# =========================================================
# TABLEAUX DE STOCKAGE
# =========================================================

transistor_losses = []
mosfet_losses = []

transistor_temperatures = []
mosfet_temperatures = []


# =========================================================
# FRÉQUENCES
# =========================================================

frequencies = np.linspace(
    1000,
    1_000_000,
    1000
)


# =========================================================
# CALCULS
# =========================================================

for f in frequencies:

    # Pertes
    transistor_loss = switching_losses(
        V,
        I,
        transistor_tr,
        transistor_tf,
        f
    )

    mosfet_loss = switching_losses(
        V,
        I,
        mosfet_tr,
        mosfet_tf,
        f
    )

    # Températures
    transistor_temperature = junction_temperature(
        Ta,
        transistor_loss,
        Rth_transistor
    )

    mosfet_temperature = junction_temperature(
        Ta,
        mosfet_loss,
        Rth_mosfet
    )

    # Stockage
    transistor_losses.append(transistor_loss)
    mosfet_losses.append(mosfet_loss)

    transistor_temperatures.append(
        transistor_temperature
    )

    mosfet_temperatures.append(
        mosfet_temperature
    )

    

# Conversion listes -> arrays numpy
transistor_temperatures = np.array(
    transistor_temperatures
)

mosfet_temperatures = np.array(
    mosfet_temperatures
)



# =========================================================
# CHOIX DES COMPOSANTS
# =========================================================

st.write("Choisir les composants à afficher")

transistor_checkbox = st.checkbox(
    "Transistor(TIP122)",
    value=True
)

mosfet_checkbox = st.checkbox(
    "Mosfet(IRLZ44N)",
    value=True
)

# =========================================================
# SOUS TITRES 1
# =========================================================
st.header("ETUDE STATIQUE")

# =========================================================
# CHOIX DES GRAPHES
# =========================================================

st.write("Choisir les graphes à afficher")

show_losses = st.checkbox(
    "Afficher les pertes",
    value=True
)

show_temperatures = st.checkbox(
    "Afficher les températures",
    value=True
)


# =========================================================
# GRAPHE DES PERTES
# =========================================================

if show_losses:

    fig, ax = plt.subplots()

    # Transistor
    if transistor_checkbox:

        ax.plot(
            frequencies,
            transistor_losses,
            label="Transistor",
            color="blue"
        )

    # Mosfet
    if mosfet_checkbox:

        ax.plot(
            frequencies,
            mosfet_losses,
            label="Mosfet",
            color="red"
        )

    ax.set_title("Comparaison des pertes")

    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Pertes (Watt)")

    ax.grid(True)
    ax.legend()

    st.pyplot(fig)


# =========================================================
# GRAPHE DES TEMPÉRATURES
# =========================================================

if show_temperatures:

    fig, ax = plt.subplots()

    # Transistor
    if transistor_checkbox:

        ax.plot(
            frequencies,
            transistor_temperatures,
            label="Transistor",
            color="blue"
        )

    # Mosfet
    if mosfet_checkbox:

        ax.plot(
            frequencies,
            mosfet_temperatures,
            label="Mosfet",
            color="red"
        )

    # Température critique
    ax.axhline(
        150,
        linestyle="--",
        color="green",
        label="Température critique transistor"
    )

    ax.set_title("Comparaison des températures")

    ax.set_xlabel("Fréquence (Hz)")
    ax.set_ylabel("Température (°C)")

    ax.grid(True)
    ax.legend()

    st.pyplot(fig)

    critical_indices = np.where(
    transistor_temperatures >= Tc_transistor
)[0]

if len(critical_indices) > 0:

    position_fc = critical_indices[0]

    fc = frequencies[position_fc]

    Tm = mosfet_temperatures[position_fc]

    st.write(f"Température critique du transistor: {Tc_transistor} °C")
    st.write(f"Fréquence critique du transistor: {fc:} Hz")
    st.write(f"Température du mosfet à la fréquence critique du transistor: {Tm:.1f} °C")

else:
    st.write("Le transistor n'atteint pas la température critique.")


# =========================================================
# SOUS TITRES 2
# =========================================================
st.header("ETUDE DYNAMIQUE")

# =========================================================
# DESCRIPTION
# =========================================================
st.write("Graphe montrant la température en fonction du temps se basant sur l'utilisation d'un modèle thermique")

# =========================================================
# CALCUL PERTES DYNAMIQUES
# =========================================================
mosfet_loss_d = switching_losses(V,I, mosfet_tr, mosfet_tf, fd)
transistor_loss_d = switching_losses(V,I, transistor_tr, transistor_tf, fd)

# =========================================================
# GRAPHE SIMULATION DYNAMIQUE
# =========================================================

times, mosfet_tempd = thermal_simulation(mosfet_loss_d, Cth_mosfet, Ta, 0, dt, Rth_mosfet, simulation_time)
times, transistor_tempd = thermal_simulation(transistor_loss_d, Cth_transistor, Ta, 0, dt, Rth_transistor, simulation_time)

fig, ax = plt.subplots()

ax.plot(times, mosfet_tempd, label = "Mosfet", color = "red")
ax.plot(times, transistor_tempd, label = "Transistor", color = "blue")

ax.axhline(
        150,
        linestyle="--",
        color="green",
        label="Température critique transistor"
    )

ax.set_xlabel("Temps(s)")
ax.set_ylabel("Température")

ax.legend()
ax.grid(True)

st.pyplot(fig)

transistor_tempd = np.array(transistor_tempd)
critical_indices_d = np.where(
    transistor_tempd >= Tc_transistor
)[0]

if len(critical_indices_d) > 0:

    position_tc = critical_indices_d[0]

    tc = times[position_tc]

    st.write(f"Le transistor atteint sa température critique en {tc:.1f} secondes")

else:
    st.write("Le transistor n'atteint pas la température critique.")
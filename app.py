import streamlit as st
import numpy as np
from losses import switching_losses
from thermal import junction_temperature
import matplotlib.pyplot as plt


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


# =========================================================
# CHOIX DES COMPOSANTS
# =========================================================

st.write("Choisir les composants à afficher")

transistor_checkbox = st.checkbox(
    "Transistor",
    value=True
)

mosfet_checkbox = st.checkbox(
    "Mosfet",
    value=True
)


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



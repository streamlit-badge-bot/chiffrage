# import json

import numpy as np
import pandas as pd
import streamlit as st


frames = []
total_jours = []
total_paliers = []
total_equip = []
cout_equip = []
total_echeance = []

st.sidebar.image("logo/Logo_CITC_Gris.png", use_column_width=True)

paliers = st.sidebar.number_input("Nombre de paliers", value=1)
tjm = st.sidebar.number_input("TJM", value=550)

st.title("Simulateur de coût PTF")


st.markdown("# Paliers")


# definition du nombre de paliers
for palier in range(paliers):
    st.header(f"Palier {palier}")

    nom = st.text_input("Dénomination du palier", "palier", key=f"{palier}")

    # nombre de taches dans chaque palier
    taches = st.number_input(
        f"Nombre de tâches à effectuer dans le palier {palier}",
        value=0,
        key=f"{palier}",
    )

    subtotal_jours = []
    subtotal_tasks = []

    # definition du nom de la tache et du nombre de jours
    # estimé nécessaire à la tâche
    for tache in range(taches):
        left, right = st.beta_columns(2)
        with left:
            task = st.text_input(
                f"Tâche {tache}", "task", key=f"{palier}_{tache}"
            )
        with right:
            jours = st.number_input(
                "Nombre de jours estimés",
                max_value=100,
                min_value=0,
                value=0,
                key=f"{palier}_{tache}",
            )

        # chaque tache est ajouté à la liste liste pour
        # avoir un sous total par palier
        subtotal_tasks.append(
            {
                "palier": palier,
                "nom": nom,
                "tache": task,
                "jours": jours,
            }
        )

        # liste des nombres de jours par taches
        subtotal_jours.append(jours)
    # subtotal_jours
    # subtotal_tasks

    # recap des taches pour chaque palier
    st.markdown("### Récapitulatif du palier")
    sub_descriptif = pd.DataFrame(
        subtotal_tasks, columns=["palier", "nom", "tache", "jours"]
    )
    st.dataframe(sub_descriptif)
    frames.append(sub_descriptif)

    # calcul du nombre global de jour par palier
    total = np.sum(subtotal_jours)
    st.sidebar.write(
        f"Total de jours hommes pour le palier {palier} : ", total
    )

    total_jours.append(total)
    # total_paliers.append(subtotal_tasks)

# recap global des taches et paliers
st.markdown("### Descriptif global des paliers")
descriptif_global = pd.concat(frames, ignore_index=True)
st.dataframe(descriptif_global)

total_jours = np.sum(total_jours)
st.sidebar.write("Nombre de jours au total pour le projet : ", total_jours)
st.sidebar.write("Coût total jour homme : ", total_jours * tjm)

pilotage = st.sidebar.number_input("Coefficient pilotage", value=0.12)
risque = st.sidebar.number_input("Coefficient risque", value=0.20)

nb_pilotage = float(total_jours * pilotage)

add_pilotage = st.sidebar.checkbox(
    "Prendre en compte le pilotage dans le risque ? Non par défaut."
)

if add_pilotage:
    nb_risque = float((total_jours + nb_pilotage) * risque)
else:
    nb_risque = float(total_jours * risque)

total_jour_projet = float(total_jours + nb_pilotage + nb_risque)

st.sidebar.write("Total de jours pour le pilotage : ", nb_pilotage)
st.sidebar.write("Total de jours pour le risque : ", nb_risque)
st.sidebar.write(
    "Total de jours pour le projet, risque et pilotage compris : ",
    total_jour_projet,
)

cout_global = float((total_jours + nb_pilotage + nb_risque) * tjm)

st.sidebar.write(
    "Coût total pour le projet, risque et pilotage compris : ",
    cout_global,
)

details = {
    "Nombre de jours homme au total pour le projet": total_jours,
    "Coût total jour homme": total_jours * tjm,
    "Coefficient pilotage": pilotage,
    "Coefficient risque": risque,
    "Total de jours pour le pilotage": nb_pilotage,
    "Total de jours pour le risque ": nb_risque,
    "Total de jours total pour le projet": total_jour_projet,
    "Coût total pour le projet, risque et pilotage compris ": cout_global,
}
details = pd.DataFrame.from_dict(details, orient="index")
# st.dataframe(details)


st.markdown("# Equipement")


nb_equip = st.number_input(
    "Nombre d'équipements à lister",
    value=1,
)

for equip in range(nb_equip):
    left, right = st.beta_columns(2)
    with left:
        equipement = st.text_input(
            f"Equipement {equip}", "equip", key=f"{equip}"
        )
    with right:
        cost = st.number_input(
            "Coût estimé",
            max_value=100000,
            min_value=0,
            value=0,
            key=f"{equip}",
        )
    cout_equip.append(cost)

    # chaque equipement est ajouté à la liste liste pour
    # avoir un sous total par palier
    total_equip.append({"equipement": equipement, "cout": cost})

st.markdown("### Récapitulatif équipement")
descriptif_equip = pd.DataFrame(total_equip, columns=["equipement", "cout"])
st.dataframe(descriptif_equip)

# cout_equip
total_cost = np.sum(cout_equip)
st.sidebar.write("Coût total estimé de l'équipement : ", total_cost)

st.markdown("# Coût final")

st.write(
    "Coût final : ",
    float((total_jours + nb_pilotage + nb_risque) * tjm + total_cost),
)


st.markdown("# Echéancier de paiement")
st.markdown(
    "## **ATTENTION** : Par défaut, l'échéancier de paiement ne prend en compte que le coût total pour le projet, risque et pilotage compris. Le coût de l'équipement n'est pris en compte."
)
adhesion = st.number_input(
    "Coût de l'adhésion", min_value=0, max_value=10000, value=2200
)

add_adhesion = st.checkbox("Prendre en compte l'adhésion dans le coût global")

if add_adhesion:
    cout_global += adhesion

# nombre d'echeances voulues
echeances = st.number_input(
    "Nombre d'échéances",
    value=0,
)

# definition du nom de la tache et du nombre de jours
# estimé nécessaire à la tâche
for echeance in range(echeances):
    left, center, right = st.beta_columns(3)
    with left:
        ratio = st.number_input(
            f"Ratio a payer à l'échéance {echeance}",
            min_value=0.0,
            max_value=1.0,
            value=0.3,
            key=f"{echeance}",
        )
    with center:
        descriptif = st.text_input(
            "Descriptif", "description", key=f"{echeance}"
        )
    with right:
        montant = st.text_input(
            "Montant en Euro HT", ratio * cout_global, key=f"{echeance}"
        )

    # chaque echeance est ajouté à la liste liste pour
    # avoir un total
    total_echeance.append(
        {"ratio": ratio, "descriptif": descriptif, "montant HT": montant}
    )

# recap des taches pour chaque palier

st.markdown("### Récapitulatif des écheances de paiement")
echeancier = pd.DataFrame(
    total_echeance, columns=["ratio", "descriptif", "montant HT"]
)
st.dataframe(echeancier)
import streamlit as st
import pandas as pd
from datetime import datetime
import data  # Assurez-vous que ce module contient les fonctions de manipulation des données
import plotly.express as px

# Page configuration
st.set_page_config(page_title="S'Thilé - Suivi et Évaluation", page_icon="👗", layout="wide")

# Title
st.title("S'Thilé - Suivi et Évaluation de la Production")

# Sidebar
st.sidebar.title("Menu")
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state['logged_in']:
    page = st.sidebar.selectbox("Choisir une page", ["Connexion"])
else:
    if st.session_state['role'] == 'employeur':
        page = st.sidebar.selectbox("Choisir une page",
                                    ["Enregistrement","Commandes de Tissus", "Production", "Employés", "Performance des Ouvriers", "Ventes", "Stocks", "Acquisition des Matières Premières", "Rapports"])
    elif st.session_state['role'] == 'employe':
        page = st.sidebar.selectbox("Choisir une page", ["Performance des Ouvriers"])


# Connexion des utilisateurs
if page == "Connexion":
    st.header("Connexion des Utilisateurs")

    with st.form("connexion_utilisateur"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        submitted = st.form_submit_button("Se connecter")

        if submitted:
            user = data.verifier_utilisateur(username, password)
            if user:
                st.session_state['logged_in'] = True
                st.session_state['role'] = user['role']  # Store the user role
                st.success("Connexion réussie.")
                st.experimental_rerun()
            else:
                st.error("Nom d'utilisateur ou mot de passe incorrect.")


# Enregistrement des utilisateurs
elif page == "Enregistrement" and st.session_state['logged_in']:
    st.header("Enregistrement des Utilisateurs")

    with st.form("enregistrement_utilisateur"):
        username = st.text_input("Nom d'utilisateur")
        password = st.text_input("Mot de passe", type="password")
        role = st.selectbox("Rôle", ["employe", "employeur"])
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if username and password and role:
                data.enregistrer_utilisateur(username, password, role)
                st.success("Utilisateur enregistré avec succès.")
            else:
                st.error("Veuillez remplir tous les champs.")




# Commandes de Tissus
elif page == "Commandes de Tissus" and st.session_state['logged_in']:
    # Afficher l'en-tête en bleu
    st.markdown("<h2 style='color:blue;'>Enregistrement des Commandes de Tissus</h2>", unsafe_allow_html=True)

    with st.form("commande_tissus"):
        date_commande = st.date_input("Date de Commande")
        type_tissu = st.text_input("Type de Tissu",placeholder="Type de tissu")
        quantite = st.number_input("Quantité",min_value=0, step=1)
        cout = st.number_input("Coût",min_value=0)
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if type_tissu =="":
                st.error("Veuillez renseigner le type de tissu...")
            elif not quantite:
                st.error("Veuillez renseigner la quantité...")
            elif not  cout:
                st.error("Veuillez renseigner le coût...")

            else:
                data.enregistrer_commande_tissus(date_commande, type_tissu, quantite, cout)
                st.success("Commande enregistrée avec succès.")






# Enregistrement des employés
elif page == "Employés" and st.session_state['logged_in']:
    st.header("Enregistrement des Employés")

    with st.form("employes"):
        nom_prenoms = st.text_input("Nom et prénoms")
        date_prise_service = st.date_input("Date de prise de service")
        type_contrat = st.selectbox("Type de contrat", ["","CDD", "CDI", "Stagiaire","Journalier"])
        date_naissance = st.date_input("Date de naissance")
        numero_telephone = st.text_input("Contact principal")
        numero_telephone2 = st.text_input("Autre contact")
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            data.enregistrer_employe(nom_prenoms, date_prise_service, type_contrat, date_naissance, numero_telephone, numero_telephone2)
            st.success("Employé enregistré avec succès.")




# Production
elif page == "Production" and st.session_state['logged_in']:
    st.markdown("<h2 style='color:blue;'>Suivi de la Production</h2>", unsafe_allow_html=True)

    types_employes = data.obtenir_types_employes()
    types_employes = [""] + types_employes
    type_numero_serie=data.obtenir_types_serie()
    type_numero_serie=type_numero_serie+[""]

    # Obtenir les données de production existantes
    production_df = data.obtenir_production()

    with st.form("production"):
        date_production = st.date_input("Date de Production")
        type_vetement = st.text_input("Type de Vêtement")
        nombre = st.number_input("Nombre", min_value=0, step=1)
        couleur = st.text_input("Couleur")
        longueur_manche = st.selectbox("Longueur de Manche", ["Courte", "Longue"])
        taille = st.selectbox("Taille", ["XS", "S", "M", "L", "XL", "XXL"])
        forme_cou = st.selectbox("Forme du Cou", ["Rond", "V", "Col"])
        ouvrier = st.selectbox("Choisir l'employé", options=types_employes, index=0)
        numero_serie = st.text_input("Numéro de Série")
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            data.enregistrer_production(date_production, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie)
            st.success("Production enregistrée avec succès.")

    numero_serie_selection = st.selectbox("Sélectionnez le Numéro de Série pour modifier l'entrée de production",
                                          options=type_numero_serie)


    st.markdown("<h3 style='color:blue;'>Modification de la Production</h3>", unsafe_allow_html=True)
    if numero_serie_selection:
        selected_row = production_df[production_df["numero_serie"] == numero_serie_selection].iloc[0]

        # Convertir la date en objet datetime.date
        date_production_value = datetime.strptime(selected_row["Date"], '%Y-%m-%d').date()

        with st.form("modifier_production"):
            date_production = st.date_input("Date de Production", value=date_production_value)
            type_vetement = st.text_input("Type de Vêtement", value=selected_row["Type de Vêtement"])
            nombre = st.number_input("Nombre", min_value=0, step=1, value=selected_row["Nombre"])
            couleur = st.text_input("Couleur", value=selected_row["Couleur"])
            longueur_manche = st.selectbox("Longueur de Manche", ["Courte", "Longue"],
                                           index=["Courte", "Longue"].index(selected_row["Longueur de Manche"]))
            taille = st.selectbox("Taille", ["XS", "S", "M", "L", "XL", "XXL"],
                                  index=["XS", "S", "M", "L", "XL", "XXL"].index(selected_row["Taille"]))
            forme_cou = st.selectbox("Forme du Cou", ["Rond", "V", "Col"],
                                     index=["Rond", "V", "Col"].index(selected_row["Forme du Cou"]))
            ouvrier = st.selectbox("Choisir l'employé", options=types_employes,
                                   index=types_employes.index(selected_row["Ouvrier"]))
            numero_serie = st.text_input("Numéro de Série", value=selected_row["numero_serie"])
            submitted = st.form_submit_button("Modifier")

            if submitted:
                data.modifier_production_par_numero_serie(numero_serie, date_production, type_vetement, nombre, couleur,
                                                          longueur_manche, taille, forme_cou, ouvrier)
                st.success("Production modifiée avec succès.")





# Performance des Ouvriers
elif page == "Performance des Ouvriers" and st.session_state['logged_in']:
    st.header("Évaluation de la Performance des Ouvriers")
    types_employes = data.obtenir_types_employes()
    with st.form("performance_ouvriers"):
        date = st.date_input("Date")
        ouvrier = st.selectbox("Ouvrier", options=types_employes)
        heure_arrivee = st.time_input("Heure d'Arrivée")
        heure_depart = st.time_input("Heure de Départ")
        nombre__chemise = st.number_input("Nombre de chemises confectionnées", min_value=0, step=1)
        nombre_vetements_curlotte = st.number_input("Nombre de curlottes Confectionnées", min_value=0, step=1)
        nombre_vetements_tunique = st.number_input("Nombre de tuniques Confectionnées", min_value=0, step=1)
        nombre_vetements_pagne = st.number_input("Nombre de pagnes Confectionnés", min_value=0, step=1)
        nombre_vetements_autre = st.number_input("Nombre d'autres vêtements confectionnés", min_value=0, step=1)

        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if not ouvrier:
                st.error("Le type de vêtement est obligatoire.")
            else:
                data.enregistrer_performance_ouvrier(date, ouvrier, heure_arrivee, heure_depart, nombre__chemise, nombre_vetements_curlotte, nombre_vetements_tunique, nombre_vetements_pagne, nombre_vetements_autre)
                st.success("Performance enregistrée avec succès.")











# Ventes
# Ventes
elif page == "Ventes" and st.session_state['logged_in']:
    st.header("Suivi des Ventes")

    # Obtenir les types de vêtements disponibles
    types_vetements = data.obtenir_types_vetements()
    stock ,_= data.obtenir_stock()

    with st.form("ventes"):
        date_vente = st.date_input("Date de Vente")
        type_vetement = st.selectbox("Type de Vêtement", options=types_vetements)
        nombre = st.number_input("Nombre", min_value=0, step=1)
        prix_vente = st.number_input("Prix de Vente", min_value=0, step=1)
        retouche = st.checkbox("Retouche")
        motif_retouche = st.text_area("Motif de Retouche")
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            if not type_vetement:
                st.error("Le type de vêtement est obligatoire.")
            elif not prix_vente>0:
                st.error("Erreur sur le prix...")
            elif not nombre>0:
                st.error("Nombre doit supérieur à 0 ...")
            elif stock.get(type_vetement, {}).get('produit', 0) - stock.get(type_vetement, {}).get('vendu', 0) < nombre:
                st.error("Stock insuffisant pour le type de vêtement sélectionné.")
            else:
                data.enregistrer_vente(date_vente, type_vetement, nombre, prix_vente, retouche, motif_retouche)
                st.success("Vente enregistrée avec succès.")




# Stocks
elif page == "Stocks" and st.session_state['logged_in']:
    st.header("État des Stocks")

    _,stock_data = data.obtenir_stock()
    st.write(stock_data)

# Acquisition des Matières Premières
elif page == "Acquisition des Matières Premières" and st.session_state['logged_in']:
    st.header("Enregistrement de l'Acquisition des Matières Premières")

    with st.form("acquisition_matiere"):
        date_acquisition = st.date_input("Date d'Acquisition")
        quantite_tissu = st.number_input("Quantité de Tissu (mètres)", min_value=0.0, step=0.1)
        matiere_tissu = st.selectbox("Choisir la matière de Tissu",["lin","Coton","Pagne","Autres"])
        couleur_tissu = st.text_input("Couleur de Tissu")
        quantite_bobine_fil = st.number_input("Quantité de Bobine de Fil", min_value=0, step=1)
        quantite_bouton = st.number_input("Quantité de Bouton", min_value=0, step=1)
        quantite_bande_tissee = st.number_input("Quantité de Bande Tissée", min_value=0, step=1)
        collant_dur = st.number_input("Collant Dur (mètres)", min_value=0.0, step=0.1)
        collant_papier = st.number_input("Collant Papier (mètres)", min_value=0.0, step=0.1)
        viseline = st.number_input("Viseline (mètres)", min_value=0.0, step=0.1)
        popeline = st.number_input("Popeline (mètres)", min_value=0.0, step=0.1)
        submitted = st.form_submit_button("Enregistrer")

        if submitted:
            data.enregistrer_acquisition(date_acquisition, quantite_tissu, matiere_tissu, couleur_tissu, quantite_bobine_fil, quantite_bouton, quantite_bande_tissee, collant_dur, collant_papier, viseline, popeline)
            st.success("Acquisition enregistrée avec succès.")




# Rapports
elif page == "Rapports" and st.session_state['logged_in']:
    st.header("Rapports Statistiques")

    ventes_data = data.obtenir_ventes()
    if not ventes_data.empty:
        st.subheader("Diagramme Circulaire des Types de Vêtements Vendus")
        fig = px.pie(ventes_data, names='Type de Vêtement', title='Répartition des Vêtements Vendus par Type')
        st.plotly_chart(fig)
    else:
        st.info("Aucune donnée de vente disponible.")

    st.header("Données statistiques")
    st.subheader("Tableaux de Ventes")
    st.write(ventes_data)

    st.subheader("Tableaux d'acquisition de matière première")
    matiere_data = data.obtenir_acquisitions()
    st.write(matiere_data)

    st.subheader("Tableaux de Production")
    production_data = data.obtenir_production()
    st.write(production_data)

    st.subheader("Tableaux des Performances des Ouvriers")
    performance_data = data.obtenir_performances()
    st.write(performance_data)

    st.subheader("Tableaux des employés")
    employes_data = data.obtenir_employes()
    st.write(employes_data)

    # Ajout des graphiques et tableaux pour les performances des ouvriers
    st.subheader("Statistiques sur les Performances des Ouvriers")

    # Charger les données de la table performances
    performances_df = performance_data

    # Calcul des heures travaillées
    performances_df['heure_arrivee'] = pd.to_datetime(performances_df['heure_arrivee'])
    performances_df['heure_depart'] = pd.to_datetime(performances_df['heure_depart'])
    performances_df['heures_travaillees'] = (performances_df['heure_depart'] - performances_df['heure_arrivee']).dt.seconds / 3600

    # Nombre total de vêtements confectionnés par ouvrier
    performances_df['total_vetements'] = (performances_df['nombre_vetements_chemise'] +
                                          performances_df['nombre_vetements_curlotte'] +
                                          performances_df['nombre_vetements_tunique'] +
                                          performances_df['nombre_vetements_pagne'] +
                                          performances_df['nombre_vetements_autre'])

    # Graphique à barres - Nombre total de vêtements confectionnés par ouvrier
    fig_vetements_par_ouvrier = px.bar(performances_df.groupby('ouvrier')['total_vetements'].sum().reset_index(),
                                       x='ouvrier', y='total_vetements', title='Nombre total de vêtements confectionnés par ouvrier')
    st.plotly_chart(fig_vetements_par_ouvrier)

    # Graphique à barres - Nombre total de vêtements confectionnés par type
    total_vetements_par_type = performances_df[['nombre_vetements_chemise', 'nombre_vetements_curlotte',
                                                'nombre_vetements_tunique', 'nombre_vetements_pagne',
                                                'nombre_vetements_autre']].sum().reset_index()
    total_vetements_par_type.columns = ['Type de vêtement', 'Total']
    fig_vetements_par_type = px.bar(total_vetements_par_type, x='Type de vêtement', y='Total',
                                    title='Nombre total de vêtements confectionnés par type')
    st.plotly_chart(fig_vetements_par_type)

    # Tableau récapitulatif par ouvrier
    st.subheader("Tableau récapitulatif par ouvrier")
    table_recap_ouvrier = performances_df.groupby('ouvrier').agg({
        'nombre_vetements_chemise': 'sum',
        'nombre_vetements_curlotte': 'sum',
        'nombre_vetements_tunique': 'sum',
        'nombre_vetements_pagne': 'sum',
        'nombre_vetements_autre': 'sum',
        'heures_travaillees': 'sum'
    }).reset_index()
    st.write(table_recap_ouvrier)

    # Diagramme circulaire - Répartition des types de vêtements confectionnés
    fig_repartition_vetements = px.pie(total_vetements_par_type, names='Type de vêtement', values='Total',
                                       title='Répartition des types de vêtements confectionnés')
    st.plotly_chart(fig_repartition_vetements)

    # Graphique en ligne - Performance quotidienne des ouvriers
    performances_df['date'] = pd.to_datetime(performances_df['date'])
    fig_performance_quotidienne = px.line(performances_df.groupby(['date', 'ouvrier'])['total_vetements'].sum().reset_index(),
                                          x='date', y='total_vetements', color='ouvrier',
                                          title='Performance quotidienne des ouvriers')
    st.plotly_chart(fig_performance_quotidienne)

import sqlite3
import pandas as pd
import hashlib

# Connexion à la base de données SQLite
conn = sqlite3.connect('sthile.db')
cursor = conn.cursor()

def supprimer_table_performances():
    cursor.execute('''DROP TABLE IF EXISTS performances''')
    conn.commit()

def supprimer_table_ventes():
    cursor.execute('''DROP TABLE IF EXISTS ventes''')
    conn.commit()


def supprimer_table_utilisateurs():
    cursor.execute('''DROP TABLE IF EXISTS utilisateurs''')
    conn.commit()




def supprimer_table_production():
    cursor.execute('''DROP TABLE IF EXISTS production''')
    conn.commit()


# Création des tables si elles n'existent pas déjà
def creer_tables():
    cursor.execute('''CREATE TABLE IF NOT EXISTS commandes (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        type_tissu TEXT,
                        quantite REAL,
                        cout REAL
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS production (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            type_vetement TEXT,
                            nombre INTEGER,
                            couleur TEXT,
                            longueur_manche TEXT,
                            taille TEXT,
                            forme_cou TEXT,
                            ouvrier TEXT,
                            numero_serie TEXT
                          )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS performances (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            ouvrier TEXT,
                            heure_arrivee TEXT,
                            heure_depart TEXT,
                            nombre_vetements_chemise INTEGER,
                            nombre_vetements_curlotte INTEGER,
                            nombre_vetements_tunique INTEGER,
                            nombre_vetements_pagne INTEGER,
                            nombre_vetements_autre INTEGER
                          )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS ventes (
                        id INTEGER PRIMARY KEY,
                        date TEXT,
                        type_vetement TEXT,
                        nombre INTEGER,
                        prix_vente REAL,
                        retouche INTEGER,
                        motif_retouche TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS utilisateurs (
                        id INTEGER PRIMARY KEY,
                        username TEXT UNIQUE,
                        password TEXT,
                        role TEXT
                      )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS acquisitions (
                            id INTEGER PRIMARY KEY,
                            date TEXT,
                            quantite_tissu REAL,
                            matiere_tissu TEXT,
                            couleur_tissu TEXT,
                            quantite_bobine_fil INTEGER,
                            quantite_bouton INTEGER,
                            quantite_bande_tissee INTEGER,
                            collant_dur REAL,
                            collant_papier REAL,
                            viseline REAL,
                            popeline REAL
                          )''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS employes (
                               id INTEGER PRIMARY KEY,
                               nom_prenoms TEXT,
                               date_prise_service TEXT,
                               type_contrat TEXT,
                               date_naissance TEXT,
                               numero_telephone TEXT,
                               numero_telephone2 TEXT
                             )''')

    conn.commit()

# Appel à la création des tables au démarrage

# Supprimer la table performances existante
#supprimer_table_performances()
#supprimer_table_production()
#supprimer_table_ventes()
#supprimer_table_utilisateurs()
creer_tables()

# Fonctions pour enregistrer les données
def enregistrer_employe(nom_prenoms, date_prise_service, type_contrat, date_naissance, numero_telephone, numero_telephone2):
    cursor.execute('''
        INSERT INTO employes (nom_prenoms, date_prise_service, type_contrat, date_naissance, numero_telephone, numero_telephone2)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (nom_prenoms, date_prise_service, type_contrat, date_naissance, numero_telephone, numero_telephone2))
    conn.commit()

def enregistrer_commande_tissus(date, type_tissu, quantite, cout):
    cursor.execute('''INSERT INTO commandes (date, type_tissu, quantite, cout)
                      VALUES (?, ?, ?, ?)''', (date, type_tissu, quantite, cout))
    conn.commit()



def enregistrer_production(date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie):
    cursor.execute('''INSERT INTO production (date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou,ouvrier,numero_serie)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie))
    conn.commit()



def enregistrer_acquisition(date, quantite_tissu, matiere_tissu, couleur_tissu, quantite_bobine_fil, quantite_bouton, quantite_bande_tissee, collant_dur, collant_papier, viseline, popeline):
    cursor.execute('''INSERT INTO acquisitions (date, quantite_tissu, matiere_tissu, couleur_tissu, quantite_bobine_fil, quantite_bouton, quantite_bande_tissee, collant_dur, collant_papier, viseline, popeline)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (date, quantite_tissu, matiere_tissu, couleur_tissu, quantite_bobine_fil, quantite_bouton, quantite_bande_tissee, collant_dur, collant_papier, viseline, popeline))
    conn.commit()





def enregistrer_performance_ouvrier(date, ouvrier, heure_arrivee, heure_depart, nombre_vetements_chemise, nombre_vetements_curlotte, nombre_vetements_tunique, nombre_vetements_pagne, nombre_vetements_autre):
    heure_arrivee_str = heure_arrivee.strftime('%H:%M')
    heure_depart_str = heure_depart.strftime('%H:%M')
    cursor.execute('''INSERT INTO performances (date, ouvrier, heure_arrivee, heure_depart, nombre_vetements_chemise, nombre_vetements_curlotte, nombre_vetements_tunique, nombre_vetements_pagne, nombre_vetements_autre)
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                   (date, ouvrier, heure_arrivee_str, heure_depart_str, nombre_vetements_chemise, nombre_vetements_curlotte, nombre_vetements_tunique, nombre_vetements_pagne, nombre_vetements_autre))
    conn.commit()

def enregistrer_vente(date, type_vetement, nombre, prix_vente, retouche, motif_retouche):
    cursor.execute('''INSERT INTO ventes (date, type_vetement, nombre, prix_vente, retouche, motif_retouche)
                      VALUES (?, ?, ?, ?, ?, ?)''', (date, type_vetement, nombre, prix_vente, retouche, motif_retouche))
    conn.commit()

def enregistrer_utilisateur(username, password, role):
    password_hashed = hashlib.sha256(password.encode()).hexdigest()
    cursor.execute('''INSERT INTO utilisateurs (username, password, role)
                      VALUES (?, ?, ?)''', (username, password_hashed, role))
    conn.commit()






def verifier_utilisateur(username, password):
    password_encoded = password.encode('utf-8')
    password_hashed = hashlib.sha256(password_encoded).hexdigest()
    cursor.execute('''SELECT * FROM utilisateurs WHERE username=? AND password=?''', (username, password_hashed))
    user = cursor.fetchone()
    if user:
        return {'id': user[0], 'username': user[1], 'role': user[3]}
    return None
# Fonctions pour obtenir les données
def obtenir_ventes():
    cursor.execute('SELECT * FROM ventes')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Date', 'Type de Vêtement', 'Nombre', 'Prix de Vente', 'Retouche', 'Motif de Retouche'])
    return df

# Information employés
def obtenir_employes():
    cursor.execute('SELECT * FROM employes')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID','Nom et prénoms', 'Date de prise de service', 'Type de contrat', 'Date de naissance', 'Contact principal', 'Autre contact'])
    return df

def obtenir_production():
    cursor.execute('SELECT * FROM production')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Date', 'Type de Vêtement', 'Nombre', 'Couleur', 'Longueur de Manche', 'Taille', 'Forme du Cou', 'Ouvrier','numero_serie'])
    return df

def obtenir_performances():
    cursor.execute('SELECT * FROM performances')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'date', 'ouvrier', 'heure_arrivee', 'heure_depart', 'nombre_vetements_chemise','nombre_vetements_curlotte', 'nombre_vetements_tunique','nombre_vetements_pagne','nombre_vetements_autre'])
    return df

def obtenir_types_vetements():
    cursor.execute('SELECT DISTINCT type_vetement FROM production')
    data = cursor.fetchall()
    types_vetements = [row[0] for row in data]
    return types_vetements

def obtenir_types_serie():
    cursor.execute('SELECT DISTINCT numero_serie FROM production')
    data = cursor.fetchall()
    types_serie_numero = [row[0] for row in data]
    return types_serie_numero



def obtenir_types_employes():
    cursor.execute('SELECT DISTINCT nom_prenoms FROM employes')
    data = cursor.fetchall()
    types_vetements = [row[0] for row in data]
    return types_vetements


# Acquisition de matière
def obtenir_acquisitions():
    cursor.execute('SELECT * FROM acquisitions')
    data = cursor.fetchall()
    df = pd.DataFrame(data, columns=['ID', 'Date', 'Quantité de Tissu', 'Matière de Tissu', 'Couleur de Tissu', 'Quantité de Bobine de Fil', 'Quantité de Bouton', 'Quantité de Bande Tissée', 'Collant Dur', 'Collant Papier', 'Viseline', 'Popeline'])
    return df


def obtenir_stock():
    cursor.execute('''
        SELECT type_vetement, SUM(nombre) as nombre_produit
        FROM production
        GROUP BY type_vetement
    ''')
    production = cursor.fetchall()
    cursor.execute('''
        SELECT type_vetement, SUM(nombre) as nombre_vendu
        FROM ventes
        GROUP BY type_vetement
    ''')
    ventes = cursor.fetchall()

    stock = {}
    for row in production:
        stock[row[0]] = {'produit': row[1], 'vendu': 0}
    for row in ventes:
        if row[0] in stock:
            stock[row[0]]['vendu'] = row[1]

    stock_data = [{'Type de Vêtement': k, 'Stock Disponible': v['produit'] - v['vendu']} for k, v in stock.items()]
    df = pd.DataFrame(stock_data)
    return stock ,df # On retourne le dictionnaire stock au lieu de la DataFrame







def modifier_production(id, date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie):
    cursor.execute('''UPDATE production 
                      SET date = ?, type_vetement = ?, nombre = ?, couleur = ?, longueur_manche = ?, taille = ?, forme_cou = ?, ouvrier = ?, numero_serie = ?
                      WHERE id = ?''',
                   (date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie, id))
    conn.commit()



def modifier_production_par_numero_serie(numero_serie, date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier):
    cursor.execute('''UPDATE production 
                      SET date = ?, type_vetement = ?, nombre = ?, couleur = ?, longueur_manche = ?, taille = ?, forme_cou = ?, ouvrier = ?
                      WHERE numero_serie = ?''',
                   (date, type_vetement, nombre, couleur, longueur_manche, taille, forme_cou, ouvrier, numero_serie))
    conn.commit()


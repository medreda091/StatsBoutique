"""Génère le jeu de données de démonstration dans sql/donnees.sql.

Données fictives mais réalistes pour une boutique en ligne, générées de façon
déterministe (graine fixe) : le fichier produit est toujours identique.
Usage : python3 scripts/generer_donnees.py
"""

import random
from datetime import date, timedelta
from pathlib import Path

GRAINE = 42
FICHIER_SORTIE = Path(__file__).resolve().parents[1] / "sql" / "donnees.sql"

# --- Référentiels -----------------------------------------------------------

CATEGORIES = [
    "Informatique", "Audio", "Maison", "Sport",
    "Cuisine", "Jeux vidéo", "Livres", "Mode",
]

PRODUITS_PAR_CATEGORIE = {
    "Informatique": [("Clavier mécanique", 89.99), ("Souris sans fil", 39.99),
                     ("Écran 27 pouces", 249.99), ("Disque SSD 1 To", 79.99),
                     ("Webcam HD", 59.99)],
    "Audio": [("Casque Bluetooth", 129.99), ("Enceinte portable", 69.99),
              ("Écouteurs intra-auriculaires", 49.99), ("Barre de son", 199.99),
              ("Micro USB", 89.99)],
    "Maison": [("Lampe de bureau LED", 34.99), ("Aspirateur robot", 299.99),
               ("Set de 3 cadres photo", 24.99), ("Rideaux occultants", 44.99),
               ("Diffuseur d'huiles essentielles", 29.99)],
    "Sport": [("Tapis de yoga", 29.99), ("Haltères réglables", 119.99),
              ("Montre connectée sport", 179.99), ("Sac de sport", 49.99),
              ("Corde à sauter connectée", 39.99)],
    "Cuisine": [("Robot pâtissier", 349.99), ("Cafetière à piston", 39.99),
                ("Set de couteaux", 89.99), ("Airfryer", 129.99),
                ("Balance de cuisine", 24.99)],
    "Jeux vidéo": [("Manette sans fil", 69.99), ("Clavier gamer RGB", 119.99),
                   ("Casque gaming", 99.99), ("Tapis de souris XXL", 29.99),
                   ("Volant de course", 249.99)],
    "Livres": [("Roman policier : L'ombre du quai", 14.99),
               ("Guide Python pour débutants", 29.99),
               ("BD : Les voyageurs du temps", 16.99),
               ("Livre de recettes du monde", 24.99),
               ("Essai : Comprendre l'IA", 19.99)],
    "Mode": [("Sneakers blanches", 89.99), ("Sac à dos urbain", 59.99),
             ("Montre minimaliste", 129.99), ("Écharpe en laine", 34.99),
             ("Lunettes de soleil", 79.99)],
}

PRENOMS = ["Léa", "Hugo", "Emma", "Louis", "Chloé", "Raphaël", "Jade", "Arthur",
           "Manon", "Jules", "Camille", "Adam", "Sarah", "Nathan", "Inès",
           "Gabriel", "Louise", "Ethan", "Anna", "Maxime", "Lina", "Théo",
           "Eva", "Antoine", "Julia", "Enzo", "Alice", "Lucas", "Sofia", "Noah"]

NOMS = ["Martin", "Bernard", "Dubois", "Moreau", "Laurent", "Simon", "Michel",
        "Lefebvre", "Leroy", "Roux", "David", "Bertrand", "Morel", "Fournier",
        "Girard", "Bonnet", "Dupont", "Lambert", "Fontaine", "Rousseau",
        "Vincent", "Muller", "Faure", "Andre", "Mercier", "Blanchard",
        "Guerin", "Boyer", "Garnier", "Chevalier"]

VILLES = ["Lyon", "Paris", "Marseille", "Toulouse", "Bordeaux", "Nantes",
          "Lille", "Strasbourg", "Rennes", "Grenoble", "Dijon", "Nice",
          "Montpellier", "Clermont-Ferrand", "Angers", "Tours"]

NB_CLIENTS = 200
NB_COMMANDES = 1400
NB_AVIS = 450
DEBUT_VENTES = date(2025, 1, 1)
FIN_VENTES = date(2026, 9, 30)


def echapper(texte: str) -> str:
    """Échappe les apostrophes pour le SQL."""
    return texte.replace("'", "''")


def date_aleatoire(rng: random.Random, debut: date, fin: date) -> date:
    return debut + timedelta(days=rng.randint(0, (fin - debut).days))


def main() -> None:
    rng = random.Random(GRAINE)
    lignes_sql = [
        "-- =================================================================",
        "-- StatsBoutique — jeu de données de démonstration",
        "-- Construit avec scripts/generer_donnees.py (graine 42, déterministe).",
        f"-- {NB_CLIENTS} clients, 40 produits, {NB_COMMANDES} commandes, {NB_AVIS} avis.",
        "-- =================================================================",
        "",
    ]

    # --- Catégories ------------------------------------------------------
    lignes_sql.append("-- Catégories")
    for i, nom in enumerate(CATEGORIES, start=1):
        lignes_sql.append(
            f"INSERT INTO categories (id, nom) VALUES ({i}, '{echapper(nom)}');"
        )
    id_categorie = {nom: i for i, nom in enumerate(CATEGORIES, start=1)}

    # --- Produits ---------------------------------------------------------
    lignes_sql.append("")
    lignes_sql.append("-- Produits")
    produits = []  # (id, nom, id_categorie, prix, cout, date_ajout)
    pid = 0
    for categorie, articles in PRODUITS_PAR_CATEGORIE.items():
        for nom, prix in articles:
            pid += 1
            cout = round(prix * rng.uniform(0.40, 0.65), 2)
            date_ajout = date_aleatoire(rng, date(2024, 6, 1), date(2025, 3, 1))
            produits.append((pid, nom, id_categorie[categorie], prix, cout,
                             date_ajout.isoformat()))
            lignes_sql.append(
                "INSERT INTO produits (id, nom, categorie_id, prix, cout, date_ajout) "
                f"VALUES ({pid}, '{echapper(nom)}', {id_categorie[categorie]}, "
                f"{prix:.2f}, {cout:.2f}, '{date_ajout.isoformat()}');"
            )

    # Les 3 derniers produits ne sont jamais vendus (pour la requête n°8).
    produits_vendables = produits[:-3]

    # --- Clients ----------------------------------------------------------
    lignes_sql.append("")
    lignes_sql.append("-- Clients")
    clients = []  # (id, date_inscription)
    emails_vus = set()
    for cid in range(1, NB_CLIENTS + 1):
        nom_complet = f"{rng.choice(PRENOMS)} {rng.choice(NOMS)}"
        base_email = (nom_complet.lower().replace(" ", ".").replace("é", "e")
                      .replace("è", "e").replace("ê", "e").replace("ë", "e"))
        email = f"{base_email}{cid}@exemple.fr"
        assert email not in emails_vus
        emails_vus.add(email)
        ville = rng.choice(VILLES)
        inscription = date_aleatoire(rng, date(2024, 1, 1), date(2025, 6, 30))
        clients.append((cid, inscription))
        lignes_sql.append(
            "INSERT INTO clients (id, nom, email, ville, date_inscription) "
            f"VALUES ({cid}, '{echapper(nom_complet)}', '{email}', "
            f"'{echapper(ville)}', '{inscription.isoformat()}');"
        )

    # --- Commandes + lignes ------------------------------------------------
    lignes_sql.append("")
    lignes_sql.append("-- Commandes et lignes de commande")
    statuts = (["livree"] * 88 + ["expediee"] * 5 + ["en_preparation"] * 4
               + ["annulee"] * 3)
    commandes = []  # (id, client_id, date_commande, statut)
    lid = 0
    for oid in range(1, NB_COMMANDES + 1):
        client_id, inscription = rng.choice(clients)
        date_commande = date_aleatoire(
            rng, max(inscription, DEBUT_VENTES), FIN_VENTES)
        statut = rng.choice(statuts)
        commandes.append((oid, client_id, date_commande.isoformat(), statut))
        lignes_sql.append(
            "INSERT INTO commandes (id, client_id, date_commande, statut) "
            f"VALUES ({oid}, {client_id}, '{date_commande.isoformat()}', "
            f"'{statut}');"
        )
        for _ in range(rng.randint(1, 4)):
            lid += 1
            dispo = [p for p in produits_vendables
                     if p[5] <= date_commande.isoformat()]
            prod = rng.choice(dispo)
            quantite = rng.randint(1, 3)
            lignes_sql.append(
                "INSERT INTO lignes_commande (id, commande_id, produit_id, "
                "quantite, prix_unitaire) "
                f"VALUES ({lid}, {oid}, {prod[0]}, {quantite}, {prod[3]:.2f});"
            )

    # --- Avis --------------------------------------------------------------
    lignes_sql.append("")
    lignes_sql.append("-- Avis clients")
    produits_avec_id_ligne = produits_vendables
    for aid in range(1, NB_AVIS + 1):
        prod = rng.choice(produits_avec_id_ligne)
        client_id = rng.randint(1, NB_CLIENTS)
        note = rng.choices([5, 4, 3, 2, 1], weights=[45, 30, 12, 7, 6])[0]
        date_avis = date_aleatoire(rng, DEBUT_VENTES, FIN_VENTES)
        lignes_sql.append(
            "INSERT INTO avis (id, produit_id, client_id, note, date_avis) "
            f"VALUES ({aid}, {prod[0]}, {client_id}, {note}, "
            f"'{date_avis.isoformat()}');"
        )

    FICHIER_SORTIE.write_text("\n".join(lignes_sql) + "\n", encoding="utf-8")
    print(f"{FICHIER_SORTIE.name} généré "
          f"({len(lignes_sql)} lignes, {lid} lignes de commande).")


if __name__ == "__main__":
    main()

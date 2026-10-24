"""Vérifie que les 12 requêtes d'analyse s'exécutent et sont justes."""

import pytest

from conftest import DOSSIER_SQL, lire_requete

FICHIERS_REQUETES = sorted((DOSSIER_SQL / "requetes").glob("*.sql"))


def chiffre_affaires_total(db):
    return db.execute("""
        SELECT SUM(l.quantite * l.prix_unitaire)
        FROM lignes_commande l
        JOIN commandes c ON c.id = l.commande_id
        WHERE c.statut <> 'annulee'
    """).fetchone()[0]


@pytest.mark.parametrize("fichier", FICHIERS_REQUETES, ids=lambda f: f.name)
def test_requete_execute_sans_erreur(db, fichier):
    lignes = db.execute(fichier.read_text(encoding="utf-8")).fetchall()
    assert len(lignes) > 0


def test_01_ca_mensuel_croissance(db):
    lignes = db.execute(lire_requete(1)).fetchall()
    assert len(lignes) == 21  # 21 mois de ventes
    assert lignes[0][3] is None  # pas de croissance pour le premier mois
    assert round(sum(l[1] for l in lignes), 2) == round(chiffre_affaires_total(db), 2)


def test_02_top_produits_ordonnes(db):
    lignes = db.execute(lire_requete(2)).fetchall()
    assert len(lignes) == 10
    cas = [l[2] for l in lignes]
    assert cas == sorted(cas, reverse=True)
    assert all(0 < part < 100 for part in (l[3] for l in lignes))


def test_05_classement_clients(db):
    lignes = db.execute(lire_requete(5)).fetchall()
    assert len(lignes) == 20
    assert lignes[0][3] == 1  # le premier a le rang 1
    assert {l[5] for l in lignes} <= {1, 2, 3, 4}  # quartiles valides


def test_06_cumul_final_egal_au_total(db):
    lignes = db.execute(lire_requete(6)).fetchall()
    assert round(lignes[-1][2], 2) == round(chiffre_affaires_total(db), 2)


def test_08_produits_jamais_vendus(db):
    lignes = db.execute(lire_requete(8)).fetchall()
    assert len(lignes) == 3


def test_09_saisonnalite_douze_mois(db):
    lignes = db.execute(lire_requete(9)).fetchall()
    assert sorted(l[0] for l in lignes) == list(range(1, 13))


def test_10_rfm_scores_valides(db):
    lignes = db.execute(lire_requete(10)).fetchall()
    assert len(lignes) == 30
    for ligne in lignes:
        score = ligne[4]
        assert len(score) == 3 and all(c in "1234" for c in score)


def test_11_clients_inactifs(db):
    lignes = db.execute(lire_requete(11)).fetchall()
    assert len(lignes) > 0
    for ligne in lignes:
        derniere = ligne[3]
        assert derniere is None or derniere < "2026-04-01"


def test_12_ecart_categorie_coherent(db):
    lignes = db.execute(lire_requete(12)).fetchall()
    assert len(lignes) > 0
    for ligne in lignes:
        # Tolérance d'un centime : la requête arrondit après le calcul.
        assert abs((ligne[3] - ligne[4]) - ligne[5]) < 0.011

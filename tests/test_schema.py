"""Vérifie que le schéma est bien créé : tables, colonnes, contraintes."""

import sqlite3

import pytest


def test_tables_existantes(db):
    tables = {r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table'")}
    assert {"categories", "clients", "produits",
            "commandes", "lignes_commande", "avis"} <= tables


def test_colonnes_clients(db):
    colonnes = [r[1] for r in db.execute("PRAGMA table_info(clients)")]
    assert colonnes == ["id", "nom", "email", "ville", "pays",
                        "date_inscription"]


def test_colonnes_lignes_commande(db):
    colonnes = [r[1] for r in db.execute("PRAGMA table_info(lignes_commande)")]
    assert colonnes == ["id", "commande_id", "produit_id",
                        "quantite", "prix_unitaire"]


def test_cles_etrangeres_declarees(db):
    cles = {r[2] for r in db.execute("PRAGMA foreign_key_list(lignes_commande)")}
    assert cles == {"commandes", "produits"}
    cles_avis = {r[2] for r in db.execute("PRAGMA foreign_key_list(avis)")}
    assert cles_avis == {"produits", "clients"}


def test_contrainte_quantite_positive(db):
    # Une quantité nulle ou négative doit être refusée.
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO lignes_commande (commande_id, produit_id, "
                   "quantite, prix_unitaire) VALUES (1, 1, 0, 10.00)")


def test_contrainte_note_entre_1_et_5(db):
    with pytest.raises(sqlite3.IntegrityError):
        db.execute("INSERT INTO avis (produit_id, client_id, note, date_avis) "
                   "VALUES (1, 1, 6, '2026-01-01')")


def test_index_crees(db):
    index = {r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'index'")}
    assert {"idx_commandes_date", "idx_lignes_commande",
            "idx_lignes_produit", "idx_avis_produit"} <= index

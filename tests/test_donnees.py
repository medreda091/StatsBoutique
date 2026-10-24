"""Vérifie la qualité du jeu de données : volumes et intégrité."""


def test_volumes(db):
    assert db.execute("SELECT COUNT(*) FROM categories").fetchone()[0] == 8
    assert db.execute("SELECT COUNT(*) FROM clients").fetchone()[0] == 200
    assert db.execute("SELECT COUNT(*) FROM produits").fetchone()[0] == 40
    assert db.execute("SELECT COUNT(*) FROM commandes").fetchone()[0] == 1400
    assert db.execute("SELECT COUNT(*) FROM avis").fetchone()[0] == 450
    assert db.execute("SELECT COUNT(*) FROM lignes_commande").fetchone()[0] > 0


def test_emails_uniques(db):
    total = db.execute("SELECT COUNT(*) FROM clients").fetchone()[0]
    distincts = db.execute("SELECT COUNT(DISTINCT email) FROM clients").fetchone()[0]
    assert total == distincts


def test_prix_et_quantites_coherents(db):
    assert db.execute("SELECT COUNT(*) FROM produits WHERE prix <= 0").fetchone()[0] == 0
    assert db.execute("SELECT COUNT(*) FROM produits WHERE cout < 0").fetchone()[0] == 0
    assert db.execute(
        "SELECT COUNT(*) FROM lignes_commande WHERE quantite <= 0"
    ).fetchone()[0] == 0
    assert db.execute(
        "SELECT COUNT(*) FROM avis WHERE note NOT BETWEEN 1 AND 5"
    ).fetchone()[0] == 0


def test_pas_de_lignes_orphelines(db):
    orphelines = db.execute("""
        SELECT COUNT(*)
        FROM lignes_commande l
        LEFT JOIN commandes c ON c.id = l.commande_id
        LEFT JOIN produits p ON p.id = l.produit_id
        WHERE c.id IS NULL OR p.id IS NULL
    """).fetchone()[0]
    assert orphelines == 0


def test_commandes_apres_inscription(db):
    anterieures = db.execute("""
        SELECT COUNT(*)
        FROM commandes c
        JOIN clients cl ON cl.id = c.client_id
        WHERE c.date_commande < cl.date_inscription
    """).fetchone()[0]
    assert anterieures == 0


def test_prix_unitaire_egal_au_prix_produit(db):
    differents = db.execute("""
        SELECT COUNT(*)
        FROM lignes_commande l
        JOIN produits p ON p.id = l.produit_id
        WHERE l.prix_unitaire <> p.prix
    """).fetchone()[0]
    assert differents == 0


def test_trois_produits_jamais_vendus(db):
    jamais_vendus = db.execute("""
        SELECT COUNT(*)
        FROM produits p
        LEFT JOIN lignes_commande l ON l.produit_id = p.id
        WHERE l.id IS NULL
    """).fetchone()[0]
    assert jamais_vendus == 3

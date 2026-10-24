"""Vérifie que les vues existent et retournent des résultats justes."""


def test_vues_existantes(db):
    vues = {r[0] for r in db.execute(
        "SELECT name FROM sqlite_master WHERE type = 'view'")}
    assert {"vue_lignes_detail", "vue_ca_mensuel",
            "vue_stats_produits"} <= vues


def test_vue_lignes_detail_complete(db):
    nb_vue = db.execute("SELECT COUNT(*) FROM vue_lignes_detail").fetchone()[0]
    nb_lignes = db.execute("SELECT COUNT(*) FROM lignes_commande").fetchone()[0]
    assert nb_vue == nb_lignes


def test_vue_ca_mensuel_juste(db):
    total_vue = db.execute(
        "SELECT ROUND(SUM(chiffre_affaires), 2) FROM vue_ca_mensuel"
    ).fetchone()[0]
    total_direct = db.execute("""
        SELECT ROUND(SUM(l.quantite * l.prix_unitaire), 2)
        FROM lignes_commande l
        JOIN commandes c ON c.id = l.commande_id
        WHERE c.statut <> 'annulee'
    """).fetchone()[0]
    assert total_vue == total_direct


def test_vue_stats_produits_un_produit_par_ligne(db):
    assert db.execute("SELECT COUNT(*) FROM vue_stats_produits").fetchone()[0] == 40


def test_vue_stats_produits_marge_coherente(db):
    incoherentes = db.execute("""
        SELECT COUNT(*)
        FROM vue_stats_produits v
        JOIN produits p ON p.id = v.produit_id
        WHERE ROUND(v.marge_unitaire, 2) <> ROUND(p.prix - p.cout, 2)
    """).fetchone()[0]
    assert incoherentes == 0

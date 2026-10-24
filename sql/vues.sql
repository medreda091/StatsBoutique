-- =====================================================================
-- StatsBoutique — vues pour simplifier les analyses
-- =====================================================================

-- Détail de chaque ligne de commande, avec toutes les dimensions utiles.
CREATE VIEW vue_lignes_detail AS
SELECT l.id              AS ligne_id,
       c.id              AS commande_id,
       c.date_commande,
       c.statut,
       cl.id             AS client_id,
       cl.nom            AS client_nom,
       cl.ville          AS client_ville,
       p.id              AS produit_id,
       p.nom             AS produit_nom,
       cat.nom           AS categorie,
       l.quantite,
       l.prix_unitaire,
       l.quantite * l.prix_unitaire AS montant
FROM lignes_commande l
JOIN commandes c  ON c.id = l.commande_id
JOIN clients cl   ON cl.id = c.client_id
JOIN produits p   ON p.id = l.produit_id
JOIN categories cat ON cat.id = p.categorie_id;

-- Chiffre d'affaires par mois (commandes non annulées).
CREATE VIEW vue_ca_mensuel AS
SELECT substr(c.date_commande, 1, 7) AS mois,
       COUNT(DISTINCT c.id)          AS nb_commandes,
       SUM(l.quantite * l.prix_unitaire) AS chiffre_affaires
FROM commandes c
JOIN lignes_commande l ON l.commande_id = c.id
WHERE c.statut <> 'annulee'
GROUP BY mois;

-- Statistiques par produit : ventes, chiffre d'affaires et avis.
CREATE VIEW vue_stats_produits AS
SELECT p.id AS produit_id,
       p.nom AS produit_nom,
       cat.nom AS categorie,
       p.prix,
       p.prix - p.cout AS marge_unitaire,
       COALESCE(v.quantite_vendue, 0) AS quantite_vendue,
       COALESCE(v.chiffre_affaires, 0) AS chiffre_affaires,
       COALESCE(a.nb_avis, 0) AS nb_avis,
       a.note_moyenne
FROM produits p
JOIN categories cat ON cat.id = p.categorie_id
LEFT JOIN (
    SELECT l.produit_id,
           SUM(l.quantite) AS quantite_vendue,
           SUM(l.quantite * l.prix_unitaire) AS chiffre_affaires
    FROM lignes_commande l
    JOIN commandes c ON c.id = l.commande_id
    WHERE c.statut <> 'annulee'
    GROUP BY l.produit_id
) v ON v.produit_id = p.id
LEFT JOIN (
    SELECT produit_id,
           COUNT(*) AS nb_avis,
           ROUND(AVG(note), 2) AS note_moyenne
    FROM avis
    GROUP BY produit_id
) a ON a.produit_id = p.id;

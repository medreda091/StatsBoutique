-- 07 — Rentabilité par catégorie : marge totale, marge moyenne et taux.
-- Techniques : jointures, agrégation, calculs sur plusieurs tables.

SELECT cat.nom AS categorie,
       COUNT(DISTINCT p.id) AS nb_produits,
       SUM(l.quantite) AS quantite_vendue,
       ROUND(SUM(l.quantite * l.prix_unitaire), 2) AS chiffre_affaires,
       ROUND(SUM(l.quantite * (l.prix_unitaire - p.cout)), 2) AS marge_totale,
       ROUND(100.0 * SUM(l.quantite * (l.prix_unitaire - p.cout))
             / SUM(l.quantite * l.prix_unitaire), 1) AS taux_marge_pct
FROM categories cat
JOIN produits p ON p.categorie_id = cat.id
JOIN lignes_commande l ON l.produit_id = p.id
JOIN commandes c ON c.id = l.commande_id
WHERE c.statut <> 'annulee'
GROUP BY cat.nom
ORDER BY marge_totale DESC;

-- 02 — Les 10 produits qui rapportent le plus, et leur part du CA total.
-- Techniques : CTE, SUM() OVER () pour le total sans GROUP BY supplémentaire.

WITH ca_produits AS (
    SELECT p.nom AS produit,
           cat.nom AS categorie,
           SUM(l.quantite * l.prix_unitaire) AS ca
    FROM lignes_commande l
    JOIN commandes c ON c.id = l.commande_id
    JOIN produits p ON p.id = l.produit_id
    JOIN categories cat ON cat.id = p.categorie_id
    WHERE c.statut <> 'annulee'
    GROUP BY p.nom, cat.nom
)
SELECT produit,
       categorie,
       ROUND(ca, 2) AS chiffre_affaires,
       ROUND(100.0 * ca / SUM(ca) OVER (), 2) AS part_du_ca_pct
FROM ca_produits
ORDER BY ca DESC
LIMIT 10;

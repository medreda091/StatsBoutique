-- 03 — Panier moyen par mois et écart par rapport à la moyenne globale.
-- Techniques : agrégation, sous-requête scalaire.

WITH paniers AS (
    SELECT c.id AS commande_id,
           substr(c.date_commande, 1, 7) AS mois,
           SUM(l.quantite * l.prix_unitaire) AS panier
    FROM commandes c
    JOIN lignes_commande l ON l.commande_id = c.id
    WHERE c.statut <> 'annulee'
    GROUP BY c.id, mois
)
SELECT mois,
       COUNT(*) AS nb_commandes,
       ROUND(AVG(panier), 2) AS panier_moyen,
       ROUND(AVG(panier) - (SELECT AVG(panier) FROM paniers), 2)
           AS ecart_moyenne_globale
FROM paniers
GROUP BY mois
ORDER BY mois;

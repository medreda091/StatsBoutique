-- 01 — Chiffre d'affaires mensuel et croissance d'un mois sur l'autre.
-- Techniques : CTE, fonction de fenêtrage LAG.

WITH ca_mensuel AS (
    SELECT substr(c.date_commande, 1, 7) AS mois,
           SUM(l.quantite * l.prix_unitaire) AS ca
    FROM commandes c
    JOIN lignes_commande l ON l.commande_id = c.id
    WHERE c.statut <> 'annulee'
    GROUP BY mois
)
SELECT mois,
       ROUND(ca, 2) AS chiffre_affaires,
       ROUND(LAG(ca) OVER (ORDER BY mois), 2) AS ca_mois_precedent,
       ROUND(
           100.0 * (ca - LAG(ca) OVER (ORDER BY mois))
           / NULLIF(LAG(ca) OVER (ORDER BY mois), 0),
           2
       ) AS croissance_pct
FROM ca_mensuel
ORDER BY mois;

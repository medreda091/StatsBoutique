-- 06 — Chiffre d'affaires journalier et cumul depuis le début.
-- Techniques : SUM() OVER (ORDER BY ... ROWS BETWEEN ...).

WITH ca_journalier AS (
    SELECT c.date_commande AS jour,
           SUM(l.quantite * l.prix_unitaire) AS ca
    FROM commandes c
    JOIN lignes_commande l ON l.commande_id = c.id
    WHERE c.statut <> 'annulee'
    GROUP BY jour
)
SELECT jour,
       ROUND(ca, 2) AS chiffre_affaires,
       ROUND(SUM(ca) OVER (
           ORDER BY jour
           ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
       ), 2) AS ca_cumule,
       ROUND(AVG(ca) OVER (
           ORDER BY jour
           ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
       ), 2) AS moyenne_mobile_7j
FROM ca_journalier
ORDER BY jour;

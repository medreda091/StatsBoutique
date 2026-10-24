-- 10 — Segmentation RFM des clients (récence, fréquence, montant).
-- La récence est exprimée en mois par rapport au 2026-09-30.
-- Techniques : CTE, NTILE, concaténation de scores.

WITH stats_clients AS (
    SELECT c.client_id,
           MAX(c.date_commande) AS derniere_commande,
           COUNT(*) AS frequence,
           SUM(l.quantite * l.prix_unitaire) AS montant
    FROM commandes c
    JOIN lignes_commande l ON l.commande_id = c.id
    WHERE c.statut <> 'annulee'
    GROUP BY c.client_id
),
rfm AS (
    SELECT client_id,
           -- Mois écoulés entre la dernière commande et la date de référence.
           (2026 * 12 + 9)
             - (CAST(substr(derniere_commande, 1, 4) AS INTEGER) * 12
                + CAST(substr(derniere_commande, 6, 2) AS INTEGER))
               AS recence_mois,
           frequence,
           montant
    FROM stats_clients
),
scores AS (
    SELECT client_id,
           recence_mois,
           frequence,
           ROUND(montant, 2) AS montant,
           NTILE(4) OVER (ORDER BY recence_mois ASC) AS score_r,
           NTILE(4) OVER (ORDER BY frequence DESC) AS score_f,
           NTILE(4) OVER (ORDER BY montant DESC) AS score_m
    FROM rfm
)
SELECT cl.nom AS client,
       s.recence_mois,
       s.frequence,
       s.montant,
       -- On inverse R : 1 = le plus récent.
       (5 - s.score_r) || s.score_f || s.score_m AS score_rfm
FROM scores s
JOIN clients cl ON cl.id = s.client_id
ORDER BY score_rfm DESC, s.montant DESC
LIMIT 30;

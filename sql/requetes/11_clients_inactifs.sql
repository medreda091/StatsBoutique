-- 11 — Clients inactifs : aucune commande depuis plus de 6 mois
-- (par rapport au 2026-09-30) ou aucune commande du tout. Cible relance.
-- Technique : LEFT JOIN sur une agrégation.

WITH derniere_commande AS (
    SELECT client_id,
           MAX(date_commande) AS derniere
    FROM commandes
    WHERE statut <> 'annulee'
    GROUP BY client_id
)
SELECT cl.nom AS client,
       cl.email,
       cl.ville,
       dc.derniere AS derniere_commande
FROM clients cl
LEFT JOIN derniere_commande dc ON dc.client_id = cl.id
WHERE dc.derniere IS NULL OR dc.derniere < '2026-04-01'
ORDER BY dc.derniere;

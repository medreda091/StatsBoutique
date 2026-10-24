-- 04 — Cohortes d'inscription : combien de clients recommandent ?
-- Un client est « récurrent » s'il a passé au moins 2 commandes non annulées.
-- Techniques : CTE, CASE, agrégation conditionnelle.

WITH commandes_client AS (
    SELECT c.client_id,
           COUNT(*) AS nb_commandes
    FROM commandes c
    WHERE c.statut <> 'annulee'
    GROUP BY c.client_id
)
SELECT substr(cl.date_inscription, 1, 7) AS cohorte,
       COUNT(*) AS nb_clients,
       SUM(CASE WHEN cc.nb_commandes >= 2 THEN 1 ELSE 0 END)
           AS nb_clients_recurrents,
       ROUND(100.0 * SUM(CASE WHEN cc.nb_commandes >= 2 THEN 1 ELSE 0 END)
             / COUNT(*), 1) AS taux_recurrence_pct
FROM clients cl
LEFT JOIN commandes_client cc ON cc.client_id = cl.id
GROUP BY cohorte
ORDER BY cohorte;

-- 05 — Classement des 20 meilleurs clients : rang et quartile de CA.
-- Techniques : RANK, DENSE_RANK, NTILE.

WITH ca_clients AS (
    SELECT cl.nom AS client,
           cl.ville,
           SUM(l.quantite * l.prix_unitaire) AS ca
    FROM clients cl
    JOIN commandes c ON c.client_id = cl.id
    JOIN lignes_commande l ON l.commande_id = c.id
    WHERE c.statut <> 'annulee'
    GROUP BY cl.nom, cl.ville
)
SELECT client,
       ville,
       ROUND(ca, 2) AS chiffre_affaires,
       RANK() OVER (ORDER BY ca DESC) AS rang,
       DENSE_RANK() OVER (ORDER BY ca DESC) AS rang_dense,
       NTILE(4) OVER (ORDER BY ca DESC) AS quartile
FROM ca_clients
ORDER BY ca DESC
LIMIT 20;

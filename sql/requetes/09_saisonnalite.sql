-- 09 — Saisonnalité : quel mois calendaire vend le plus, toutes années confondues ?
-- Technique : regroupement sur une partie de la date.

SELECT CAST(substr(c.date_commande, 6, 2) AS INTEGER) AS mois_calendaire,
       COUNT(DISTINCT c.id) AS nb_commandes,
       ROUND(SUM(l.quantite * l.prix_unitaire), 2) AS chiffre_affaires,
       ROUND(AVG(l.quantite * l.prix_unitaire), 2) AS panier_moyen
FROM commandes c
JOIN lignes_commande l ON l.commande_id = c.id
WHERE c.statut <> 'annulee'
GROUP BY mois_calendaire
ORDER BY chiffre_affaires DESC;

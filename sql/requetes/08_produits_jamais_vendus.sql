-- 08 — Produits qui n'ont jamais été vendus : à solder ou à retirer ?
-- Technique : anti-jointure (LEFT JOIN + IS NULL).

SELECT p.nom AS produit,
       cat.nom AS categorie,
       p.prix,
       p.date_ajout
FROM produits p
JOIN categories cat ON cat.id = p.categorie_id
LEFT JOIN lignes_commande l ON l.produit_id = p.id
WHERE l.id IS NULL
ORDER BY p.date_ajout;

-- 12 — Satisfaction par produit : note moyenne vs moyenne de sa catégorie.
-- Techniques : AVG() OVER (PARTITION BY ...), jointure de vues.

SELECT produit_nom,
       categorie,
       nb_avis,
       note_moyenne,
       ROUND(AVG(note_moyenne) OVER (PARTITION BY categorie), 2)
           AS moyenne_categorie,
       ROUND(note_moyenne - AVG(note_moyenne) OVER (PARTITION BY categorie), 2)
           AS ecart_categorie
FROM vue_stats_produits
WHERE nb_avis >= 5
ORDER BY ecart_categorie DESC;

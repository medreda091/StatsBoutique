# StatsBoutique

Base de données e-commerce fictive et **12 requêtes d'analyse en SQL avancé** :
fonctions de fenêtrage, CTE, vues, anti-jointures, segmentation RFM…

Le projet montre un usage concret de PostgreSQL pour l'analyse de données :
nettoyer le besoin métier, écrire la requête, vérifier le résultat avec des tests.

## Contenu

- `sql/schema.sql` — 6 tables : clients, catégories, produits, commandes,
  lignes de commande, avis (+ index).
- `sql/donnees.sql` — jeu de données réaliste généré par script :
  200 clients, 40 produits, 1 400 commandes, 450 avis.
- `sql/vues.sql` — 3 vues pour simplifier les analyses
  (`vue_lignes_detail`, `vue_ca_mensuel`, `vue_stats_produits`).
- `sql/requetes/` — 12 requêtes numérotées, chacune avec un commentaire
  qui explique la question métier et les techniques utilisées.
- `scripts/generer_donnees.py` — génère `donnees.sql` (graine fixe,
  donc le fichier est toujours identique).
- `tests/` — 40 tests pytest qui chargent tout en mémoire et vérifient
  le schéma, les données, les vues et chaque requête.

## Les 12 requêtes

| # | Question | Techniques |
|---|----------|------------|
| 01 | CA mensuel et croissance d'un mois sur l'autre | CTE, `LAG` |
| 02 | Top 10 des produits et leur part du CA total | `SUM() OVER ()` |
| 03 | Panier moyen par mois vs moyenne globale | Sous-requête |
| 04 | Cohortes d'inscription et taux de clients récurrents | `CASE`, agrégation conditionnelle |
| 05 | Classement des meilleurs clients | `RANK`, `DENSE_RANK`, `NTILE` |
| 06 | CA journalier, cumul et moyenne mobile 7 jours | `SUM() OVER (ORDER BY … ROWS …)` |
| 07 | Marge totale et taux de marge par catégorie | Jointures, agrégation |
| 08 | Produits jamais vendus | Anti-jointure (`LEFT JOIN … IS NULL`) |
| 09 | Saisonnalité : quel mois calendaire vend le plus | Regroupement sur la date |
| 10 | Segmentation RFM des clients | CTE, `NTILE` |
| 11 | Clients inactifs depuis 6 mois (cible relance) | `LEFT JOIN` sur agrégation |
| 12 | Note moyenne d'un produit vs sa catégorie | `AVG() OVER (PARTITION BY …)` |

Exemple de résultat (requête 02 — top produits) :

```
Aspirateur robot | Maison      | 72297.59 € | 11.19 % du CA
Robot pâtissier  | Cuisine     | 70697.98 € | 10.95 % du CA
Volant de course | Jeux vidéo  | 50747.97 € | 7.86 % du CA
```

## Stack

PostgreSQL 16, SQL standard, Python 3 (génération des données + tests),
Docker Compose, GitHub Actions.

## Installation

### Option 1 — PostgreSQL avec Docker (recommandé)

```bash
make db
# La base stats_boutique est créée avec le schéma,
# les données et les vues déjà chargés.
make psql
```

Puis, pour exécuter une requête :

```bash
docker compose exec -T db psql -U boutique -d stats_boutique \
  < sql/requetes/01_ca_mensuel_croissance.sql
```

### Option 2 — test rapide sans Docker

Les tests utilisent SQLite en mémoire (aucun prérequis) :

```bash
pip install -r requirements.txt
make test
```

## Utilisation

Chaque fichier de `sql/requetes/` est autonome : ouvrez-le dans
psql, DBeaver ou DataGrip et exécutez-le. Exemple avec psql :

```bash
docker compose exec -T db psql -U boutique -d stats_boutique \
  < sql/requetes/05_classement_clients.sql
```

Pour régénérer les données (elles sont déterministes) :

```bash
python3 scripts/generer_donnees.py
```

## Structure

```
StatsBoutique/
├── sql/
│   ├── schema.sql        # tables + index
│   ├── donnees.sql       # données générées (ne pas éditer à la main)
│   ├── vues.sql          # 3 vues d'analyse
│   └── requetes/         # 12 requêtes numérotées
├── scripts/
│   └── generer_donnees.py
├── tests/                # 40 tests pytest
├── docker-compose.yml
├── Makefile
└── .github/workflows/ci.yml
```

## Tests

```bash
make test
# 40 passed
```

Les tests vérifient le schéma (tables, colonnes, contraintes),
l'intégrité des données (pas d'orphelins, volumes attendus),
la justesse des vues et de chaque requête (totaux, tris, rangs…).

## Licence

MIT — voir [LICENSE](LICENSE).

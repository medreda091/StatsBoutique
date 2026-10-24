-- =====================================================================
-- StatsBoutique — schéma de la base de données
-- Boutique en ligne fictive : clients, produits, commandes et avis.
-- SQL standard, compatible PostgreSQL (cible) et SQLite (tests).
-- =====================================================================

CREATE TABLE categories (
    id   INTEGER PRIMARY KEY,
    nom  TEXT NOT NULL UNIQUE
);

CREATE TABLE clients (
    id               INTEGER PRIMARY KEY,
    nom              TEXT NOT NULL,
    email            TEXT NOT NULL UNIQUE,
    ville            TEXT NOT NULL,
    pays             TEXT NOT NULL DEFAULT 'France',
    date_inscription DATE NOT NULL
);

CREATE TABLE produits (
    id           INTEGER PRIMARY KEY,
    nom          TEXT NOT NULL,
    categorie_id INTEGER NOT NULL REFERENCES categories (id),
    prix         DECIMAL(10, 2) NOT NULL CHECK (prix > 0),
    cout         DECIMAL(10, 2) NOT NULL CHECK (cout >= 0),
    date_ajout   DATE NOT NULL
);

CREATE TABLE commandes (
    id             INTEGER PRIMARY KEY,
    client_id      INTEGER NOT NULL REFERENCES clients (id),
    date_commande  DATE NOT NULL,
    statut         TEXT NOT NULL DEFAULT 'livree'
                   CHECK (statut IN ('en_preparation', 'expediee', 'livree', 'annulee'))
);

CREATE TABLE lignes_commande (
    id            INTEGER PRIMARY KEY,
    commande_id   INTEGER NOT NULL REFERENCES commandes (id),
    produit_id    INTEGER NOT NULL REFERENCES produits (id),
    quantite      INTEGER NOT NULL CHECK (quantite > 0),
    prix_unitaire DECIMAL(10, 2) NOT NULL CHECK (prix_unitaire >= 0)
);

CREATE TABLE avis (
    id          INTEGER PRIMARY KEY,
    produit_id  INTEGER NOT NULL REFERENCES produits (id),
    client_id   INTEGER NOT NULL REFERENCES clients (id),
    note        INTEGER NOT NULL CHECK (note BETWEEN 1 AND 5),
    commentaire TEXT,
    date_avis   DATE NOT NULL
);

-- Index pour accélérer les analyses par date et les jointures fréquentes.
CREATE INDEX idx_commandes_date ON commandes (date_commande);
CREATE INDEX idx_lignes_commande ON lignes_commande (commande_id);
CREATE INDEX idx_lignes_produit ON lignes_commande (produit_id);
CREATE INDEX idx_avis_produit ON avis (produit_id);

"""Base de test : charge le schéma, les données et les vues en mémoire."""

import sqlite3
from pathlib import Path

import pytest

RACINE = Path(__file__).resolve().parents[1]
DOSSIER_SQL = RACINE / "sql"


def charger_base() -> sqlite3.Connection:
    """Construit une base SQLite en mémoire avec tout le projet chargé."""
    connexion = sqlite3.connect(":memory:")
    connexion.execute("PRAGMA foreign_keys = ON")
    connexion.executescript((DOSSIER_SQL / "schema.sql").read_text(encoding="utf-8"))
    connexion.executescript((DOSSIER_SQL / "donnees.sql").read_text(encoding="utf-8"))
    connexion.executescript((DOSSIER_SQL / "vues.sql").read_text(encoding="utf-8"))
    return connexion


def lire_requete(numero: int) -> str:
    """Lit le fichier SQL d'une requête d'analyse par son numéro (1 à 12)."""
    fichiers = sorted((DOSSIER_SQL / "requetes").glob("*.sql"))
    return fichiers[numero - 1].read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def db():
    connexion = charger_base()
    yield connexion
    connexion.close()

# Raccourcis pour StatsBoutique.

test:  ## Lance les tests (base SQLite en mémoire, aucun prérequis).
	python3 -m pytest tests/ -q

db:  ## Démarre PostgreSQL avec le schéma, les données et les vues chargés.
	docker compose up -d db

psql:  ## Ouvre un shell psql sur la base.
	docker compose exec db psql -U boutique -d stats_boutique

stop:  ## Arrête PostgreSQL.
	docker compose down

clean:  ## Supprime la base PostgreSQL (les données seront régénérées).
	docker compose down -v

.PHONY: test db psql stop clean

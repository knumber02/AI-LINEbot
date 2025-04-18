
#############################################
# alembic（マイグレーションツール）の汎用コマンド
#############################################

.PHONY: alembic-migrate
migrate:
	poetry run python -m alembic upgrade head

.PHONY: alembic-rollback
rollback:
	poetry run python -m alembic downgrade -1

.PHONY: alembic-refresh
fresh:
	poetry run python -m alembic downgrade base
	poetry run python -m alembic upgrade head

.PHONY: alembic-autogenerate
autogenerate:
	poetry run python -m alembic revision --autogenerate -m "$(message)"

#############################################
# シーダーの汎用コマンド
#############################################

.PHONY: seed
seed:
	poetry run python -m api.database.seeders.run_seeder

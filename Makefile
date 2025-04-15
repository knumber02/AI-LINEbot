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
refresh:
	poetry run python -m alembic downgrade base
	poetry run python -m alembic upgrade head

.PHONY: alembic-autogenerate
autogenerate:
	poetry run python -m alembic revision --autogenerate -m "$(message)"


#############################################
# alembic（マイグレーションツール）の汎用コマンド
#############################################

.PHONY: alembic-migrate
migrate:
	cd demo_app && poetry run python -m alembic upgrade head

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

#############################################
# Lambdaデプロイ用ZIP作成
#############################################

.PHONY: build-zip
build-zip:
	rm -rf lambda_build lambda_package.zip
	poetry export --without-hashes -f requirements.txt > requirements.txt
	pip install --target=lambda_build/ -r requirements.txt
	cp -r demo_app lambda_build/
	cp demo_app/lambda_handler.py lambda_build/
	cd lambda_build && zip -r ../lambda_package.zip .

.PHONY: upload-zip
upload-zip:
	aws s3 cp lambda_package.zip s3://fastapi-line-bot/

.PHONY: login-aws
login-aws:
	aws sso login --profile my-sso-profile

.PHONY: get-caller-identity
get-caller-identity:
	aws sts get-caller-identity --profile my-sso-profile

.PHONY: terraform-plan
terraform-plan:
	cd terraform && terraform plan

.PHONY: terraform-apply
terraform-apply:
	cd terraform && terraform apply


#############################################
# お掃除コマンド
#############################################

.PHONY: clean
clean:
	rm -rf lambda_build lambda_package.zip requirements.txt

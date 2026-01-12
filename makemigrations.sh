export PYTHONPATH="$(pwd)/src"

alembic revision --autogenerate --version-path=src/infra/migrations

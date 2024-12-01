alembic revision --autogenerate -m "Intial migration"
alembic upgrade head

python main.py

exec "$@"
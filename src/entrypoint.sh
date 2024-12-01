if alembic check | grep -q 'No new upgrade operations detected.'; then
    echo 'No migrations detected'
else
    alembic revision --autogenerate -m 'Intial migration'
fi

alembic upgrade head

python main.py

exec "$@"
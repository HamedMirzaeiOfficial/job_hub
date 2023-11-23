SET DEBUG=True
SET DB_ENGINE=sqlite3
echo 'Environment Variables Added'

pip install -r requirements.txt

python manage.py collectstatic --noinput
python manage.py makemigrations
python manage.py migrate
python manage.py runserver